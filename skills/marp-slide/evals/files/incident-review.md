---
marp: true
theme: default
paginate: true
---

<style>
section { background: #fdf6e3; color: #586e75; }
section:nth-child(2n) { background: #073642; color: #93a1a1; }
h2 { color: #b58900; }
</style>

<!-- _class: lead -->

# Checkout outage, 12 March

Incident review, Payments team

---

## What happened during the checkout outage on the twelfth of March and why it lasted so long

- Deploy 4.18.0 shipped a connection-pool change at 14:02 UTC
- p99 checkout latency rose from 210 ms to 840 ms
- Error rate peaked at 3.2% of checkout requests
- Pager fired after 14 minutes because the alert threshold was 5%
- Rollback started at 14:31 and finished at 14:38
- Two retries per request doubled database load
- Cache hit rate fell from 92% to 61%
- Support received 312 tickets
- Finance estimates 41,000 EUR in lost orders

<!-- Mention that the 5% threshold was approved in January. -->

---

## Latency

![bg right:40%](img/latency-chart.png)

<p style="color: #dc322f; font-size: 40px">840 ms p99</p>

---

## The fix

```python
pool = ConnectionPool(max_size=50, timeout_s=2)  # was max_size=10
```

- Pool size restored to 50
- Alert threshold lowered to 1%
