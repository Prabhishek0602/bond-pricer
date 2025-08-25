import pandas as pd
from datetime import datetime
from bond_math import generate_cashflows, price_from_ytm, ytm_from_price

# Load bonds from CSV
bonds = pd.read_csv("bonds.csv")

results = []

for _, row in bonds.iterrows():
    settlement = datetime.strptime(row["settlement"], "%Y-%m-%d")
    maturity = datetime.strptime(row["maturity"], "%Y-%m-%d")
    coupon_rate = float(row["coupon_rate"])
    face_value = float(row["face_value"])
    ytm_guess = float(row["ytm"])  # starting YTM for pricing

    # Generate cashflows
    cfs = generate_cashflows(settlement, maturity, coupon_rate, face_value)

    # Price from YTM
    price = price_from_ytm(settlement, cfs, ytm_guess)

    # Back out YTM from that price
    calc_ytm = ytm_from_price(settlement, cfs, price)

    results.append({
        "settlement": row["settlement"],
        "maturity": row["maturity"],
        "coupon_rate": coupon_rate,
        "face_value": face_value,
        "ytm_input": ytm_guess,
        "price": round(price, 2),
        "ytm_output": round(calc_ytm * 100, 2)
    })

# Save results to CSV
df_out = pd.DataFrame(results)
df_out.to_csv("output.csv", index=False)

print("✅ Bond pricing completed. Results saved to output.csv")

