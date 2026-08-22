#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  CHARLOTTE ULTRA — SWARM INTELLIGENCE ENGINE                   ║
║  Copyright © 2026 Tom Jeziorski. All Rights Reserved.           ║
║  TRADE SECRET — Unauthorized use strictly prohibited.           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import hashlib
import math
import random
import time
import uuid
from datetime import datetime, timedelta

AGENT_ROLES = ["scout", "worker", "validator", "coordinator", "harvester", "sentinel"]

DEFAULT_STRATEGIES = [
    "arbitrage_scan",
    "bonus_hunt",
    "cashback_grid",
    "flip_scout",
    "grant_monitor",
    "crypto_yield",
    "freelance_bid",
    "data_harvest",
]


def _seed_from(*parts) -> int:
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


class OrbitSwarm:
    """Distributed multi-agent coordination engine (simulated)."""

    def __init__(self):
        self.max_agents = 256
        self.communication_protocol = "mesh"
        self.consensus_algorithm = "byzantine_fault_tolerant"
        self.swarm_id = str(uuid.uuid4())
        self.active_swarms = {}
        self.created_at = datetime.utcnow().isoformat()
        self.total_tasks_dispatched = 0
        self.total_decisions_made = 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _generate_mesh_topology(self, agent_count, rng):
        """Generate a simple mesh adjacency description."""
        edges = min(agent_count * 3, agent_count * (agent_count - 1) // 2) if agent_count > 1 else 0
        return {
            "topology_type": "full_mesh" if agent_count <= 8 else "partial_mesh",
            "node_count": agent_count,
            "edge_count": edges,
            "avg_hop_distance": round(math.log2(agent_count) if agent_count > 1 else 1.0, 2),
            "redundant_paths": rng.randint(1, 5),
        }

    def _genetic_step(self, generation, rng):
        """Simulate one generation of a genetic algorithm."""
        base_fitness = 1 - math.exp(-generation / 25.0)
        noise = rng.uniform(-0.03, 0.03)
        fitness = round(min(0.999, max(0.05, base_fitness + noise)), 4)
        return fitness

    def _pheromone_decay(self, distance, evaporation_rate):
        """Ant colony optimization pheromone strength calculation."""
        return math.exp(-evaporation_rate * distance)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def spawn_swarm(self, task, agent_count=16):
        agent_count = max(1, min(agent_count, self.max_agents))
        seed = _seed_from("spawn", task, agent_count, time.time())
        rng = random.Random(seed)

        swarm_id = str(uuid.uuid4())
        agents = []
        for i in range(agent_count):
            agent_id = f"agent-{swarm_id[:8]}-{i:04d}"
            agents.append({
                "id": agent_id,
                "role": rng.choice(AGENT_ROLES),
                "status": rng.choice(["idle", "working", "syncing"]),
                "assigned_subtask": f"{task}::subtask_{i}",
                "cpu_alloc_pct": round(rng.uniform(5, 40), 2),
            })

        mesh_topology = self._generate_mesh_topology(agent_count, rng)
        communication_channels = [
            f"channel-{c}" for c in rng.sample(
                ["broadcast", "gossip", "direct", "relay", "multicast"], k=min(3, 5)
            )
        ]
        eta_minutes = round(rng.uniform(2, 90), 1)
        estimated_completion = (datetime.utcnow() + timedelta(minutes=eta_minutes)).isoformat()

        record = {
            "swarm_id": swarm_id,
            "task": task,
            "agents": agents,
            "mesh_topology": mesh_topology,
            "communication_channels": communication_channels,
            "estimated_completion": estimated_completion,
            "spawned_at": datetime.utcnow().isoformat(),
        }
        self.active_swarms[swarm_id] = record
        self.total_tasks_dispatched += 1
        return record

    def collective_decision(self, options, criteria=None):
        if not options:
            options = ["hold", "escalate", "retry"]
        criteria = criteria or ["cost", "speed", "reliability"]
        seed = _seed_from("decision", tuple(options), tuple(criteria), time.time())
        rng = random.Random(seed)

        num_agents = rng.randint(9, 33)  # odd count favors BFT quorum
        votes = {opt: 0 for opt in options}
        agent_votes = []
        for i in range(num_agents):
            choice = rng.choices(options, weights=[rng.uniform(0.5, 2.0) for _ in options])[0]
            votes[choice] += 1
            agent_votes.append({"agent_id": f"voter-{i:03d}", "vote": choice})

        winning_option = max(votes, key=votes.get)
        total_votes = sum(votes.values()) or 1
        confidence = round(votes[winning_option] / total_votes, 4)
        dissenting_agents = [v["agent_id"] for v in agent_votes if v["vote"] != winning_option]
        byzantine_quorum = math.floor((2 * num_agents) / 3) + 1
        consensus_round = 1 if votes[winning_option] >= byzantine_quorum else rng.randint(2, 4)

        self.total_decisions_made += 1

        return {
            "winning_option": winning_option,
            "vote_distribution": votes,
            "confidence": confidence,
            "dissenting_agents": dissenting_agents,
            "consensus_round": consensus_round,
            "quorum_required": byzantine_quorum,
            "total_voters": num_agents,
        }

    def distributed_earn(self, strategies=None):
        strategies = strategies or DEFAULT_STRATEGIES
        seed = _seed_from("earn", tuple(strategies), int(time.time() // 60))
        rng = random.Random(seed)

        results = {}
        for strategy in strategies:
            strat_seed = _seed_from(strategy, seed)
            strat_rng = random.Random(strat_seed)
            assigned_agents = strat_rng.randint(2, 24)
            projected_hourly = round(strat_rng.uniform(1.5, 85.0), 2)
            efficiency_score = round(strat_rng.uniform(0.4, 0.98), 4)
            status = strat_rng.choice(["running", "queued", "scaling", "throttled"])
            results[strategy] = {
                "assigned_agents": assigned_agents,
                "projected_hourly": projected_hourly,
                "status": status,
                "efficiency_score": efficiency_score,
            }
        return results

    def mesh_network_status(self):
        seed = _seed_from("mesh_status", int(time.time() // 30))
        rng = random.Random(seed)
        node_count = rng.randint(8, self.max_agents)

        nodes = []
        for i in range(min(node_count, 20)):  # cap sample size in the report
            nodes.append({
                "node_id": f"node-{i:03d}",
                "latency_ms": round(rng.uniform(2, 180), 2),
                "bandwidth_mbps": round(rng.uniform(10, 1000), 1),
                "uptime_pct": round(rng.uniform(95.0, 99.999), 3),
            })

        total_throughput = round(sum(n["bandwidth_mbps"] for n in nodes), 2)
        return {
            "node_count_total": node_count,
            "node_sample": nodes,
            "total_throughput_mbps": total_throughput,
            "redundancy_factor": round(rng.uniform(1.5, 4.0), 2),
            "partition_tolerance": rng.choice(["high", "medium", "byzantine_resilient"]),
            "healing_capability": round(rng.uniform(0.7, 0.99), 4),
        }

    def swarm_optimize(self, target="earnings"):
        seed = _seed_from("optimize", target, int(time.time() // 45))
        rng = random.Random(seed)

        generations = rng.randint(15, 60)
        best_fitness = 0.0
        for g in range(generations):
            best_fitness = max(best_fitness, self._genetic_step(g, rng))

        population_size = rng.randint(50, 400)
        population_stats = {
            "population_size": population_size,
            "avg_fitness": round(best_fitness * rng.uniform(0.6, 0.9), 4),
            "diversity_index": round(rng.uniform(0.1, 0.8), 4),
        }
        mutation_rate = round(rng.uniform(0.01, 0.08), 4)
        crossover_points = rng.randint(1, 4)
        convergence_pct = round(min(99.9, best_fitness * 100), 2)

        return {
            "target": target,
            "generation": generations,
            "best_fitness": round(best_fitness, 4),
            "population_stats": population_stats,
            "mutation_rate": mutation_rate,
            "crossover_points": crossover_points,
            "convergence_pct": convergence_pct,
        }

    def pheromone_trail(self, task_type):
        seed = _seed_from("pheromone", task_type, int(time.time() // 20))
        rng = random.Random(seed)

        evaporation_rate = round(rng.uniform(0.05, 0.3), 4)
        num_nodes = rng.randint(4, 12)
        path = [f"waypoint-{i}" for i in range(num_nodes)]
        distances = [rng.uniform(0.5, 5.0) for _ in range(num_nodes - 1)]
        trail_strength = round(
            sum(self._pheromone_decay(d, evaporation_rate) for d in distances) / max(1, len(distances)), 4
        )
        discovery_rate = round(rng.uniform(0.1, 0.9), 4)

        return {
            "task_type": task_type,
            "trail_strength": trail_strength,
            "optimal_path": path,
            "discovery_rate": discovery_rate,
            "evaporation_rate": evaporation_rate,
        }

    def get_status(self):
        return {
            "swarm_id": self.swarm_id,
            "max_agents": self.max_agents,
            "communication_protocol": self.communication_protocol,
            "consensus_algorithm": self.consensus_algorithm,
            "active_swarms_count": len(self.active_swarms),
            "active_swarm_ids": list(self.active_swarms.keys()),
            "total_tasks_dispatched": self.total_tasks_dispatched,
            "total_decisions_made": self.total_decisions_made,
            "created_at": self.created_at,
        }
