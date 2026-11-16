# Refactor: split the notification pipeline

The refactor touches eleven components.

- Ingest group: Webhook Receiver, Event Validator, Dedup Filter.
- Routing group: Rule Engine, Template Renderer, Preference Service.
- Delivery group: Email Sender, SMS Sender, Push Sender, Retry Queue.
- Storage: Notification Store (a PostgreSQL database that the Rule Engine and the Retry Queue write to).

Flow: Webhook Receiver -> Event Validator -> Dedup Filter -> Rule Engine. The Rule Engine reads Preference Service, then Template Renderer, then fans out to the three senders. Failed sends go to Retry Queue, which re-enters the senders and records state in Notification Store.
