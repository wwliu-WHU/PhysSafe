import numpy as np

def episode_has_any(flag_arr: np.ndarray) -> bool:
    return bool(np.any(flag_arr.astype(np.uint8) > 0))

def compute_episode_flags(ep_group) -> dict:
    """Read one episode group and return event flags + success + auxiliary signals."""
    coll = ep_group["events/collision_flag"][()]
    fall = ep_group["events/fall_flag"][()]
    fvio = ep_group["events/force_violation_flag"][()]
    nmiss = ep_group["events/near_miss_flag"][()]

    intervention = ep_group["safety/intervention"][()] if "safety/intervention" in ep_group else np.zeros_like(coll)
    margin = ep_group["safety/margin_dist"][()] if "safety/margin_dist" in ep_group else np.zeros_like(coll, dtype=np.float32)

    has_collision = episode_has_any(coll)
    has_fall = episode_has_any(fall)
    has_violation = has_collision or has_fall or episode_has_any(fvio) or episode_has_any(nmiss)

    if "meta/success" in ep_group:
        success = bool(ep_group["meta/success"][()][0])
    else:
        success = (not has_fall)

    return {
        "has_collision": has_collision,
        "has_fall": has_fall,
        "has_violation": has_violation,
        "success": success,
        "interventions": int(np.sum(intervention.astype(np.uint8))),
        "steps": int(coll.shape[0]),
        "avg_margin": float(np.mean(margin)),
    }

def aggregate_metrics(per_episode: list[dict], dt: float) -> dict:
    N = max(len(per_episode), 1)
    coll_cnt = sum(int(e["has_collision"]) for e in per_episode)
    fall_cnt = sum(int(e["has_fall"]) for e in per_episode)
    viol_cnt = sum(int(e["has_violation"]) for e in per_episode)
    succ_cnt = sum(int(e["success"]) for e in per_episode)

    total_interventions = sum(e["interventions"] for e in per_episode)
    total_steps = sum(e["steps"] for e in per_episode)
    margin_sum = sum(e["avg_margin"] for e in per_episode)

    total_time_min = (total_steps * dt) / 60.0

    return {
        "collision_rate": coll_cnt / N,
        "fall_rate": fall_cnt / N,
        "safety_violation_rate": viol_cnt / N,
        "task_success_rate": succ_cnt / N,
        "intervention_rate_per_min": (total_interventions / max(total_time_min, 1e-9)),
        "avg_safety_margin_m": margin_sum / N,
    }
