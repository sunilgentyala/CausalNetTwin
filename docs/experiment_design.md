# Experiment Design

## Topologies

- Leaf-spine with equal-cost paths
- k-ary fat-tree
- 4:1 oversubscribed multi-tenant fabric
- Link and path failure variants

## Workloads

- AI AllReduce and parameter synchronization
- RDMA-style elephant flows
- Kafka producer and consumer traffic
- Spark shuffle
- Storage backup and replication
- Latency-sensitive mice flows

## Scenarios

- Mixed steady-state traffic
- Sudden elephant-flow arrival
- Storage backup and AI training collision
- Link failure and packet loss
- Oversubscribed tenant contention
- Collective communication synchronization burst

## Baselines

ECMP, static traffic engineering, correlation-based congestion prediction, conventional DRL, and a digital twin without causal validation.

## Metrics

P95 and P99 flow completion time, SLO violation rate, link utilization, queue occupancy, packet loss, Jain fairness, route churn, intervention success rate, harmful-action rate, rollback frequency, telemetry overhead, inference latency, and congestion-source localization accuracy.

## Extension to packet-level and emulation environments

1. Recreate topologies in Containerlab or Mininet.
2. Program BMv2 switches with P4 INT metadata and ECN/queue controls.
3. Use ONOS or Ryu for routing and P4Runtime actuation.
4. Generate RDMA-like, AllReduce, Kafka, Spark, and storage-replication traces.
5. Scale topology and workload diversity in ns-3.
6. Export the same telemetry schema defined in `telemetry_schema.md`.
7. Preserve seed, topology, workload, model version, safety limits, candidate action, decision, and rollback record for every run.
