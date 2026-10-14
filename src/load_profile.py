"""Sudhakar's house — hourly load profile (validated v2)."""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt

# MY house's real appliances, in watts
APPLIANCE_WATTS = {
    "fridge": 150, "lights": 54, "fans": 225, "tv": 100,
    "laptops": 195, "geyser": 2000, "router": 10, "ac": 2000,
    "kettle": 2000, "washing_machine": 500,
}

# When each appliance runs: {hour: fraction of the hour it's ON}
APPLIANCE_SCHEDULE = {
    "fridge": {h: 0.30 for h in range(24)},                          # 2-3 yr old, cycles
    "lights": {h: 1.0 for h in range(18, 23)},                       # 6 LED bulbs, 6-11pm
    "fans": {h: 1.0 for h in list(range(0, 4)) + list(range(18, 24))},  # 3 fans, ~10h
    "tv": {h: 1.0 for h in range(19, 23)},
    "laptops": {h: 1.0 for h in range(9, 18)},                      # 3 laptops, work hours
    "geyser": {6: 0.5},                                              # 6am, 30 min
    "router": {h: 1.0 for h in range(24)},
    "ac": {h: 0.45 for h in list(range(17, 24)) + list(range(0, 8))},  # 5pm-8am, thermostat cycles
    "kettle": {7: 0.1},                                              # ~6 min/day
    "washing_machine": {10: 0.3},                                    # 3-4 loads/week, averaged
}


def build_hourly_load():
    load = pd.Series(0.0, index=range(24), name="load_kwh")
    for appliance, schedule in APPLIANCE_SCHEDULE.items():
        for hour, fraction in schedule.items():
            load[hour] += APPLIANCE_WATTS[appliance] * fraction / 1000.0
    return load


def main():
    load = build_hourly_load()
    print(f"Daily total: {load.sum():.2f} kWh")
    print(f"Evening peak (6-10pm): {load[18:22].sum():.2f} kWh")
    print(f"Monthly estimate: {load.sum() * 30:.0f} units (kWh)")
    ax = load.plot(kind="bar", title="Sudhakar's house: hourly electricity use",
                   ylabel="kWh", xlabel="hour of day")
    ax.figure.savefig("plots/load_profile.png", dpi=150, bbox_inches="tight")
    print("Saved: plots/load_profile.png")


if __name__ == "__main__":
    main()
