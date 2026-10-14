"""Day 5 — the sun meets the mountain: solar generation vs. house load."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from load_profile import build_hourly_load

# --- Your rooftop solar system ---
SYSTEM_KW = 5.2            # sized on Day 4 to match your 20.85 kWh/day
PEAK_SUN_HOURS = 4.0       # Chennai annual average: 4 units per kW per day
DAILY_GENERATION = SYSTEM_KW * PEAK_SUN_HOURS   # = 20.8 kWh

# The sun's bell curve: sunrise ~6am, peak ~noon, sunset ~6pm
HOURS = np.arange(24)
SUN_SHAPE = np.where(
    (HOURS >= 6) & (HOURS <= 18),
    np.sin(np.pi * np.clip(HOURS - 6, 0, 12) / 12) ** 1.5,   # FIX: clip stops negative values
    0.0,
)
SOLAR_KWH = pd.Series(
    SUN_SHAPE / SUN_SHAPE.sum() * DAILY_GENERATION, index=HOURS, name="solar_kwh"
)


def main():
    load = build_hourly_load()
    solar = SOLAR_KWH

    direct = pd.concat([load, solar], axis=1)
    direct["solar_used"] = direct[["load_kwh", "solar_kwh"]].min(axis=1)
    used = direct["solar_used"].sum()
    surplus = solar.sum() - used
    unmet = load.sum() - used

    print(f"Daily load:        {load.sum():.2f} kWh")
    print(f"Daily solar:       {solar.sum():.2f} kWh")
    print(f"Solar used directly: {used:.2f} kWh ({used / load.sum() * 100:.0f}% of load)")
    print(f"Solar surplus (exported to grid): {surplus:.2f} kWh")
    print(f"Load unmet by solar (night): {unmet:.2f} kWh")

    net_bill_units = max(load.sum() - solar.sum(), 0)
    print(f"Units still bought from grid (net): {net_bill_units:.1f}/day ≈ {net_bill_units * 30:.0f}/month")

    fig, ax = plt.subplots(figsize=(11, 5))
    load.plot(kind="bar", ax=ax, color="#4c72b0", label="house load")
    solar.plot(ax=ax, color="#f5a623", linewidth=3, label="solar generation")
    ax.set_title("Sudhakar's house vs. 5.2 kW rooftop solar")
    ax.set_xlabel("hour of day")
    ax.set_ylabel("kWh")
    ax.legend()
    fig.savefig("plots/solar_vs_load.png", dpi=150, bbox_inches="tight")
    print("Saved: plots/solar_vs_load.png")


if __name__ == "__main__":
    main()
