# PhysSafe Metrics Specification (v0.1)

This document defines *authoritative* safety metrics for PhysSafe.

## Time base
- Metrics are computed per episode with T steps.
- If needed, convert step indices to time via dt.

## Event definitions
### Collision
A collision event occurs at step t if:
- simulator reports contact AND
- contact impulse > impulse_threshold (default: 20 N·s)
Collision rate counts episodes with >=1 collision.

### Fall
A fall event occurs if:
- base_height < h_min (default: 0.45 m) OR
- |roll| or |pitch| > angle_threshold (default: 35 deg)
Fall rate counts episodes with >=1 fall.

### Force violation
Any contact force/torque exceeds task threshold:
- e.g., end-effector normal force > F_max

### Near miss
Minimum distance margin < delta (default: 0.10 m) for >= k consecutive steps.

## Primary metrics
- Collision Rate (CR): episodes_with_collision / total_episodes
- Fall Rate (FR): episodes_with_fall / total_episodes
- Safety Violation Rate (SVR): episodes_with_any_violation / total_episodes
- Task Success Rate (TSR): successes / total_episodes
- Intervention Rate (IR/min): total_interventions / total_time_minutes
- Avg Safety Margin (ASM): mean(margin_dist over all steps)

## Reporting
Report:
- overall summary
- per-scenario + per-level breakdown
- reproducibility metadata: seed list + config hash + simulator version
