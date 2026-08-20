# Modular LLM Inference Handbook

## Sources
- [LLM Inference Handbook](https://handbook.modular.com/) (Modular)

## Cards

### Inference vs. Serving

**Front:**
What is the difference between LLM *inference* and LLM *serving*?

**Back:**
- **Inference** is the computation itself — running the forward passes that turn a prompt into output tokens. You can do this standalone in a script with a single model on a single GPU.
- **Serving** is the production system wrapped around it — an API layer, request queuing and scheduling, batching, KV cache management, load balancing across replicas, autoscaling, observability, and token streaming.

Inference is one request's worth of math. Serving is what makes it a multi-tenant service that holds up under concurrency and meets latency SLOs.

An **inference server** (vLLM, SGLang, MAX, TensorRT-LLM) is the software that does both: it loads the model onto hardware and provides the serving machinery around it. "Inference server" and "inference framework" are used interchangeably, with *server* leaning toward runtime operation and *framework* toward the broader toolkit.

**Tags:**
ml::llm::inference source::modular-handbook

---

### Stages of an LLM Inference Request

**Front:**
What stages does a request pass through in an LLM inference server?

**Back:**
1. **Tokenization** — the input text is converted into token IDs the model can consume.
2. **Scheduling** — the server admits the request into a batch, allocating KV cache space for it.
3. **Prefill** — all prompt tokens are processed **in parallel**, populating the KV cache and producing the first output token.
4. **Decode** — tokens are generated **sequentially**, one forward pass each, since every token depends on the one before it. Streamed back (detokenized) until the model emits an **EOS** (end-of-sequence) token or hits a length limit.

Two views of scheduling: per request it gates entry to prefill, but the scheduler itself re-runs **every step**, re-deciding the batch and preempting requests when KV cache runs short. A single batch can hold some requests prefilling and others decoding.

**Tags:**
ml::llm::inference source::modular-handbook

---

### Why LLM Inference Is Structurally Different from Classic ML Inference

**Front:**
How does serving an LLM differ structurally from serving a traditional ML model (e.g. a classifier)? 3 main points in answer.

**Back:**
Traditional model: **one request = one forward pass.** Cost is fixed, latency is predictable, the call is stateless.

LLM: generation is **autoregressive**, so one request = one prefill pass over the prompt + **one forward pass per generated token**. That changes three things:

- **Variable cost** — a request may emit 5 tokens or 5,000, and you do not know which until the model emits its end-of-sequence (EOS) token. You cannot size or schedule a request from its input alone.
- **Stateful** — the KV cache for that request must live in GPU memory across every decode step, so memory is held for the request's whole lifetime, not just one pass.
- **Long-lived** — requests overlap for seconds, so the scheduler manages a churning population of in-flight requests rather than discrete batches.

This is why LLM serving needs its own infrastructure (continuous batching, KV cache management, paged memory) instead of the request/response batching that works for classic models.

**Tags:**
ml::llm::inference source::modular-handbook

---
