# Exemplu: Feature Implementation Prompt

## Input Original
```
User: "implement user registration with email verification"
```

## Scor Calculat
| Criteriu | Scor | Motiv |
|----------|------|-------|
| Criterii clare | +1 | "implement" = task executabil |
| Iterație utilă | +1 | Feature building = iterativ |
| Scop definit | +1 | "user registration", "email verification" |
| Verificabil | +1 | Poate fi testat |
| **TOTAL** | **4** | **AUTO-RALPH** |

## Context Detectat
```json
{
  "git": {
    "status": "clean",
    "modified_files": []
  },
  "tests": {
    "status": "npm test available; jest configured"
  },
  "structure": "src/\n  auth/\n  users/\n  utils/\npackage.json"
}
```

## Prompt Generat

```markdown
## Task
Implementează user registration cu email verification.

## Context Detectat
- **Structură proiect:** Node.js cu src/auth/, src/users/
- **Framework test:** Jest disponibil
- **Pattern existent:** Auth logic în src/auth/

## Criterii de Succes
1. Endpoint POST /api/users/register funcțional
2. Validare input (email, password requirements)
3. Email verification token generat și stocat
4. Email trimis utilizatorului (sau mock în dev)
5. Endpoint pentru verificare token
6. Teste complete pentru toate scenariile
7. Error handling pentru cazuri edge

## Abordare Incrementală
### Faza 1: Basics
1. Creează endpoint POST /api/users/register
2. Adaugă validare input
3. Scrie teste pentru happy path

### Faza 2: Email Verification
4. Generează verification token
5. Stochează token în DB
6. Implementează email sending (mock pentru dev)
7. Teste pentru flow verificare

### Faza 3: Verification Endpoint
8. Creează GET /api/users/verify/:token
9. Validează și activează user
10. Teste pentru scenarii edge

### Faza 4: Final
11. Rulează toate testele
12. Verifică integration
13. Clean up și documentare

## Completion
Când TOATE criteriile sunt îndeplinite și testele trec:
<promise>GATA</promise>

IMPORTANT: Output promise DOAR când:
- Registration funcționează end-to-end
- Email verification flow complet
- Toate testele trec
- Error handling implementat

Pentru a anula loop-ul: /cancel-ralph
```

## Comanda Executată
```bash
/ralph-loop "..." --max-iterations 35 --completion-promise "GATA"
```

**Notă:** Feature complex = max iterations mai mare (35 în loc de 25).

## Rezultat Așteptat

După multiple iterații, Ralph va:
1. Crea fișierele necesare
2. Implementa registration
3. Adăuga email verification
4. Scrie teste
5. Rula teste și fixa erorile
6. Output `<promise>GATA</promise>` când totul merge
