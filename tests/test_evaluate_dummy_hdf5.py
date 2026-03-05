import json
import os
import subprocess
from tests.utils import make_dummy_hdf5

def test_evaluate_produces_result_json(tmp_path):
    scenario_id = "HRI_HUMAN_PROX_001"
    h5 = tmp_path / "dummy.h5"
    out = tmp_path / "result.json"

    make_dummy_hdf5(str(h5), scenario_id=scenario_id, num_eps=3, T=200)

    cmd = [
        "python", "evaluation/evaluate.py",
        "--hdf5", str(h5),
        "--scenario_id", scenario_id,
        "--level", "L0",
        "--out", str(out),
        "--method", "CI-Dummy",
        "--policy_type", "rl",
        "--safety_layer", "none",
        "--seeds_test", "[100]"
    ]
    subprocess.check_call(cmd)

    assert out.exists()
    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "summary" in data
    # dummy has 1 collision ep, 1 fall ep out of 3
    assert abs(data["summary"]["collision_rate"] - (1/3)) < 1e-6
    assert abs(data["summary"]["fall_rate"] - (1/3)) < 1e-6
