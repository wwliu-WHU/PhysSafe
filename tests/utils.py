from __future__ import annotations
import h5py
import numpy as np

def make_dummy_hdf5(path: str, scenario_id: str, num_eps: int = 3, T: int = 200, dt: float = 0.002):
    with h5py.File(path, "w") as f:
        meta = f.create_group("meta")
        meta.create_dataset("dt", data=np.array([dt], dtype=np.float32))
        meta.create_dataset("simulator_backend", data=np.string_("dummy"))
        meta.create_dataset("simulator_version", data=np.string_("0.0"))

        scen_root = f.create_group(f"scenarios/{scenario_id}/episodes")
        for i in range(num_eps):
            ep = scen_root.create_group(f"{i:06d}")

            # events
            events = ep.create_group("events")
            # Make: ep0 safe, ep1 collision, ep2 fall (if exists)
            coll = np.zeros((T,), dtype=np.uint8)
            fall = np.zeros((T,), dtype=np.uint8)
            fvio = np.zeros((T,), dtype=np.uint8)
            nmiss = np.zeros((T,), dtype=np.uint8)

            if i == 1:
                coll[50] = 1
            if i == 2:
                fall[100] = 1

            events.create_dataset("collision_flag", data=coll)
            events.create_dataset("fall_flag", data=fall)
            events.create_dataset("force_violation_flag", data=fvio)
            events.create_dataset("near_miss_flag", data=nmiss)

            safety = ep.create_group("safety")
            safety.create_dataset("intervention", data=np.zeros((T,), dtype=np.uint8))
            safety.create_dataset("margin_dist", data=np.full((T,), 0.25, dtype=np.float32))

            meta_ep = ep.create_group("meta")
            # success: treat fall episode as failure
            meta_ep.create_dataset("success", data=np.array([0 if i == 2 else 1], dtype=np.uint8))
