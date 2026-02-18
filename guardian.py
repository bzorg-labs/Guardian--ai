from sklearn.tree import DecisionTreeClassifier

X = [
    [500, 1000, 10, 0, 0],
    [1500, 1000, 14, 1, 1],
    [1200, 2000, 2, 0, 1],
    [2000, 1500, 20, 1, 1],
    [800, 1000, 1, 0, 0]
]

y = ["approve", "decline", "manual review", "decline", "manual review"]

model = DecisionTreeClassifier(max_depth=3)
model.fit(X, y)

def predict_transaction(tx):
    decision = model.predict([tx])[0]
    amount, balance, hour, country_risk, device_risk = tx

    reasons = []

    if amount > balance:
        reasons.append("Amount is greater than balance")
    if amount > 1000 and country_risk == 1:
        reasons.append("High amount and risky country")
    if hour < 6 or hour > 23:
        reasons.append("Transaction at unusual hour")
    if country_risk == 1:
        reasons.append("Risky country")
    if device_risk == 1:
        reasons.append("Risky device")

    if len(reasons) == 0:
        reasons.append("All checks passed")

    return decision, reasons