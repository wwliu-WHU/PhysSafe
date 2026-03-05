# PhysSafe: A Benchmark for Physical Safety in Humanoid Robots

PhysSafe is an open benchmark for evaluating **physical safety** of humanoid (and general embodied) robot controllers.
It provides:
- standardized safety-critical scenarios (YAML specs)
- a unified evaluation protocol + metrics
- an HDF5 dataset schema for large-scale synthetic trajectories
- baseline slots and a leaderboard format

## What you can do today
- Use our **scenario specs** to configure safety-critical evaluation
- Export rollouts to our **HDF5 schema**
- Run `evaluation/evaluate.py` to generate a standardized `result.json` for leaderboard submission

## Repository Structure
- `scenarios/`: scenario definitions with difficulty levels (L0–L4)
- `spec/`: benchmark specs (scenario/result/HDF5/metrics)
- `evaluation/`: reference metric computation and result export
- `examples/`: example outputs and dummy generators

## Quickstart
See `docs/quickstart.md`.

## License
Apache-2.0 (recommended for community adoption).

## Citation
See `CITATION.cff`.
