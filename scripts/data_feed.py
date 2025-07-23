import numpy as np
import pandas as pd

n_samples = 10000

asset_classes = ['equity', 'debt', 'gold', 'real_estate', 'crypto', 'cash']
risk_score = [0.9, 0.3, 0.5, 0.6, 1.0, 0.1]

# Randomly generate financial and psychometric factors
ages = np.random.randint(25, 61, size=n_samples)

def estimate_income_from_age(age):
    if 25 <= age <= 30:
        return np.random.randint(30000, 60000)
    elif 31 <= age <= 35:
        return np.random.randint(60000, 90000)
    elif 36 <= age <= 45:
        return np.random.randint(90000, 140000)
    elif 46 <= age <= 55:
        return np.random.randint(80000, 120000)
    elif 56 <= age <= 60:
        return np.random.randint(60000, 100000)
    else:
        return 0

income = np.array([estimate_income_from_age(age) for age in ages])
capital = np.random.randint(100000, 2500000, size=n_samples)

def estimate_dependents_active(age):
    if age < 25 or age > 60:
        return 0
    if 25 <= age <= 35:
        return np.random.choice([0, 1, 2])
    elif 36 <= age <= 45:
        return np.random.choice([1, 2, 3])
    elif 46 <= age <= 55:
        return np.random.choice([1, 2])
    else:
        return np.random.choice([0, 1])

dependents = np.array([estimate_dependents_active(age) for age in ages])

expenses = np.array([int(income[i] * np.random.uniform(0.3, 0.6)) + dependents[i] * 5000 for i in range(n_samples)])
emi = np.array([int(income[i] * np.random.uniform(0.1, 0.3)) for i in range(n_samples)])

def liquidity_from_dependents_and_age(dep, age):
    if age < 35:
        base = 100000
    elif age < 50:
        base = 80000
    else:
        base = 60000
    return base + dep * 10000 + np.random.randint(-5000, 5000)

liquidity_need = np.array([liquidity_from_dependents_and_age(dependents[i], ages[i]) for i in range(n_samples)])

goals = np.random.choice(['retirement', 'growth', 'income'], size=n_samples)

confidence = np.random.uniform(0, 10, size=n_samples)
knowledge = np.random.uniform(0, 10, size=n_samples)
comfort_with_negatives = np.random.uniform(0, 10, size=n_samples)
market_awareness = np.random.uniform(0, 10, size=n_samples)
experience = np.random.uniform(0, 10, size=n_samples)

def score_from_age(age):
    if age <= 30:
        return 0.9
    elif age <= 40:
        return 0.7
    elif age <= 50:
        return 0.5
    elif age <= 60:
        return 0.3
    else:
        return 0.1

def score_from_income(income):
    if income <= 50000:
        return 0.2
    elif income <= 70000:
        return 0.4
    elif income <= 100000:
        return 0.6
    elif income <= 150000:
        return 0.8
    else:
        return 0.9

def score_from_capital(capital):
    if capital <= 500000:
        return 0.2
    elif capital <= 1000000:
        return 0.4
    elif capital <= 1500000:
        return 0.6
    elif capital <= 2000000:
        return 0.8
    else:
        return 0.9

def score_from_goal(goal):
    goal_map = {"retirement": 0.3, "income": 0.6, "growth": 0.9}
    return goal_map.get(goal.lower(), 0.5)

def calculate_profile_score(age, income, capital, goal):
    s_age = score_from_age(age)
    s_income = score_from_income(income)
    s_capital = score_from_capital(capital)
    s_goal = score_from_goal(goal)
    return 0.25 * (s_age + s_income + s_capital + s_goal)

profile_scores = [calculate_profile_score(ages[i], income[i], capital[i], goals[i]) for i in range(n_samples)]

# Utility Constant A calculation
A = []
for i in range(n_samples):
    risk_capacity_score = (income[i] - expenses[i] - emi[i]) / max(capital[i], 1)
    liquidity_factor = 1 - min(liquidity_need[i] / max(capital[i], 1), 1)

    psychometric_avg = np.mean([
        confidence[i],
        knowledge[i],
        comfort_with_negatives[i],
        market_awareness[i],
        experience[i]
    ]) / 10  # Normalize psychometric scores to [0, 1]

    final_risk_tolerance = 0.4 * profile_scores[i] + 0.3 * risk_capacity_score + 0.3 * psychometric_avg
    final_risk_tolerance = np.clip(final_risk_tolerance, 0, 1)

    a_val = 10 * (1 - final_risk_tolerance)
    A.append(round(a_val, 3))

# Generate portfolio allocations using utility A and softmax
allocations = []
for a in A:
    risk_pref = max(min((10 - a) / 10, 1), 0)
    base = np.array(risk_score)
    adjusted = base * (risk_pref + 0.01)  # avoid zero
    exp_scores = np.exp(adjusted)
    softmax_weights = exp_scores / np.sum(exp_scores)
    allocations.append(softmax_weights)

allocations = np.array(allocations)
portfolio_risk = [sum(w * r for w, r in zip(allocations[i], risk_score)) for i in range(n_samples)]

result = pd.DataFrame({
    "age": ages,
    "income": income,
    "capital": capital,
    "expenses": expenses,
    "emi": emi,
    "liquidity_need": liquidity_need,
    "dependents": dependents,
    "goal": goals,
    "confidence": confidence,
    "knowledge": knowledge,
    "comfort_with_negatives": comfort_with_negatives,
    "market_awareness": market_awareness,
    "experience": experience,
    "portfolio_risk": portfolio_risk,
    "profile_score": profile_scores,
    "utility_A": A,
    **{f"weight_{cls}": allocations[:, idx] for idx, cls in enumerate(asset_classes)}
})

print(result.head())

result.to_csv("simulated_investor_profiles.csv", index=False)
print("Data saved to simulated_investor_profiles.csv")
