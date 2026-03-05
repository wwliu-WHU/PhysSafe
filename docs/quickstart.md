# Quickstart

## 1) Prepare a rollout HDF5
Export your simulation rollouts to match `spec/hdf5_schema.md`.

## 2) Evaluate
Example:
```bash
python evaluation/evaluate.py \
  --hdf5 path/to/rollouts.h5 \
  --scenario_id HRI_HUMAN_PROX_001 \
  --level L3 \
  --scenario_yaml scenarios/hri_human_proximity.yaml \
  --seeds_test "[100,101,102,103,104]" \
  --method DualModelSafety \
  --policy_type rl \
  --safety_layer dual_model \
  --out results/result.json
