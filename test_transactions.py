from guardian import predict_transaction

print("Welcome to Friendly Guardian")

amount = int(input("Enter amount: "))
balance = int(input("Enter balance: "))
hour = int(input("Enter hour (0-23): "))
country_risk = int(input("Country risk (0 or 1): "))
device_risk = int(input("Device risk (0 or 1): "))

tx = [amount, balance, hour, country_risk, device_risk]

decision, log = predict_transaction(tx)

report = []
report.append("=== Friendly Guardian Report ===")
report.append(f"Transaction: {tx}")
report.append(f"Decision: {decision}")
report.extend(log)

with open("report.txt", "w") as f:
    for line in report:
        f.write(line + "\n")

print("Report saved as report.txt")