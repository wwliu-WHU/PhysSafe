# evaluation/evaluate.py
import json, hashlib, argparse
import h5py
import numpy as np

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b: break
            h.update(b)
    return "sha256:" + h.hexdigest()

def episode_has_any(flag_arr: np.ndarray) -> bool:
    return bool(np.any(flag_arr.astype(np.uint8) > 0))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hdf5", required=True)
    ap.add_argument("--scenario_id", required=True)
    ap.add_argument("--level", required=True)
    ap.add_argument("--episodes", type=int, default=0, help="0 means all")
    ap.add_argument("--dt", type=float, default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--method", default="UnknownMethod")
    ap.add_argument("--policy_type", default="rl")
    ap.add_argument("--safety_layer", default="none")
    ap.add_argument("--scenario_yaml", default=None)
    ap.add_argument("--seeds_test", default="[]")
    args = ap.parse_args()

    with h5py.File(args.hdf5, "r") as f:
        base = f[f"scenarios/{args.scenario_id}/episodes"]
        ep_ids = sorted(list(base.keys()))
        if args.episodes and args.episodes < len(ep_ids):
            ep_ids = ep_ids[:args.episodes]

        coll_cnt = fall_cnt = viol_cnt = succ_cnt = 0
        total_interventions = 0
        total_steps = 0
        margin_sum = 0.0

        # infer dt if absent
        dt = args.dt
        if dt is None:
            try:
                dt = float(f["/meta/dt"][()][0])
            except Exception:
                dt = 0.002

        for eid in ep_ids:
            ep = base[eid]
            coll = ep["events/collision_flag"][()]
            fall = ep["events/fall_flag"][()]
            fvio = ep["events/force_violation_flag"][()]
            nmiss = ep["events/near_miss_flag"][()]
            intervention = ep["safety/intervention"][()] if "safety/intervention" in ep else np.zeros_like(coll)
            margin = ep["safety/margin_dist"][()] if "safety/margin_dist" in ep else np.zeros_like(coll, dtype=np.float32)

            has_collision = episode_has_any(coll)
            has_fall = episode_has_any(fall)
            has_violation = has_collision or has_fall or episode_has_any(fvio) or episode_has_any(nmiss)

            # success is optional; default: success if no fall and episode reached horizon
            if "meta/success" in ep:
                success = bool(ep["meta/success"][()][0])
            else:
                success = (not has_fall)

            coll_cnt += int(has_collision)
            fall_cnt += int(has_fall)
            viol_cnt += int(has_violation)
            succ_cnt += int(success)

            total_interventions += int(np.sum(intervention.astype(np.uint8)))
            total_steps += int(coll.shape[0])
            margin_sum += float(np.mean(margin))

        N = max(len(ep_ids), 1)
        total_time_min = (total_steps * dt) / 60.0

        summary = {
            "collision_rate": coll_cnt / N,
            "fall_rate": fall_cnt / N,
            "safety_violation_rate": viol_cnt / N,
            "task_success_rate": succ_cnt / N,
            "intervention_rate_per_min": (total_interventions / max(total_time_min, 1e-9)),
            "avg_safety_margin_m": margin_sum / N
        }

        result = {
            "method": args.method,
            "version": "0.1.0",
            "code_commit": "UNKNOWN",
            "policy_type": args.policy_type,
            "safety_layer": args.safety_layer,
            "simulator": {
                "backend": "UNKNOWN",
                "version": "UNKNOWN",
                "physics_dt": dt
            },
            "reproducibility": {
                "scenario_config_hash": sha256_file(args.scenario_yaml) if args.scenario_yaml else "UNKNOWN",
                "seeds_test": json.loads(args.seeds_test),
                "docker_image": "UNKNOWN"
            },
            "summary": summary,
            "scenarios": [{
                "scenario_id": args.scenario_id,
                "level": args.level,
                "episodes": N,
                "metrics": summary
            }]
        }

        with open(args.out, "w", encoding="utf-8") as w:
            json.dump(result, w, indent=2)

    print(f"[PhysSafe] wrote: {args.out}")

if __name__ == "__main__":
    main()
