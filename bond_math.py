import numpy as np
from datetime import datetime

# Function 1: Calculate year fraction between two dates (simple ACT/365)
def year_fraction(start_date, end_date):
    days = (end_date - start_date).days
    return days / 365.0

# Function 2: Create bond cashflows
def generate_cashflows(settlement, maturity, coupon_rate, face_value=100, freq=2):
    """
    settlement : date when you buy bond (datetime)
    maturity   : maturity date (datetime)
    coupon_rate: annual coupon rate (e.g., 0.05 for 5%)
    face_value : usually 100
    freq       : number of coupon payments per year (2 = semi-annual)
    """
    cashflows = []
    coupon = face_value * coupon_rate / freq
    
    # number of payments
    n_periods = int((maturity.year - settlement.year) * freq)
    
    for i in range(1, n_periods + 1):
        pay_date = settlement.replace(year=settlement.year) + \
                   (maturity - settlement) * i / n_periods
        if i == n_periods:  # last payment includes principal
            cashflows.append((pay_date, coupon + face_value))
        else:
            cashflows.append((pay_date, coupon))
    return cashflows

# Function 3: Price a bond given YTM
def price_from_ytm(settlement, cashflows, ytm, freq=2):
    price = 0
    for pay_date, cf in cashflows:
        t = year_fraction(settlement, pay_date)
        price += cf / (1 + ytm/freq)**(t*freq)
    return price

# Function 4: Yield to Maturity (solve by trial)
def ytm_from_price(settlement, cashflows, market_price, freq=2):
    def f(ytm):
        return price_from_ytm(settlement, cashflows, ytm, freq) - market_price
    
    low, high = 0.0, 1.0  # search between 0% and 100%
    for _ in range(100):
        mid = (low + high) / 2
        if f(mid) > 0:
            low = mid
        else:
            high = mid
    return mid

# Example usage
if __name__ == "__main__":
    settlement = datetime(2023, 9, 1)
    maturity = datetime(2028, 9, 1)
    coupon_rate = 0.05   # 5% coupon
    face_value = 100

    cfs = generate_cashflows(settlement, maturity, coupon_rate, face_value)
    price = price_from_ytm(settlement, cfs, 0.06)  # assume 6% YTM
    ytm = ytm_from_price(settlement, cfs, price)

    print("Cashflows:", cfs)
    print("Price from 6% YTM:", round(price, 2))
    print("YTM from that price:", round(ytm*100, 2), "%")

