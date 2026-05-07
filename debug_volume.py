spread_per_pair = 10.64  # Fixed $ spread between exchanges

fees = [
    ("0.1% (default)", 0.001),
    ("0.05% (taker)", 0.0005),
    ("0.02% (maker)", 0.0002),
    ("0.01% (high vol)", 0.0001),
]

amounts = [81000, 810000, 8100000]  # $81k, $810k, $8.1M

print("Volume | Fee Rate | Spread $ | Fee $ | Net $ | Profit %")
print("-" * 55)
for amount in amounts:
    for fee_name, fee_pct in fees:
        fee_cost = amount * fee_pct * 2  # both sides
        net = spread_per_pair - fee_cost
        profit_pct = (net / amount) * 100
        print(f"${amount:>7} | {fee_name:>12} | ${spread_per_pair:>6.2f} | ${fee_cost:>6.2f} | ${net:>7.2f} | {profit_pct:>6.4f}%")