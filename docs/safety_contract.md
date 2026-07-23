# Safety Contract

The default research policy approves an action only when all predicted outcomes remain within the configured limits:

- P99 flow completion time at or below 12 ms
- Packet loss at or below 0.20 percent
- Jain tenant fairness at or above 0.85
- Route churn at or below 2.0 percent per decision window
- SLO violation rate at or below 8.0 percent

The limits are examples for reproducible evaluation, not universal production defaults. Production use requires workload-specific SLOs, independent policy approval, change windows, access control, audit retention, and fail-safe behavior.

Rollback is triggered when the observed P99 latency or packet-loss outcome exceeds the predicted value by more than 20 percent and the deviation is harmful.
