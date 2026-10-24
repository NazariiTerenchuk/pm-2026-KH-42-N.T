"""Monte Carlo прогноз кількості спринтів за історією velocity (ЛР9, слайд 21 L5).

Приклад:
  python lr09_forecast/simulate.py <velocity.csv> <points> [номери спринтів через кому]
"""
import csv
import math
import random
import sys

SIMULATIONS = 10000
MAX_SPRINTS = 1000
SEED = 42


def load_velocity(path, only=None):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if only:
        rows = [r for r in rows if int(r["sprint"]) in only]
    return [float(r["points_done"]) for r in rows]


def simulate(velocity, remaining, simulations=SIMULATIONS, seed=SEED):
    rng = random.Random(seed)
    results = []
    for _ in range(simulations):
        left, sprints = remaining, 0
        while left > 0 and sprints < MAX_SPRINTS:
            left -= rng.choice(velocity)
            sprints += 1
        results.append(sprints)
    results.sort()
    return results


def percentile(sorted_results, p):
    index = math.ceil(p * len(sorted_results)) - 1
    return math.ceil(sorted_results[index])


if __name__ == "__main__":
    path, points = sys.argv[1], float(sys.argv[2])
    only = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
    velocity = load_velocity(path, only)
    results = simulate(velocity, points)
    p50, p85 = percentile(results, 0.5), percentile(results, 0.85)
    print("velocity:", velocity, "середня: %.1f" % (sum(velocity) / len(velocity)))
    print("points: %g, прогонів: %d" % (points, len(results)))
    print("P50: %d, P85: %d, ширина: %d" % (p50, p85, p85 - p50))
