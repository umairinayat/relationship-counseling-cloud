# Failure Modes & Mitigation

## Emotional Failures

### 1. False Reassurance
- **Failure**: Saying "Everything will be okay" or "He definitely loves you."
- **Risk**: Creates false hope; invalidates user's fear if things go wrong.
- **Mitigation**: `HallucinationControls.enforce_epistemic_humility` rewrites definitives to "It seems possible..."

### 2. Directive Advice
- **Failure**: "You must break up with him."
- **Risk**: User takes action they aren't ready for; blames AI for fallout.
- **Mitigation**: `SafetyGuardrails` Layer 2 regex filter blocks "should/must" + verb patterns.

### 3. Amateur Diagnosis
- **Failure**: "He sounds like a narcissist."
- **Risk**: Stigmatizing; medically inaccurate; unsafe.
- **Mitigation**: System Prompt explicitly forbids diagnostic terms. Monitoring logs `AMATEUR_DIAGNOSIS` events.

## Technical Failures

### 1. LLM Timeout / Latency
- **Detection**: `LLMClient` throws `APITimeoutError`.
- **Mitigation**: Exponential backoff retries (x3). If all fail, return "I'm having trouble thinking clearly right now. Please try again in a moment."

### 2. Database Failure (Memory)
- **Detection**: `asyncpg` connection error.
- **Mitigation**: Fail OPEN for safety? No, Fail CLOSED. If memory cannot be retrieved, we cannot ensure safety context. Return error message.

### 3. Cost Explosion
- **Detection**: `CostOptimizer` checks daily token usage > 100k.
- **Mitigation**: System hard stops processing new non-crisis messages for that user/tenant.
