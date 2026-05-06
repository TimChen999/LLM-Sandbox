# Making This Substitute for Real Coursework

Vibe coding alone is entertainment. With the right rules, it becomes a real curriculum — at least for the production ML half, where formal coursework is weakest anyway.

## What this can and can't replace

| What this loop gives you | What it doesn't |
|---|---|
| Vocabulary, system-level thinking, intuition for tradeoffs | Math foundations (linear algebra, stats, optimization) |
| Familiarity with what each component does and why | Algorithm internals (e.g., how attention actually computes) |
| Pattern recognition across architectures | The discipline of writing code yourself, from scratch |
| Exposure to failure modes | Reproducing things under exam-style conditions |

So: this is a strong substitute for an MLOps / production ML course. It is **not** a substitute for ML fundamentals — for those, pair it with structured material (suggestions at the bottom).

## The rules that turn watching into learning

These are the rules. Without them, the loop is a tour. With them, it's a curriculum.

### Rule 1: Predict before observing
Before Claude runs each "what if" knob, write down what you expect to happen — in the progress log, in plain English. Then run it. **The gap between your prediction and reality is the learning.** If you skip this step, you become a passenger watching a screen.

Example:
> *Prediction: if I shift the input distribution by 20%, accuracy will drop by ~5% and the drift detector will trigger after about 50 requests.*
>
> *Actual: accuracy dropped 12%. Drift detector fired after 8 requests. Why? Because the detector compares distributions per-batch, not cumulatively.*

### Rule 2: Make the design call before Claude writes code
Don't let Claude jump straight to "here's the architecture." You guess first — "I'd put a queue here, maybe cache predictions?" — then Claude shows you what's standard and you discuss why. This builds the **judgment** muscle. Judgment is what coursework usually fails to teach and what interviews actually test.

### Rule 3: Explain it back in your own words
After each topic, write a 3-sentence explanation in the progress log, as if explaining to a friend who codes but doesn't know ML. If you can't write the three sentences, you didn't learn it — go again.

### Rule 4: Reimplement core topics from scratch, weeks later
This is the hardest rule and the most important one. Pick 2–3 topics that matter most to your goals (probably: model serving, monitoring, A/B testing) and rebuild them in a blank file with **no help from Claude**. Painful, but it's the closest substitute for the rigor of coursework. If you skip this rule, you'll recognize patterns but not be able to produce them.

### Rule 5: Pair each topic with one real artifact
For each topic, read one real-world thing — a blog post, a paper, a postmortem. The toy demo gives you the shape; the artifact gives you the scale and the war stories. Suggested pairings:

| Topic | Artifact |
|---|---|
| Data drift | Google's *Data Validation for Machine Learning* paper |
| A/B testing | Microsoft's *Trustworthy Online Controlled Experiments* (book or paper) |
| Recommenders | Netflix tech blog series on recommendations |
| Feature stores | Uber's *Michelangelo* blog post |
| LLM evals | Anthropic's evaluation guide; OpenAI evals repo |
| Model serving | Any KServe or BentoML production case study |

### Rule 6: Capstone project
After ~10 topics, build one project that uses 5+ of them together — something you would be willing to show another engineer. Examples: a recommender with monitoring, retraining, and A/B testing. An LLM tutor with prompt versioning, evals, and cost tracking.

The capstone is the test of whether the loop worked. If you can't build it, the previous topics didn't stick.

## How the process actually works, step by step

Here is what a single topic looks like end-to-end, with the rules applied.

1. **Pick a topic** from the list below. One concept at a time.
2. **State the goal in your own words** before any code. ("I want to understand what data drift is and how systems detect it.") Write it in the progress log.
3. **Make the design call (Rule 2)**. Guess what the system would need: a baseline distribution, a way to compare new data to it, an alert. Write your guess down.
4. **Claude builds the demo.** Small, focused, one concept. Claude also writes a plain-English explainer paragraph.
5. **Claude offers a menu of "what if" knobs.**
6. **Predict (Rule 1).** Pick a knob. Before running, write down what you expect to happen.
7. **Run it. Observe.** Compare to your prediction. Discuss the gap.
8. **Repeat steps 5–7** for 2–3 knobs per topic.
9. **Explain back (Rule 3).** Write the 3-sentence explanation. Fill in "what surprised me" in the log.
10. **Read the artifact (Rule 5).** Skim the paper or blog. Note one thing the real-world version does that the toy didn't.
11. **Move to the next topic.** Or, every few topics, do a Rule 4 reimplementation pass.

That's the loop. Boring on paper, effective in practice.

## Comprehensive topic list

Pick whatever sounds interesting next. The order doesn't matter, but starting with **model serving + basic monitoring** gives you a substrate that later topics can plug into.

### Serving and inference (foundations)
- **Model serving** — turn a trained model into a live HTTP endpoint. Teaches what "deployment" actually means.
- **Batch vs. real-time inference** — when to precompute vs. compute on demand. Cost/latency tradeoff.
- **Caching predictions** — what to cache, what not to, why repeated requests are an opportunity.
- **Latency and throughput tradeoffs** — p50 vs. p99, batching, GPU utilization.

### Monitoring and reliability (the 3am stuff)
- **Logging predictions and inputs** — what to log, what not to, retention.
- **Performance monitoring** — accuracy decay when ground truth is delayed.
- **Data drift detection** — your inputs change shape and the model silently rots.
- **Concept drift detection** — the world changes and the relationship the model learned no longer holds. Different beast from data drift.
- **Alerting and on-call patterns** — what's worth paging on vs. what's noise.

### Experimentation (how teams actually decide if a new model is better)
- **A/B testing two models** — split traffic, measure, decide. Statistical thinking in production.
- **Shadow deployments** — run new model silently next to old one. Test risk-free.
- **Canary rollouts** — release to 1% → 10% → 100%. Gradual de-risking.
- **Offline vs. online evaluation** — why offline metrics often lie.

### Data and training pipelines
- **Feature stores** — what they are, why teams build whole systems just for features.
- **Training pipelines and reproducibility** — why "it worked on my laptop" is a red flag.
- **Retraining triggers** — scheduled vs. drift-triggered. When each is right.
- **Data versioning** — DVC, lakeFS, why you can't just git-add a 50GB CSV.

### LLM-specific production topics
- **Prompt versioning** — treating prompts like code.
- **LLM evals** — testing a non-deterministic system.
- **Cost and token tracking** — tokens add up fast; how teams monitor and cap spend.
- **Caching and rate limiting** — both for cost and for reliability.
- **Guardrails and safety filters** — keeping the model from saying or doing things it shouldn't.
- **Prompt caching (provider-side)** — when and how it actually saves money.

### Cross-cutting
- **Model registry and versioning** — Git, but for trained models.
- **Rollback strategies** — when the new model is worse, how do you undo, fast?
- **Cost tracking** — both training and inference.
- **Compliance and audit logs** — what regulated industries actually require.

## What you still need outside this loop

For the ML fundamentals side, this loop won't get you there. Pair it with one of:

- **Math/stats**: 3Blue1Brown's linear algebra series, Khan Academy stats, *Mathematics for Machine Learning* by Deisenroth, Faisal, Ong (free PDF).
- **Classical ML internals**: *Hands-On Machine Learning* by Géron, or the StatQuest YouTube channel.
- **Deep learning**: fast.ai, or Karpathy's *Zero to Hero* series.

Even one of these running in the background, plus this loop, makes a self-built curriculum that's competitive with most real courses on production ML.
