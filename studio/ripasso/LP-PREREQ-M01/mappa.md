# Mappa testuale — Fondamenti del primo modulo

Elaborato originale della sessione del 19 ottobre 2026, limitato alle unità 1–5. I riferimenti dettagliati sono negli appunti dello stesso blocco.

## Distribuzione fisica: quale guasto considero?

- Regione → area di distribuzione.
- Availability zone → separazione fisica dentro una regione.
- Più zone → verificare supporto e configurazione dei componenti.
- Perdita regionale → ragionare su recupero dell’intera applicazione.
- Region pair → associazione, senza disponibilità applicativa automatica.

## Organizzazione gestionale: dove applico le impostazioni?

```text
Management group
    ↓
Subscription
    ↓
Resource group
    ↓
Risorsa
```

- Scope ampio → effetto più esteso di policy e permessi.
- Scope dei permessi → limitare alle risorse da amministrare.
- Resource group → ciclo di vita; location e tag richiedono le precisazioni negli appunti.

## Le due verifiche della sessione

- Caso A, regola comune ai due gruppi → subscription: risposta confermata.
- Database replicato, applicazione soltanto nella regione persa → possibile indisponibilità: risposta confermata.
- Perché preferire B ad A? → motivazione e rinuncia ancora da esplicitare.

## Fonti e confini

[Infrastruttura fisica](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/5-describe-azure-physical-infrastructure), [gestione](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/6-describe-azure-management-infrastructure), [ARM](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview), [region pair](https://learn.microsoft.com/en-us/azure/reliability/regions-paired). Consultate il 19 ottobre 2026. Nessuna verifica di SKU, SLA o piano DR completo.
