spread = 81361.6 - 81350.96
ask = 81350.96
fee_pct = 0.0002  # 0.02% maker fee

fee_cost = ask * fee_pct + 81361.6 * fee_pct
net = spread - fee_cost
profit_pct = (net / ask) * 100

print(f"With 0.02% maker fees (pro rate):")
print(f"  Fee cost: ${fee_cost:.2f}")
print(f"  Net profit: ${net:.2f}")
print(f"  Profit %: {profit_pct:.4f}%")
print()

# If you HOLD BTC instead of converting back to USD
# Only pay the buy fee
buy_fee = ask * fee_pct
print(f"If holding BTC (no sell fee):")
print(f"  Cost: ${buy_fee:.2f}")
print(f"  Spread covers buy fee: {'YES' if spread > buy_fee else 'NO'}")