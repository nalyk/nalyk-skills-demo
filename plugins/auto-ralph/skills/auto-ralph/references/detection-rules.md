# Reguli de Detecție pentru auto-ralph

Sistem de scoring pentru a determina dacă un task este potrivit pentru Ralph Loop.

## Scoring System (0-4 puncte)

### Criteriu 1: Criterii de Succes Clare (+1 punct)

**Întrebare:** Poate fi verificat obiectiv dacă task-ul e complet?

| Indicator | Scor |
|-----------|------|
| "fix bug X" (eroare dispare = succes) | +1 |
| "add tests" (teste trec = succes) | +1 |
| "implement feature X" (funcționează = succes) | +1 |
| "make it better" (subiectiv) | 0 |
| "help me understand" (nu e executabil) | 0 |

**Keywords pozitive:**
- fix, repair, solve, debug
- implement, add, create, build
- test, write tests, coverage
- refactor, clean up, reorganize

**Keywords negative:**
- explain, understand, what is
- help me, show me
- why, how does, what does
- explore, investigate, research

---

### Criteriu 2: Beneficiază de Iterație (+1 punct)

**Întrebare:** Task-ul necesită multiple încercări pentru a reuși?

| Tip Task | Scor | Motivație |
|----------|------|-----------|
| Bug fixing | +1 | try → fail → analyze → retry |
| Test writing | +1 | write → run → fix → repeat |
| Feature building | +1 | implement → test → refine |
| Code explanation | 0 | one-shot answer |
| Question answering | 0 | single response |

**Iterația ajută când:**
- Există feedback loop (teste, erori, logs)
- Soluția poate fi verificată automat
- Îmbunătățirea e incrementală

---

### Criteriu 3: Scop Bine Definit (+1 punct)

**Întrebare:** Este clar CE trebuie făcut și UNDE?

| Specificitate | Scor | Exemplu |
|---------------|------|---------|
| Foarte specific | +1 | "fix auth in login.ts line 45" |
| Specific | +1 | "add CRUD for users in api/" |
| Moderat | +0.5 | "improve the auth system" |
| Vag | 0 | "make the code better" |
| Nedefinit | 0 | "help me with the project" |

**Indicatori de specificitate:**
- Nume de fișiere menționate
- Funcții/clase specificate
- Erori concrete descrise
- Comportament dorit clar

---

### Criteriu 4: Completion Verificabilă (+1 punct)

**Întrebare:** Poate Claude să determine SINCER când task-ul e gata?

| Verificabilitate | Scor | Metodă |
|------------------|------|--------|
| Teste automate | +1 | `npm test` passes |
| Eroare dispare | +1 | no more errors in logs |
| Feature funcționează | +1 | manual verification possible |
| "Cod mai curat" | 0 | subiectiv, nu verificabil |
| "Mai bine" | 0 | nedefinit |

**Completion verificabilă când:**
- Teste pot confirma
- Erori pot fi verificate
- Output poate fi demonstrat
- Comportament poate fi observat

---

## Decizie Matrix

```
SCOR TOTAL:

4 puncte: AUTO-RALPH IMEDIAT
  - Task ideal pentru Ralph Loop
  - Exemplu: "fix the failing tests in auth module"

3 puncte: AUTO-RALPH
  - Task potrivit, poate necesita clarificare minoră
  - Exemplu: "implement user registration"

2 puncte: RĂSPUNS NORMAL (poate sugera Ralph)
  - Task posibil potrivit, dar lipsește ceva
  - Exemplu: "make the code better" (vag)

1-0 puncte: RĂSPUNS NORMAL
  - Task nepotrivit pentru Ralph
  - Exemplu: "explain how the auth works"
```

---

## Reguli de Override

### Force Ralph (ignoră scorul)
Când utilizatorul folosește trigger explicit:
- "ralph this"
- "auto ralph"
- "loop it"
- "iterate until done"
- "keep trying"

### Force Normal (chiar dacă scor mare)
Când utilizatorul cere explicit:
- "just answer"
- "don't loop"
- "one time"
- "explain first"

---

## Detecție Automată Context

### Ce detectăm și cum folosim:

| Context | Cum detectăm | Impact |
|---------|--------------|--------|
| Git dirty | `git status` | +specificity dacă fișiere relevante |
| Test framework | package.json, pytest.ini | +verifiability |
| Recent errors | npm-debug.log, error patterns | +criteria clare |
| Project type | file patterns | Selectează prompt pattern |

### Script detect-context.sh output:
```json
{
  "git": {
    "status": "M src/auth.ts\nM tests/auth.test.ts",
    "modified_files": ["src/auth.ts", "tests/auth.test.ts"],
    "recent_commits": ["fix: typo", "feat: add login"]
  },
  "tests": {
    "status": "npm test available"
  },
  "errors": "TypeError: Cannot read property...",
  "structure": "src/\nlib/\ntests/\npackage.json"
}
```

---

## Exemple Complete

### Exemplu 1: Scor 4 (AUTO-RALPH)

**Input:** "fix the auth bug, testele failează"

| Criteriu | Scor | Motiv |
|----------|------|-------|
| Criterii clare | +1 | "fix" + "testele failează" = succes când teste trec |
| Beneficiază iterație | +1 | Bug fix = iterativ |
| Scop definit | +1 | "auth" = locație |
| Verificabil | +1 | "testele" = verificare automată |
| **TOTAL** | **4** | **AUTO-RALPH** |

### Exemplu 2: Scor 2 (NORMAL)

**Input:** "make the code cleaner"

| Criteriu | Scor | Motiv |
|----------|------|-------|
| Criterii clare | 0 | "cleaner" = subiectiv |
| Beneficiază iterație | +1 | Refactoring = iterativ |
| Scop definit | 0 | Nu specifică ce cod |
| Verificabil | +1 | Poate rula teste existente |
| **TOTAL** | **2** | **NORMAL** (poate sugera Ralph dacă user clarifică) |

### Exemplu 3: Scor 0 (NORMAL)

**Input:** "ce face codul ăsta?"

| Criteriu | Scor | Motiv |
|----------|------|-------|
| Criterii clare | 0 | Întrebare, nu task |
| Beneficiază iterație | 0 | One-shot answer |
| Scop definit | 0 | "ăsta" = nedefinit |
| Verificabil | 0 | Nu e executabil |
| **TOTAL** | **0** | **NORMAL** |

---

## Language-Specific Keywords

### Română
- Pozitiv: repară, fix, adaugă, implementează, testează, refactorizează
- Negativ: explică, ce face, cum funcționează, ajută-mă să înțeleg

### Engleză
- Pozitiv: fix, add, implement, test, refactor, build, create
- Negativ: explain, what is, how does, help me understand

### Rusă
- Pozitiv: исправь, добавь, создай, сделай, протестируй
- Negativ: объясни, что это, как работает, помоги понять

### Mixed (common în Moldova)
Acceptă orice combinație. Scorul se calculează pe semantică, nu pe limbă.
