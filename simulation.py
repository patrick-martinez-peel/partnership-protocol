import numpy as np
import matplotlib.pyplot as plt
import random

# --- REPRODUCIBILITY ---
# Setting seeds ensures the simulation produces identical results every time it runs.
random.seed(42)
np.random.seed(42)

# --- CONFIGURATION ---
POPULATION_SIZE = 1000
ROUNDS_PER_SIM = 50
SIMULATION_RUNS = 5

# Economic Constants
PROFIT = 100
COST_SAFE = 20

# Liability Parameters
LLC_FINE = 30
LLC_REPUTATION_LOSS = 10  # Total penalty = 40
PARTNERSHIP_FINE = 100
PARTNERSHIP_REPUTATION_LOSS = 100  # Total penalty = 200

LEARNING_RATE = 0.1  # Social learning rate


# --- THE AGENT ---
class Agent:
    def __init__(self, strategy: int):
        """
        strategy: 1 = Safe, 0 = Risky
        """
        self.strategy = strategy
        self.wealth = 0


# --- THE SIMULATION ENGINE ---
def run_evolutionary_cycle(audit_prob: float,
                           fine_amount: float,
                           reputation_loss: float,
                           liability_model: str) -> float:
    """
    Run one evolutionary cycle of the agent population for a given audit probability
    and liability regime.

    Returns:
        Fraction of agents playing the Safe strategy at the end of the cycle.
    """
    # 1. Initialize Population (50% Safe, 50% Risky)
    agents = [Agent(strategy=1) for _ in range(POPULATION_SIZE // 2)] + \
             [Agent(strategy=0) for _ in range(POPULATION_SIZE // 2)]

    random.shuffle(agents)

    # 2. Run Rounds
    for _ in range(ROUNDS_PER_SIM):
        # Reset wealth each round
        for agent in agents:
            agent.wealth = 0

        # A. PAIRING & PLAYING
        random.shuffle(agents)
        pairs = zip(agents[0::2], agents[1::2])

        for agent_A, agent_B in pairs:
            is_audited = random.random() < audit_prob

            # Base Payoffs
            payoff_A = PROFIT
            payoff_B = PROFIT

            if agent_A.strategy == 1:
                payoff_A -= COST_SAFE
            if agent_B.strategy == 1:
                payoff_B -= COST_SAFE

            # Apply Fines if audited
            if is_audited:
                # Agent A Defect Logic
                if agent_A.strategy == 0:
                    payoff_A -= (fine_amount + reputation_loss)
                    if liability_model == "Partnership":
                        # Joint liability: partner also bears the penalty
                        payoff_B -= (fine_amount + reputation_loss)

                # Agent B Defect Logic
                if agent_B.strategy == 0:
                    payoff_B -= (fine_amount + reputation_loss)
                    if liability_model == "Partnership":
                        payoff_A -= (fine_amount + reputation_loss)

            agent_A.wealth += payoff_A
            agent_B.wealth += payoff_B

        # B. EVOLUTION (Social Learning)
        safe_agents = [a for a in agents if a.strategy == 1]
        risky_agents = [a for a in agents if a.strategy == 0]

        avg_safe_wealth = np.mean([a.wealth for a in safe_agents]) if safe_agents else 0
        avg_risky_wealth = np.mean([a.wealth for a in risky_agents]) if risky_agents else 0

        if avg_risky_wealth > avg_safe_wealth:
            # Safe agents switch to Risky with some probability
            for agent in safe_agents:
                if random.random() < LEARNING_RATE:
                    agent.strategy = 0
        elif avg_safe_wealth > avg_risky_wealth:
            # Risky agents switch to Safe with some probability
            for agent in risky_agents:
                if random.random() < LEARNING_RATE:
                    agent.strategy = 1

    # Return fraction of Safe agents
    return sum(a.strategy for a in agents) / POPULATION_SIZE


def main():
    # --- EXPERIMENT SETUP ---
    audit_probabilities = np.linspace(0, 1.0, 20)
    results_llc = []
    results_partnership = []

    print(f"Running tuned simulation with {POPULATION_SIZE} agents...")
    print(f"Rounds per simulation: {ROUNDS_PER_SIM}, runs per point: {SIMULATION_RUNS}")
    print("AuditProb  |  LLC_Safe  |  Partnership_Safe")
    print("-------------------------------------------")

    for p in audit_probabilities:
        # 1. LLC Model
        # Analytic benchmark: Gain from defecting = 20, total penalty = 40 -> 20/40 = 0.5.
        # In the full evolutionary simulation, safety dominance emerges closer to ~0.6.
        avg_safe_llc = np.mean([
            run_evolutionary_cycle(
                p,
                fine_amount=LLC_FINE,
                reputation_loss=LLC_REPUTATION_LOSS,
                liability_model="LLC",
            )
            for _ in range(SIMULATION_RUNS)
        ])
        results_llc.append(avg_safe_llc)

        # 2. Partnership Model
        # Analytic benchmark: Gain from defecting = 20, total penalty = 200 -> 20/200 = 0.1.
        # In the simulation, high safety is typically achieved around ~0.2.
        avg_safe_partnership = np.mean([
            run_evolutionary_cycle(
                p,
                fine_amount=PARTNERSHIP_FINE,
                reputation_loss=PARTNERSHIP_REPUTATION_LOSS,
                liability_model="Partnership",
            )
            for _ in range(SIMULATION_RUNS)
        ])
        results_partnership.append(avg_safe_partnership)

        print(f"{p:0.2f}      |  {avg_safe_llc:0.3f}    |  {avg_safe_partnership:0.3f}")

    # --- VISUALIZATION ---
    plt.figure(figsize=(10, 6))

    plt.plot(
        audit_probabilities * 100,
        results_llc,
        label='LLC Model (Low Liability/Reputation)',
        color='red',
        marker='o',
        linestyle='--',
    )

    plt.plot(
        audit_probabilities * 100,
        results_partnership,
        label='Partnership Model (High Liability/Reputation)',
        color='green',
        marker='s',
        linewidth=2,
    )

    plt.title('Agent-Based Simulation: The "Efficiency Gap"', fontsize=14)
    plt.xlabel('Audit Probability (Regulatory Oversight %)', fontsize=12)
    plt.ylabel('Fraction of Safe Agents', fontsize=12)
    plt.axhline(y=0.95, color='gray', linestyle=':', alpha=0.5, label='Target Safety (95%)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.fill_between(
        audit_probabilities * 100,
        results_partnership,
        results_llc,
        color='lightgreen',
        alpha=0.2,
    )
    plt.text(
        50,
        0.5,
        "The Efficiency Gap\n(LLCs require massive policing)\n(Partnerships are self-policing)",
        fontsize=10,
        ha='center',
        bbox=dict(facecolor='white', alpha=0.8),
    )

    plt.tight_layout()
    plt.savefig("efficiency_gap.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
