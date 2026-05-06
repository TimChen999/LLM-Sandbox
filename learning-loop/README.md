# Production ML Learning Loop

A lightweight setup for vibe-coding production ML concepts. The goal is **conceptual fluency** — understanding what each piece does, when to reach for it, and how it behaves when poked — without spending time on tedious implementation work.

## How the loop works

1. **Pick a topic.** One concept at a time (e.g., "model drift").
2. **Claude builds a tiny working demo** of it — a model, a fake data stream, a dashboard, whatever the topic needs.
3. **Claude writes a 1-paragraph plain-English explainer** of what's happening and why it matters in production.
4. **Claude offers a menu of "what if" knobs** — adjustments that change the system's behavior. Examples:
   - What if the input data slowly shifts over time?
   - What if 10% of requests are garbage?
   - What if we retrain weekly vs. daily?
   - What if the model is twice as slow?
5. **Pick a knob, run it, watch what happens.** Then discuss what you saw and what it implies for real systems.

The learning happens at steps 4 and 5. Breaking things and watching the system react is what builds intuition.

## Topic menu

Reasonable places to start. Not an order — pick whatever sounds interesting next.

### Serving and inference
- Model serving (turn a trained model into an HTTP endpoint)
- Batch vs. real-time inference
- Latency and throughput tradeoffs
- Caching predictions

### Monitoring and reliability
- Logging predictions and inputs
- Model performance monitoring (accuracy decay over time)
- Data drift detection
- Concept drift detection
- Alerting and on-call patterns

### Experimentation
- A/B testing two models
- Shadow deployments (run new model silently alongside old)
- Canary rollouts
- Offline vs. online evaluation

### Data and training pipelines
- Feature stores (what they are, why they exist)
- Training pipelines and reproducibility
- Retraining triggers (scheduled vs. drift-triggered)
- Data versioning

### LLM-specific production topics
- Prompt versioning
- LLM evals (how to test a non-deterministic system)
- Cost and token tracking
- Caching and rate limiting
- Guardrails and safety filters

### Cross-cutting
- Model registry and versioning
- Rollback strategies
- Cost tracking
- Compliance and audit logs

## Progress log

Add a row each time we explore a topic. Keep notes brief — the goal is to remember what stuck, not to write a textbook.

| Date | Topic | What I poked | What surprised me |
|------|-------|--------------|-------------------|
|      |       |              |                   |

## Working agreement with Claude

- Claude writes the code; I make the decisions about what to try next.
- Explanations stay in plain English. If a term shows up, define it inline.
- Demos stay small — one concept per demo. Resist building a "real" app.
- Breaking things on purpose is encouraged. Failure modes teach more than green checkmarks.
