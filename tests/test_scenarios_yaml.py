import glob
import yaml

REQUIRED_KEYS = ["scenario_id", "scenario_name", "description", "simulator", "robot_model", "task", "time", "levels"]

def test_scenarios_yaml_parse_and_required_keys():
    files = glob.glob("scenarios/*.yaml")
    assert files, "No scenario YAML files found in scenarios/"

    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for k in REQUIRED_KEYS:
            assert k in data, f"{fp} missing required key: {k}"
        # must have L0-L4 for difficulty scaling
        for level in ["L0", "L1", "L2", "L3", "L4"]:
            assert "levels" in data and level in data["levels"], f"{fp} missing levels.{level}"
