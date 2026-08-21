---
type: platform
verified: 2026-08-12
---
# Two small ones that cause big errors

**Multi-currency portals: always use `amount_in_home_currency`.**
Summing raw `amount` mixes currencies silently. A ZAR renewal counted as £323k and
overstated an entire event attribution report. The deal *counts* were right the whole
time; only the values were wrong, which is exactly why nobody spotted it.

**Custom code steps die at 20 seconds.**
Measured 15.7s on a real event attribution run, which is too close. Split into two
sequential code steps rather than optimising and hoping.
