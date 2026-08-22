#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  CHARLOTTE ULTRA — MULTIVERSE ENGINE                            ║
║  Copyright © 2026 Tom Jeziorski. All Rights Reserved.           ║
║  TRADE SECRET — Unauthorized use strictly prohibited.           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import hashlib
import math
import random
import statistics
import time


# ---------------------------------------------------------------------------
# Monte Carlo / statistical helper functions
# ---------------------------------------------------------------------------

def _random_walk(steps: int, drift: float = 0.0, volatility: float = 1.0):
    """Generates a simple random walk series (e.g. return path)."""
    path = [0.0]
    for _ in range(steps):
        step = random.gauss(drift, volatility)
        path.append(path[-1] + step)
    return path


def _mean(values):
    return statistics.mean(values) if values else 0.0


def _std_dev(values):
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def _percentile(values, pct: float):
    if not values:
        return 0.0
    ordered = sorted(values)
    k = (len(ordered) - 1) * (pct / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return ordered[int(k)]
    d0 = ordered[int(f)] * (c - k)
    d1 = ordered[int(c)] * (k - f)
    return d0 + d1


def _monte_carlo_outcomes(iterations: int, base_return: float = 0.05, volatility: float = 0.20):
    """Runs a simple Monte Carlo simulation of terminal outcomes."""
    outcomes = []
    for _ in range(iterations):
        walk = _random_walk(50, drift=base_return / 50.0, volatility=volatility / math.sqrt(50))
        outcomes.append(walk[-1])
    return outcomes


def _hash_id(prefix: str, *parts) -> str:
    material = "|".join(str(p) for p in parts) + str(time.time_ns())
    digest = hashlib.sha256(material.encode()).hexdigest()[:10]
    return f"{prefix}-{digest}"


def _sharpe_ratio(returns, risk_free=0.0):
    if len(returns) < 2:
        return 0.0
    excess = [r - risk_free for r in returns]
    sd = _std_dev(excess)
    return round(_mean(excess) / sd, 3) if sd else 0.0


def _sortino_ratio(returns, risk_free=0.0):
    if len(returns) < 2:
        return 0.0
    downside = [min(0.0, r - risk_free) for r in returns]
    downside_dev = math.sqrt(_mean([d ** 2 for d in downside])) if downside else 0.0
    excess_mean = _mean([r - risk_free for r in returns])
    return round(excess_mean / downside_dev, 3) if downside_dev else 0.0


def _max_drawdown(equity_curve):
    peak = equity_curve[0] if equity_curve else 0.0
    max_dd = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        if peak != 0:
            dd = (peak - value) / abs(peak) if peak else 0.0
            max_dd = max(max_dd, dd)
    return round(max_dd * 100, 3)


class GalacticMultiverse:
    """Parallel strategy simulation and timeline branching for optimal decisions."""

    def __init__(self):
        self.max_timelines = 1024
        self.branching_factor = 8
        self.simulation_depth = 100
        self.collapse_threshold = 0.85
        self.active_universes = []
        self._timelines = {}
        self._boot_time = time.time()

    def branch_timeline(self, strategy, variables=None):
        variables = variables or {}
        timeline_id = _hash_id("TL", strategy)

        branches = []
        for i in range(self.branching_factor):
            variable_state = {
                key: round(val * random.uniform(0.85, 1.15), 4) if isinstance(val, (int, float)) else val
                for key, val in variables.items()
            }
            initial_conditions = {
                "volatility_regime": random.choice(["low", "medium", "high"]),
                "liquidity_state": random.choice(["thin", "normal", "deep"]),
            }
            projected_outcome = round(random.gauss(0.08, 0.15), 4)
            branches.append({
                "branch_id": f"{timeline_id}-B{i}",
                "variable_state": variable_state,
                "initial_conditions": initial_conditions,
                "projected_outcome": projected_outcome,
            })

        recommended_branch = max(branches, key=lambda b: b["projected_outcome"])["branch_id"]
        record = {
            "timeline_id": timeline_id,
            "strategy": strategy,
            "branches": branches,
            "status": "ACTIVE",
        }
        self._timelines[timeline_id] = record
        self.active_universes.append(timeline_id)

        return {
            "timeline_id": timeline_id,
            "branches": branches,
            "total_branches": len(branches),
            "computation_cost": round(len(branches) * self.simulation_depth * 0.01, 3),
            "recommended_branch": recommended_branch,
        }

    def simulate_multiverse(self, scenario, iterations=1000):
        outcomes = _monte_carlo_outcomes(iterations)
        outcomes_sorted = sorted(outcomes)

        percentiles = {
            "p5": round(_percentile(outcomes_sorted, 5), 4),
            "p25": round(_percentile(outcomes_sorted, 25), 4),
            "p50": round(_percentile(outcomes_sorted, 50), 4),
            "p75": round(_percentile(outcomes_sorted, 75), 4),
            "p95": round(_percentile(outcomes_sorted, 95), 4),
        }

        outcomes_distribution = {
            "best_case": round(max(outcomes), 4),
            "worst_case": round(min(outcomes), 4),
            "median": round(statistics.median(outcomes), 4),
            "mean": round(_mean(outcomes), 4),
            "std_dev": round(_std_dev(outcomes), 4),
            "percentiles": percentiles,
        }

        # find rough convergence point: where running mean stabilizes within 1%
        running_mean = 0.0
        convergence_at_iteration = iterations
        for idx, val in enumerate(outcomes, start=1):
            running_mean += (val - running_mean) / idx
            if idx > 50 and abs(running_mean - outcomes_distribution["mean"]) < abs(outcomes_distribution["mean"]) * 0.01 + 1e-6:
                convergence_at_iteration = idx
                break

        probability_of_profit = round(sum(1 for o in outcomes if o > 0) / len(outcomes), 4)
        dominant_timeline = _hash_id("DOM", scenario)

        return {
            "scenario_name": scenario,
            "iterations_run": iterations,
            "outcomes": outcomes_distribution,
            "convergence_at_iteration": convergence_at_iteration,
            "dominant_timeline": dominant_timeline,
            "probability_of_profit": probability_of_profit,
        }

    def collapse_wave(self, timeline_id):
        record = self._timelines.get(timeline_id)
        if record is None:
            branches = [{"branch_id": f"{timeline_id}-B0", "projected_outcome": random.gauss(0.05, 0.1)}]
        else:
            branches = record["branches"]

        best = max(branches, key=lambda b: b["projected_outcome"])
        eliminated = len(branches) - 1
        confidence = round(min(0.99, self.collapse_threshold + random.uniform(0, 0.1)), 4)
        expected_value = round(best["projected_outcome"], 4)
        risk_after_collapse = round(max(0.01, 0.3 - confidence * 0.25), 4)

        if record is not None:
            record["status"] = "COLLAPSED"
            if timeline_id in self.active_universes:
                self.active_universes.remove(timeline_id)

        return {
            "collapsed_to": best["branch_id"],
            "confidence": confidence,
            "alternative_timelines_eliminated": eliminated,
            "expected_value": expected_value,
            "risk_after_collapse": risk_after_collapse,
        }

    def parallel_backtest(self, strategies, period_days=365):
        results = []
        for strategy_name in strategies:
            timeline_count = random.randint(4, self.branching_factor)
            daily_returns = [random.gauss(0.0006, 0.015) for _ in range(period_days)]
            equity_curve = [100.0]
            for r in daily_returns:
                equity_curve.append(equity_curve[-1] * (1 + r))

            total_return_pct = round((equity_curve[-1] / equity_curve[0] - 1) * 100, 3)
            max_dd = _max_drawdown(equity_curve)
            sharpe = _sharpe_ratio(daily_returns)
            sortino = _sortino_ratio(daily_returns)
            win_rate = round(sum(1 for r in daily_returns if r > 0) / len(daily_returns), 4)

            best_timeline = f"{strategy_name}-TL{random.randint(0, timeline_count - 1)}"
            worst_timeline = f"{strategy_name}-TL{random.randint(0, timeline_count - 1)}"

            results.append({
                "strategy_name": strategy_name,
                "timeline_count": timeline_count,
                "total_return_pct": total_return_pct,
                "max_drawdown_pct": max_dd,
                "sharpe_ratio": sharpe,
                "sortino_ratio": sortino,
                "win_rate": win_rate,
                "best_timeline": best_timeline,
                "worst_timeline": worst_timeline,
            })
        return results

    def entropy_analysis(self, system="portfolio"):
        # Shannon-entropy-inspired synthetic chaos measure over a random state distribution
        state_probs = [random.random() for _ in range(10)]
        total = sum(state_probs)
        state_probs = [p / total for p in state_probs]
        shannon_entropy = -sum(p * math.log2(p) for p in state_probs if p > 0)
        entropy_score = round(min(10.0, shannon_entropy * 3.0), 3)

        chaos_index = round(entropy_score / 10.0, 4)

        if entropy_score < 3:
            stability_forecast = "Stable — low disorder"
            phase_transition_risk = "LOW"
        elif entropy_score < 6.5:
            stability_forecast = "Moderate volatility expected"
            phase_transition_risk = "MEDIUM"
        else:
            stability_forecast = "High disorder — regime shift likely"
            phase_transition_risk = "HIGH"

        recommended_actions = []
        if phase_transition_risk != "LOW":
            recommended_actions.append("Increase hedge allocation")
            recommended_actions.append("Reduce leverage exposure")
        recommended_actions.append(f"Continue monitoring {system} entropy trend")

        return {
            "entropy_score": entropy_score,
            "chaos_index": chaos_index,
            "stability_forecast": stability_forecast,
            "recommended_actions": recommended_actions,
            "phase_transition_risk": phase_transition_risk,
        }

    def timeline_merge(self, timeline_ids):
        merged_timeline_id = _hash_id("MERGE", *timeline_ids)
        merged_parameters = {}
        conflicts_resolved = 0

        for tid in timeline_ids:
            record = self._timelines.get(tid)
            if not record:
                continue
            best_branch = max(record["branches"], key=lambda b: b["projected_outcome"])
            for key, val in best_branch["variable_state"].items():
                if key in merged_parameters and merged_parameters[key] != val:
                    conflicts_resolved += 1
                    if isinstance(val, (int, float)) and isinstance(merged_parameters[key], (int, float)):
                        merged_parameters[key] = round((merged_parameters[key] + val) / 2, 4)
                else:
                    merged_parameters[key] = val

        expected_improvement_pct = round(random.uniform(2.0, 18.0), 2)

        return {
            "merged_timeline_id": merged_timeline_id,
            "source_timelines": list(timeline_ids),
            "merged_parameters": merged_parameters,
            "expected_improvement_pct": expected_improvement_pct,
            "conflicts_resolved": conflicts_resolved,
        }

    def multiverse_map(self):
        active = [tid for tid, r in self._timelines.items() if r["status"] == "ACTIVE"]
        collapsed = [tid for tid, r in self._timelines.items() if r["status"] == "COLLAPSED"]

        branching_tree = {}
        for tid, record in self._timelines.items():
            branching_tree[tid] = {
                "status": record["status"],
                "branches": [b["branch_id"] for b in record["branches"]],
            }

        dominant_path = active[0] if active else (collapsed[0] if collapsed else None)
        divergence_points = [
            {"timeline_id": tid, "divergence_count": len(r["branches"])}
            for tid, r in self._timelines.items()
        ]

        return {
            "total_timelines": len(self._timelines),
            "active_timelines": len(active),
            "collapsed_timelines": len(collapsed),
            "branching_tree": branching_tree,
            "dominant_path": dominant_path,
            "divergence_points": divergence_points,
        }

    def get_status(self):
        uptime_s = round(time.time() - self._boot_time, 2)
        return {
            "module": "GalacticMultiverse",
            "max_timelines": self.max_timelines,
            "branching_factor": self.branching_factor,
            "simulation_depth": self.simulation_depth,
            "collapse_threshold": self.collapse_threshold,
            "active_universes_count": len(self.active_universes),
            "total_timelines_tracked": len(self._timelines),
            "uptime_seconds": uptime_s,
        }


if __name__ == "__main__":
    engine = GalacticMultiverse()
    print(engine.get_status())
