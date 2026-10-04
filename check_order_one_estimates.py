#!/usr/bin/env python3
"""High-precision sanity checks for the accompanying analytic proof.

Requires mpmath. Run:
    python3 check_order_one_estimates.py

These checks do not prove the infinite statements and are not interval
arithmetic. The manuscript supplies the proofs independently of this script.
"""

import argparse
import json
from pathlib import Path

import mpmath as mp

mp.mp.dps = 90
SHIFT = mp.exp(mp.e)


def weight(t):
    logarithm = mp.log(mp.mpf(t) + SHIFT)
    return logarithm * mp.log(logarithm)


def derivative_majorant(n, radius, relative_tolerance=mp.mpf("1e-65")):
    """Return a partial sum and a geometric upper bound for its remainder.

    For this particular weight, r*w(n+k)/k decreases in k. Indeed, with
    L = log(n+k+SHIFT) >= e and l = log(L) >= 1,
    k*w'(n+k) <= l+1 < L*l = w(n+k).
    Thus when the next ratio q is below 1, the remaining sum is bounded
    by the next term divided by 1-q.
    """
    if radius == 0:
        return mp.mpf(1), mp.mpf(0), 0, {}
    current = mp.mpf(1)
    total = current
    terms = {0: current}
    for k in range(100000):
        next_ratio = radius * weight(n + k + 1) / (k + 1)
        next_term = current * next_ratio
        if next_ratio < 1:
            tail_bound = next_term / (1 - next_ratio)
            if tail_bound < relative_tolerance * total:
                return total, tail_bound, k, terms
        current = next_term
        terms[k + 1] = current
        total += current
    raise RuntimeError("Failed to bound the majorant tail")


def stringify(x):
    return mp.nstr(x, 16)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Optionally save the report")
    args = parser.parse_args()
    rows = []
    peak_checks = 0
    majorant_checks = 0
    for n in (4, 16, 64, 256, 1024, 4096, 100000000):
        wn = weight(n)
        for r_text in ("0", "0.001", "0.02", "0.1", "0.5", "1", "2", "4"):
            r = mp.mpf(r_text)
            partial, tail, last_k, terms = derivative_majorant(n, r)
            upper_sum = partial + tail
            row = {
                "n": n,
                "radius": r_text,
                "weight": stringify(wn),
                "terms_through_k": last_k,
                "relative_tail_bound": stringify(tail / partial),
            }
            t = r * wn
            if t >= 1:
                m = int(mp.floor(t))
                # The manuscript's estimate uses B(n,m) >= W(n)^m.
                frozen_term = mp.power(t, m) / mp.factorial(m)
                claimed_lower_bound = mp.exp(t) / (mp.e**2 * t)
                if not frozen_term >= claimed_lower_bound:
                    raise AssertionError((n, r_text, "factorial peak inequality"))
                # Check the actual derivative coefficient as well.
                if m not in terms:
                    log_actual = mp.fsum(mp.log(weight(n + j)) for j in range(1, m + 1))
                    actual = mp.exp(log_actual) * mp.power(r, m) / mp.factorial(m)
                else:
                    actual = terms[m]
                if not actual >= frozen_term:
                    raise AssertionError((n, r_text, "monotone coefficient inequality"))
                peak_checks += 1
                row["peak_index"] = m
                row["log_peak_bound_margin"] = stringify(mp.log(frozen_term / claimed_lower_bound))
            # This sufficient condition ensures the manuscript's tail estimate
            # for every k > n. The function w(2k)/k decreases by the same
            # derivative calculation used above.
            cutoff = mp.e * r * weight(2 * (n + 1)) / (n + 1)
            eligible = cutoff <= mp.mpf("0.5")
            row["upper_bound_cutoff_holds"] = bool(eligible)
            if eligible:
                claimed_upper = mp.exp(r * weight(2 * n)) + mp.power(2, -n)
                if not upper_sum <= claimed_upper * (1 + mp.mpf("1e-60")):
                    raise AssertionError((n, r_text, "derivative majorant inequality"))
                majorant_checks += 1
                row["log_majorant_bound_margin"] = stringify(mp.log(claimed_upper / upper_sum))
            if r > 0:
                row["log_majorant_divided_by_r_weight"] = stringify(mp.log(upper_sum) / t)
            rows.append(row)
    report = {
        "purpose": "Finite high-precision sanity checks; the proof is analytic",
        "decimal_precision": mp.mp.dps,
        "cases": len(rows),
        "peak_inequalities_checked": peak_checks,
        "majorant_inequalities_checked_when_sufficient_cutoff_holds": majorant_checks,
        "result": "PASS",
        "rows": rows,
    }
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))
    print("Example normalized majorants for radius 1:")
    for row in rows:
        if row["radius"] == "1":
            print(f"n={row['n']:>9}, log(S_n)/(W_n)={row['log_majorant_divided_by_r_weight']}")


if __name__ == "__main__":
    main()
