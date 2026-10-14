"""Day 10 — the battery: can stored sunshine run the AC mountain all night?"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt

from load_profile import build_hourly_load
from solar_profile import SOLAR_KWH

BATTERY_KWH = 10.0       # advertised capacity (typical residential LFP: 5-15 kWh)
USABLE_FRACTION = 0.85   # depth-of-discharge limit x round-trip efficiency
GRID_CAP = 5.0           # kW max charge/discharge power (plenty for a house)


def simulate(load, solar, battery_kwh):
    """One sample day: solar serves load, extra charges battery, night runs off battery."""
    usable = battery_kwh * USABLE_FRACTION
    stored = usable          # start the day fully charged (generous)
    grid_kwh = []            # units needed from grid each hour
    batt_flow = []           # battery discharge (+) / charge (-) each hour

    for hour in range(24):
        surplus = solar[hour] - load[hour]
        if surplus >= 0:                       # sun covers the house
            room = usable - stored
            charged = min(surplus, room, GRID_CAP)
            stored += charged
            batt_flow.append(-charged)
            grid_kwh.append(0.0)
        else:                                  # house needs more than the sun gives
            deficit = -surplus
            discharged = min(deficit, stored, GRID_CAP)
            stored -= discharged
            batt_flow.append(discharged)
            grid_kwh.append(deficit - discharged)

    return pd.Series(grid_kwh, index=range(24)), pd.Series(batt_flow, index=range(24))


def main():
    load = build_hourly_load()
    solar = SOLAR_KWH

    grid_with, flow = simulate(load, solar, BATTERY_KWH)
    grid_without, _ = simulate(load, solar, 0.0)

    print(f"Grid units needed, solar only:        {grid_without.sum():.2f} kWh/day")
    print(f"Grid units needed, solar + {BATTERY_KWH:.0f} kWh battery: {grid_with.sum():.2f} kWh/day")
    print(f"Battery cuts grid dependence by:      {(1 - grid_with.sum() / grid_without.sum()) * 100:.0f}%")

    fig, ax = plt.subplots(figsize=(11, 5))
    grid_without.plot(kind="bar", ax=ax, color="#c44e52", alpha=0.5, label="grid needed (no battery)")
    grid_with.plot(kind="bar", ax=ax, color="#4c72b0", label="grid needed (with battery)")
    ax.set_title(f"Blackout insurance: does a {BATTERY_KWH:.0f} kWh battery kill the night grid?")
    ax.set_xlabel("hour of day")
    ax.set_ylabel("kWh from grid")
    ax.legend()
    fig.savefig("plots/battery_effect.png", dpi=150, bbox_inches="tight")
    print("Saved: plots/battery_effect.png")


if __name__ == "__main__":
    main()
