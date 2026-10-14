# House Power Plant 🏡⚡
> Could my rooftop power my home? A 30-day Python energy modelling experiment.

## The question

We consume about ₹4,500–5,000 worth of electricity every month — paid via a
reminder on my mobile payment app, no questions asked. One day I finally asked one:
**could a rooftop solar PV plant power this house?**

Any PV design has to start from the consumption side: how much power do we
actually need? So I walked around the house counting appliances — and made
a discovery that reorganized my whole understanding of our bill: **a single
split AC consumes ~65% of everything our house draws.**

To size a PV system you need two numbers: the **maximum simultaneous power**
(which sizes panels and inverter) and the **average daily energy** (which
tells you whether the installation can meet the full day's needs). I built
an hourly model of both in Python — which brings us to the fun part.

## What I found

Four models, four answers. (Charts in `plots/`)

**1. The load: what does my house use?** (`src/load_profile.py`)
- **20.85 kWh/day** (~625 units/month) — which matches the bill: ₹4,500 ÷ 625 ≈ ₹7.2/unit, inside TNPDCL's real tariff range.
- The single split AC runs ~15 h/day and accounts for **~65% of total consumption**.
- Chart: `plots/load_profile.png` — the "AC mountain".

**2. The sun: can it deliver that much?** (`src/solar_profile.py`)
- A **5.2 kW** rooftop system generates **~20.8 kWh/day** — almost exactly what the house needs.
- But only **15% is used directly**: the sun peaks at noon; the AC mountain rises at night. Same energy, ten hours apart.
- With net metering, exports by day cancel imports by night: **net grid purchase ≈ 0**.
- Chart: `plots/solar_vs_load.png`

**3. The money: is it worth it?** (`src/money.py`)
- Bill: **₹4,503 → ₹510/month** (savings ~₹3,993/month)
- System: ₹2.86 lakh gross − ₹1 lakh subsidies (PM Surya Ghar + TN top-up) = **₹1.86 lakh net**
- **Payback: ~4.1 years**, then ~20 years of essentially free power.

**4. The battery: can I be independent?** (`src/battery.py`, `src/sweep.py`)
- Independence rises linearly at **~9.5% per kWh of battery** — until a cliff.
- **10 kWh → 95% independence (the sweet spot)**; 12 kWh → 100% (minimum for off-grid); beyond that, money buys nothing.
- Chart: `plots/battery_sweep.png` — the trade-off curve.

**Bottom line:** the sun can power this house. Net-metered solar pays for itself in ~4 years; add a ~10 kWh battery and the grid becomes optional.
## Honest limitations

This is an indicative model, not a quote. Real output would differ because:

- **One average day, repeated.** The model simulates a single typical day, every
  day. Real Chennai Decembers (northeast monsoon) generate ~30% less; the
  battery is also assumed to start each day fully charged.
- **Roof area & orientation not measured.** 5.2 kW needs roughly 350–400 sq ft
  of shadow-free roof facing (ideally) south. That's the first thing a site
  survey would check.
- **Simplified sun curve.** A sine bell, not pvlib's real sun-position maths —
  good enough for sizing, not for hour-level guarantees.
- **Tariff blended, not slabbed.** ₹7.2/unit is the validated average; the
  actual TNPDCL bill is telescopic slabs, so savings near slab edges shift a bit.
- **I'm a renter.** The consumer number (and net-metering subsidy) belongs to
  the owner — the numbers here are the pitch I'd take to them, not a plan I
  can execute alone.

## Run it yourself

Clone the repo, create a virtual environment, install the three libraries,
and run the five models in order. Every chart lands in `plots/`. Change the
constants at the top of any file (AC hours, system kW, battery size, tariff)
and re-run to model your own house.

---

*Built over 30 days in October 2026. Start a Terminal, keep asking what the bill buys.*
