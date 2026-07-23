# Telemetry Schema

Each observation window should contain the following fields:

| Field | Unit | Source | Purpose |
|---|---:|---|---|
| timestamp | ns or ms | collector | Temporal alignment |
| switch_id, port_id, queue_id | identifier | fabric inventory | Causal unit definition |
| tenant_id, workload_class | identifier | Kubernetes and scheduler labels | Multi-tenant attribution |
| link_utilization | percent | switch counter | Load state |
| queue_occupancy | bytes or packets | P4 INT or queue counter | Congestion state |
| ecn_mark_rate | percent | INT and host telemetry | Early congestion signal |
| packet_loss | percent | switch and host counters | Safety outcome |
| p95_fct, p99_fct | milliseconds | flow monitor | Tail performance |
| route_id, next_hop | identifier | SDN controller | Intervention and churn |
| storage_io_pressure | normalized | storage metrics | Cross-traffic confounder |
| collective_phase | categorical | AI job telemetry | Synchronized burst confounder |
| action_id, action_type | identifier | remediation controller | Treatment variable |
| predicted_outcome | structured | counterfactual engine | Pre-deployment expectation |
| observed_outcome | structured | verifier | Post-deployment validation |
| rollback_status | Boolean | verifier | Safety audit |
