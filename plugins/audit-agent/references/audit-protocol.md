# Shared Audit Protocol

Standards and patterns shared across all audit frameworks.

## Mandatory Completion Requirements

Every audit MUST:

1. **Answer ALL questions/metrics** - No skipping, no "N/A"
2. **Provide evidence** - Specific examples, not vague statements
3. **Complete verification checklist** - All boxes checked [x]
4. **Show completion count** - X/X format
5. **Include synthesis section** - Actionable conclusions

## Evidence Requirements

### Acceptable Evidence
- Direct quotes from code/docs
- Specific file paths and line numbers
- Measurable metrics (response time, LOC, etc.)
- Concrete examples of behavior
- Screenshots or output logs

### Unacceptable Evidence
- "It seems like..."
- "Generally speaking..."
- "In my opinion..."
- Assumptions without verification
- Hearsay or secondhand information

## Output Format Standards

### Question Answers
```markdown
### QUESTION X OF Y: [TITLE]
**"[Question text]"**

[Context/explanation]

> Your answer for QX:
[Substantive answer with 2-3 sentences minimum]
[Specific evidence or examples]
[Concrete recommendation if applicable]
```

### Metric Scores
```markdown
#### METRIC X/Y: [TITLE]
**"[Scoring question]"**

Red flags: [What to look for]

> **Score: X/5**
> **Evidence:** [Specific findings justifying score]
```

### Checklist Format
```markdown
- [x] Item completed with evidence
- [ ] Item NOT completed (must go back)
```

## Quality Gates

### Before Submitting Any Audit

1. **Completion Gate**
   - All questions/metrics addressed
   - No placeholder text remaining
   - Checklist 100% complete

2. **Evidence Gate**
   - Every finding has supporting evidence
   - No unsubstantiated claims
   - File paths/references where applicable

3. **Actionability Gate**
   - Synthesis provides clear next steps
   - Priorities are assigned
   - Recommendations are specific

## Framework-Specific Additions

### Jobs Audit
- Must end with "THE ONE GREAT IDEA"
- Top 3 actions must be immediately actionable
- Design-focused recommendations

### Carlin Audit
- Must maintain Carlin's voice throughout
- "THE ONE THING TO SAY OUT LOUD" is mandatory
- No corporate speak in answers

### Vibe Audit
- Exact numeric scores required (no ranges)
- Pareto fix plan must have 10 items
- Deployment confidence must be selected

## Multi-Audit Protocol

When running multiple audits:

1. **Sequential Execution** (if single session)
   - Complete each audit fully before starting next
   - Cross-reference after all complete

2. **Parallel Execution** (if using agents)
   - Launch all audits simultaneously
   - Wait for all to complete
   - Run synthesis after gathering results

3. **Synthesis Requirements**
   - Cross-reference table mandatory
   - Contradiction analysis required
   - Unified action plan with priorities

## Anti-Patterns to Avoid

### "Drive-By Audit"
Skimming questions without depth. Every question deserves real analysis.

### "Benefit of Doubt"
Assuming things work when not verified. Default to skepticism.

### "Generic Answers"
Copy-paste style responses that could apply to anything. Be specific.

### "Happy Path Only"
Only considering best-case scenarios. Audits expose problems.

### "Completion Theater"
Checking boxes without doing the work. The checklist verifies, not replaces.

## Audit Hygiene

- Start fresh for each audit (no assumptions from previous audits)
- Read actual code/content, don't rely on descriptions
- If you can't verify, mark as UNVERIFIED and score 0
- Be consistent in scoring across audits
- Document what you couldn't assess and why
