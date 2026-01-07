# Exemplu: Bug Fix Prompt

## Input Original
```
User: "fix the auth bug, testele failează pe login"
```

## Scor Calculat
| Criteriu | Scor | Motiv |
|----------|------|-------|
| Criterii clare | +1 | "fix" + "testele failează" |
| Iterație utilă | +1 | Bug fixing = iterativ |
| Scop definit | +1 | "auth", "login" |
| Verificabil | +1 | "testele" = verificare automată |
| **TOTAL** | **4** | **AUTO-RALPH** |

## Context Detectat
```json
{
  "git": {
    "status": "M src/auth/login.ts\nM tests/auth.test.ts",
    "modified_files": ["src/auth/login.ts", "tests/auth.test.ts"]
  },
  "tests": {
    "status": "npm test available"
  },
  "errors": "TypeError: Cannot read property 'token' of undefined"
}
```

## Prompt Generat

```markdown
## Task
Repară bug-ul de autentificare: testele failează pe login.

## Context Detectat
- **Fișiere modificate:** src/auth/login.ts, tests/auth.test.ts
- **Framework test:** npm test disponibil
- **Eroare:** TypeError: Cannot read property 'token' of undefined

## Criterii de Succes
1. Eroarea "Cannot read property 'token'" nu mai apare
2. Toate testele din tests/auth.test.ts trec
3. Funcționalitatea de login merge corect
4. Nu s-au introdus regresii în alte teste

## Abordare
1. Analizează stack trace-ul pentru root cause
2. Identifică unde `token` e undefined
3. Implementează fix
4. Rulează `npm test` pentru verificare
5. Verifică că nu ai spart alte funcționalități

## Completion
Când bug-ul e COMPLET REZOLVAT și toate testele trec:
<promise>GATA</promise>

IMPORTANT: Output promise DOAR când:
- `npm test` trece fără erori
- Funcționalitatea de login merge
- Nu ai dubii despre fix

Pentru a anula loop-ul: /cancel-ralph
```

## Comanda Executată
```bash
/ralph-loop "..." --max-iterations 25 --completion-promise "GATA"
```

## Flow Complet

```
1. User: "fix the auth bug, testele failează pe login"
2. Skill: [Calculează scor 4/4]
3. Skill: [Rulează detect-context.sh]
4. Skill: [Generează prompt din template bug-fix]
5. Skill: "Prompt generat. Execut? [Da/Nu]"
6. User: [Da]
7. Skill: /ralph-loop "..." --max-iterations 25 --completion-promise "GATA"
8. Ralph Loop: [Iterează până când teste trec]
9. Claude: <promise>GATA</promise>
10. Loop ends.
```
