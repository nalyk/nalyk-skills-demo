# Exemplu: Refactoring Prompt

## Input Original
```
User: "refactorizează utils.js, e prea mare și dezorganizat"
```

## Scor Calculat
| Criteriu | Scor | Motiv |
|----------|------|-------|
| Criterii clare | +1 | "refactorizează" = acțiune clară |
| Iterație utilă | +1 | Refactoring = incremental |
| Scop definit | +1 | "utils.js" specificat |
| Verificabil | +1 | Teste existente pot verifica non-regresie |
| **TOTAL** | **4** | **AUTO-RALPH** |

## Context Detectat
```json
{
  "git": {
    "status": "clean",
    "modified_files": []
  },
  "tests": {
    "status": "npm test available"
  },
  "structure": "src/\n  utils.js (450 lines)\ntests/\n  utils.test.js"
}
```

## Prompt Generat

```markdown
## Task
Refactorizează utils.js - e prea mare și dezorganizat.

## Context Detectat
- **Fișier target:** src/utils.js (450 linii)
- **Teste existente:** tests/utils.test.js
- **Framework test:** npm test disponibil

## Criterii de Succes
1. utils.js împărțit în module logice
2. TOATE testele existente trec (ZERO regresii!)
3. Imports actualizate în fișierele care folosesc utils
4. Cod mai ușor de citit și menținut
5. Funcționalitate IDENTICĂ

## Abordare
### PRE-REFACTOR
1. Rulează `npm test` - salvează baseline
2. Identifică funcțiile din utils.js
3. Grupează pe categorii (string utils, date utils, etc.)

### REFACTOR INCREMENTAL
4. Creează primul modul (ex: src/utils/strings.js)
5. Mută funcțiile relevante
6. Actualizează imports
7. Rulează teste - TREBUIE să treacă
8. Repetă pentru fiecare categorie

### POST-REFACTOR
9. Verifică că utils.js original poate fi șters
10. Rulează toate testele final
11. Verifică că nu ai spart nimic

## Reguli Stricte
- NICIO schimbare de funcționalitate
- Teste TREBUIE să treacă după fiecare pas
- Dacă un test failează, UNDO și reîncearcă diferit
- Păstrează backward compatibility pentru imports

## Completion
Când refactoring-ul e COMPLET și toate testele trec:
<promise>GATA</promise>

IMPORTANT: Output promise DOAR când:
- `npm test` trece 100%
- Structura e îmbunătățită
- Zero funcționalitate schimbată
- Zero regresii

ATENȚIE: NU output promise dacă ORICE test failează!

Pentru a anula loop-ul: /cancel-ralph
```

## Comanda Executată
```bash
/ralph-loop "..." --max-iterations 25 --completion-promise "GATA"
```

## Rezultat Așteptat

```
src/
  utils/
    index.js       (re-exports pentru backward compatibility)
    strings.js     (string utilities)
    dates.js       (date utilities)
    arrays.js      (array utilities)
    validation.js  (validation helpers)

tests/
  utils/
    strings.test.js
    dates.test.js
    ...
```

## Note pentru Refactoring

1. **Backward Compatibility:**
   ```javascript
   // src/utils/index.js
   export * from './strings.js';
   export * from './dates.js';
   // etc.
   ```
   Astfel codul existent care importă din `utils` continuă să funcționeze.

2. **Iterativ:**
   Ralph va face câte un pas, rula teste, continua dacă trec.

3. **Safe:**
   Dacă ceva se strică, Ralph vede testele failed și corectează.
