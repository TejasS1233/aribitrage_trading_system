spread = 81361.6 - 81350.96
ask = 81350.96
fee_pct = 0.0005  # 0.05% per side = 0.1% total

fee_cost = ask * fee_pct + 81361.6 * fee_pct
net = spread - fee_cost
profit_pct = (net / ask) * 100

print(f"With 0.05% fees per side (0.1% total):")
print(f"  Fee cost: ${fee_cost:.2f}")
print(f"  Net profit: ${net:.2f}")
print(f"  Profit %: {profit_pct:.4f}%")
print(f"  Threshold 0.01%: {'PASS' if profit_pct >= 0.01 else 'FAIL'}")