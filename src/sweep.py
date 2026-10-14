"""Day 11 — the sweep: battery size vs grid independence vs battery cost."""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt

from load_profile import build_hourly_load
from solar_profile import SOLAR_KWH
from battery import simulate

BATTERY_COST_PER_KWH = 50000   # Rs per kWh installed (residential LFP, India)


def main():
    load = build_hourly_load()
    solar = SOLAR_KWH

    sizes, independence, costs = [], [], []
    grid_only = simulate(load, solar, 0.0)[0].sum()   # baseline: no battery

    for kwh in range(0, 18, 2):        # 0, 2, 4, ... 16 kWh
        grid_needed, _ = simulate(load, solar, float(kwh))
        sizes.append(kwh)
        independence.append((1 - grid_needed.sum() / grid_only) * 100)
        costs.append(kwh * BATTERY_COST_PER_KWH)

    results = pd.DataFrame({
        "battery_kwh": sizes,
        "independence_pct": independence,
        "battery_cost_rs": costs,
    })
    print(results.to_string(index=False))
    print(f"\nSweet spot: where another 2 kWh buys less than 5 extra independence points")

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(sizes, independence, "o-", color="#4c72b0", label="grid independence %")
    ax1.set_xlabel("battery size (kWh)")
    ax1.set_ylabel("independence (%)", color="#4c72b0")
    ax2 = ax1.twinx()                                  # SECOND y-axis: cost!
    ax2.plot(sizes, costs, "s--", color="#c44e52", label="battery cost (Rs)")
    ax2.set_ylabel("cost (Rs)", color="#c44e52")
    ax1.set_title("The battery trade-off: independence vs cost")
    ax1.axvline(10, color="grey", linestyle=":", alpha=0.7)   # our sweet spot, marked
    fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.88))
    fig.savefig("plots/battery_sweep.png", dpi=150, bbox_inches="tight")
    print("Saved: plots/battery_sweep.png")


if __name__ == "__main__":
    main()
