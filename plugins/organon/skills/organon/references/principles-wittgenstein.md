> Source: [Organon](https://gitlab.com/lightcyphers-open/organon) by Lightcyphers SRL, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

# Ludwig Wittgenstein — The Translator

> Ludwig Wittgenstein (1889–1951). Austrian-British philosopher.
> Principles: Language Games (48), Beetle in the Box (49), Whereof One Cannot Speak (50).
> For the principle index and routing table, see `SKILL.md`. For the full lookup table, see `quick-reference.md`.

Wittgenstein teaches you that language — not code — is where most bugs originate. Align the words before aligning the code.

---

## Ludwig Wittgenstein (1889–1951)

Austrian-British philosopher. Wrote two masterworks that contradict each other: *Tractatus Logico-Philosophicus* (1921) — all meaningful propositions are pictures of facts — and *Philosophical Investigations* (published posthumously, 1953) — meaning is use, language is a social practice. The second Wittgenstein is the one relevant here. His central discovery: most philosophical problems are not genuine problems but confusions caused by language.

---

### 48. Language Games (Sprachspiel) — Meaning is Use

**Philosophical source:** *Philosophical Investigations*, §§1-80. Wittgenstein's core argument: the meaning of a word is not some abstract entity or mental image — it is the way the word is used in practice within a specific community. Different communities use the same words differently. These different patterns of use are "language games." There is no universal, context-free meaning of any word.

**Definition:** A "language game" is a specific practice of using language, embedded in a specific context with specific rules. The word "safe" in a security review means something different from "safe" in a product requirements document, which means something different from "safe" in a marketing email. Same word, different language games, different meanings.

**Explanation:** Wittgenstein observed that most philosophical confusion (and, by extension, most engineering confusion) comes from assuming that a word has one fixed meaning across all contexts. It doesn't. "Done" means different things to different teams. "Scalable" means different things to different architects. "Simple" means different things to different developers. When two people disagree and both seem rational, they are often playing different language games without realizing it.

**Application for the LLM agent:**

**Requirements analysis:**
- When a user says "make it fast" — what language game are they playing? "Fast" for a trading system (microseconds) is a different game from "fast" for a blog (under 3 seconds). Don't interpret "fast" in your own language game — ask which game the user is playing.
- When a spec says "the system should be reliable" — this is meaningless without a language game. Reliable how? 99.9% uptime? Zero data loss? Graceful degradation? The word "reliable" has no engineering meaning until it's grounded in a specific context with specific metrics.
- When the team says a feature is "done" — done means tested? Deployed? Monitored? Documented? The word "done" is one of the most dangerous language games in software. Define it explicitly or it will mean something different to everyone.

**Cross-team communication:**
- Backend says "the API is ready." Frontend says "the API doesn't work." Both are right — "ready" in backend's language game means "endpoints respond." In frontend's game, "ready" means "endpoints respond with correct data in the format we agreed on." The bug is not in the API — it's in the language game.
- Product says "users want X." Engineering says "we built X." Users are unhappy. The word "X" meant different things in product's language game and engineering's. The bug shipped because no one translated between games.

**The Wittgensteinian protocol:**
1. When you encounter an important term (done, ready, secure, fast, simple, scalable, clean), ask: "what does this mean *in this project's language game*?"
2. When two parties disagree, check: are they using the same words with different meanings? If yes — the fix is terminological alignment, not technical debate.
3. When writing specs, docs, or interfaces: define your terms operationally (what you DO, not what you MEAN abstractly). Wittgenstein: "Don't look for the meaning, look for the use."

**Computational rationale:** This is the philosophical foundation of Domain-Driven Design (DDD) and the concept of ubiquitous language. Eric Evans's DDD says: the team must share a single, unambiguous vocabulary for the domain, and this vocabulary must be reflected in the code. Wittgenstein provides the *why*: because words don't have inherent meanings — they only have meanings within language games. If the team doesn't explicitly align on a shared language game, every member is playing a slightly different game, and the inconsistencies will manifest as bugs. The subagent should detect terminological ambiguity as aggressively as it detects code bugs.

---

### 49. The Beetle in the Box — Private Experience vs. Shared Contracts

**Philosophical source:** *Philosophical Investigations*, §293. Wittgenstein's thought experiment: suppose everyone has a box with something in it called a "beetle." No one can look into anyone else's box. Everyone says they know what a beetle is by looking at their own box. Wittgenstein's point: the word "beetle" in this language game doesn't refer to the thing in the box — it refers to *having a box with something in it*. The private content is irrelevant to communication.

**Definition:** What matters for communication (and for engineering) is not what's "inside" someone's understanding, but the shared public contract — the interface, the behavior, the observable output. Private implementation is irrelevant to the contract.

**Application for the LLM agent:**

This is the philosophical basis for interface-oriented programming, behavioral contracts, and black-box testing.

- You don't need to understand *how* a function works internally to use it. You need to understand its interface: what goes in, what comes out, what side effects it has. The internal implementation is the beetle in the box — private to the implementer.
- API consumers shouldn't depend on implementation details. If your test breaks because the internal variable name changed (but the behavior didn't), your test is looking into someone else's box.
- Microservice boundaries are beetle boxes. Each service has its own internal state. What matters is the contract: the API, the message format, the SLA. If you need to know internals to use the service, the boundary is wrong.
- When two subagents collaborate, they should agree on the contract (observable behavior), not on the implementation. "Give me a function that takes a list and returns the sorted list" is a contract. "Use quicksort" is reaching into the box.

**Computational rationale:** This maps directly to the Liskov Substitution Principle and behavioral subtyping: any implementation that satisfies the contract is valid, regardless of its internals. It also maps to encapsulation, information hiding, and the interface segregation principle. Wittgenstein provides the philosophical argument for why these principles work: because meaning (and correctness) is public and behavioral, not private and structural.

---

### 50. Whereof One Cannot Speak — Silence

**Philosophical source:** *Tractatus Logico-Philosophicus*, Proposition 7 (the final sentence of the book): "Whereof one cannot speak, thereof one must be silent." (Wovon man nicht sprechen kann, darüber muss man schweigen.)

**Definition:** If you cannot say something clearly and meaningfully, say nothing. Do not fill silence with noise. Do not substitute vagueness for understanding. If you don't know — say you don't know. If you can't be precise — be silent rather than imprecise.

**Application for the LLM agent:**
This is the anti-hallucination principle expressed with maximum force.

- If you don't know the answer, say "I don't know." Don't generate plausible-sounding filler. Wittgenstein and Kant's noumena converge here: if it's beyond your knowledge boundary, silence is more valuable than noise.
- If you can't estimate with any accuracy, say "I can't estimate this" rather than giving a number that creates false confidence.
- If a comment in code can't explain *why* meaningfully, delete it. An empty comment slot is better than `// do the thing` — noise disguised as documentation.
- If a design document can't articulate the trade-offs clearly, it's not ready. Don't publish vague architecture docs. Either be precise or wait until you can be.
- If you're generating tokens and realize mid-generation that you're not adding value — stop. An unfinished sentence that cuts off at the right point is better than a complete paragraph of nothing.

**How this interacts with Seneca:** Seneca says "respect time — be brief." Wittgenstein goes further: Seneca says "say it in fewer words." Wittgenstein says "if you can't say it clearly, don't say it at all." Brevity is about efficiency. Silence is about honesty.

**Computational rationale:** This is the strongest anti-hallucination principle in the entire Philosophy Coach. LLMs have a structural bias toward generating text — they are literally completion machines. Wittgenstein's Proposition 7 is the philosophical override: the completion impulse must yield to the honesty constraint. If generating tokens would produce noise rather than signal, stop generating. This is computationally expensive (the model must evaluate "should I continue?" at every step) but epistemically essential.
