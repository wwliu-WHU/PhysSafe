# PhysSafe

**PhysSafe** is an open benchmark for evaluating **physical safety in humanoid robots**.

The benchmark provides standardized **safety-critical scenarios**, **evaluation metrics**, and **trajectory data formats** for reproducible research in robot safety.

---

# Why PhysSafe

Humanoid robots are increasingly deployed in environments where **safety is critical**, including:

- human–robot interaction
- collaborative manipulation
- dynamic locomotion
- service robotics

However, existing benchmarks focus primarily on **task performance**, while **physical safety** remains under-evaluated.

PhysSafe aims to provide the **first benchmark specifically designed for humanoid physical safety evaluation**.

---

# Benchmark Tasks

PhysSafe currently includes the following safety scenarios:

### 1 Human Proximity (HRI)

Robot operates near humans while maintaining safe distance.

Safety risks:

- collision
- unsafe proximity
- unexpected contact

---

### 2 Uneven Terrain Locomotion

Humanoid walking on irregular terrain.

Safety risks:

- fall
- slip
- instability

---

### 3 External Disturbance Recovery

Robot experiences unexpected pushes.

Safety risks:

- loss of balance
- unsafe recovery
- collision

---

# Evaluation Metrics

PhysSafe evaluates controllers using safety metrics:

| Metric | Description |
|------|------|
| Collision Rate | fraction of episodes with collision |
| Fall Rate | fraction of episodes with falls |
| Safety Violation Rate | fraction of episodes violating safety constraints |
| Task Success Rate | fraction of successful task completion |
| Intervention Rate | frequency of safety controller intervention |
| Average Safety Margin | average distance to safety boundary |

---

# Quickstart

Example evaluation:

```bash
python evaluation/evaluate.py \
  --hdf5 sample_rollouts.h5 \
  --scenario_id HRI_HUMAN_PROX_001 \
  --level L2 \
  --out result.json
