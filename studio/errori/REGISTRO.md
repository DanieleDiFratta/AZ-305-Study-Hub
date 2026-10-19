# Registro degli errori personali

Prima verifica del 19 ottobre 2026: punti incompleti da consolidare. Le risposte sintetiche non dimostrano da sole convinzioni errate; i richiami sotto servono a chiarirle. Le lacune della biblioteca sono nel [registro delle fonti](../../docs/LACUNE-E-AGGIORNAMENTI.md) e non devono essere attribuite all’utente.

| Data | Obiettivo | Situazione / evidenza | Ragionamento da correggere | Fonte | Prossima verifica | Esito |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-19 | 1.3.1, fondamenti | B scelta «per ereditare regole aziendali» | Motivazione non discriminante: anche A consente ereditarietà dalla subscription ai gruppi; esplicitare requisito e rinuncia di B | [ARM scope](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview#understand-scope) | Quale beneficio concreto richiede subscription separate? | Ereditarietà in A confermata con «alla subscription»; motivazione e rinuncia di B ancora da approfondire |
| 2026-10-19 | 3.2.1, fondamenti | Alla perdita regionale risponde «la region pair» | Piano di recupero non esplicitato; non attribuire automaticamente la convinzione di failover automatico | [Region pairs](https://learn.microsoft.com/en-us/azure/reliability/regions-paired) | Se solo il database è replicato, cosa manca all’applicazione? | Risposta corretta: applicazione indisponibile nella regione persa. Distinzione confermata; piano DR completo non verificato |
