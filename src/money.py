"""Day 9 — the money view: bill before/after solar, payback years."""
from load_profile import build_hourly_load
from solar_profile import SOLAR_KWH, SYSTEM_KW

TARIFF = 7.2            # Rs per kWh blended (validated on Day 4)
COST_PER_KW = 55000     # Rs per kW installed, grid-tied
SUBSIDY = 100000        # Rs: PM Surya Ghar 78k + TN top-up 22k (3kW+)
O_AND_M = 3000          # Rs/year maintenance (cleaning, inverter wear)


def main():
    load = build_hourly_load()
    solar = SOLAR_KWH

    daily_load = load.sum()
    daily_solar = solar.sum()
    net_grid = max(daily_load - daily_solar, 0)     # units to buy, after export credit

    bill_now = daily_load * 30 * TARIFF
    bill_solar = net_grid * 30 * TARIFF + 500        # + fixed/minimum charges
    savings = bill_now - bill_solar

    gross_cost = SYSTEM_KW * COST_PER_KW
    net_cost = gross_cost - SUBSIDY
    payback = net_cost / max(savings * 12 - O_AND_M, 1)   # FIX: yearly savings, yearly O&M

    print(f"Monthly bill today:      Rs {bill_now:,.0f}")
    print(f"Monthly bill with solar: Rs {bill_solar:,.0f}")
    print(f"Monthly savings:         Rs {savings:,.0f}")
    print(f"System cost (gross):     Rs {gross_cost:,.0f}")
    print(f"System cost (net of subsidy): Rs {net_cost:,.0f}")
    print(f"Payback: {payback:.1f} years, then ~20 more years free")


if __name__ == "__main__":
    main()
