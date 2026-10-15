"""Curated scope, original concise objective labels, and candidate official URLs.

Candidate URLs acquire verified status only after a successful research.py GET and content review.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
BASE = 'https://learn.microsoft.com/en-us/'
GROUPS = [
 ('1.1', 'Osservabilità', ['Scelta logging', 'Instradamento log', 'Scelta monitoraggio']),
 ('1.2', 'Identità e accessi', ['Autenticazione', 'Gestione identità', 'Autorizzazione Azure', 'Autorizzazione on-premises', 'Segreti, certificati, chiavi']),
 ('1.3', 'Governance', ['Gerarchie e tagging', 'Conformità', 'Governance identità']),
 ('2.1', 'Dati relazionali', ['Persistenza relazionale', 'Tier database/compute', 'Scalabilità database', 'Protezione dati relazionali']),
 ('2.2', 'Dati non relazionali', ['Persistenza semistrutturata', 'Persistenza non strutturata', 'Funzionalità/prestazioni/costi storage', 'Protezione/durabilità storage']),
 ('2.3', 'Integrazione dati', ['Integrazione dati', 'Analisi dati']),
 ('3.1', 'Backup e ripristino', ['Recupero Azure/ibrido', 'Backup/recupero compute', 'Backup/recupero database', 'Backup/recupero oggetti']),
 ('3.2', 'Alta disponibilità', ['Disponibilità compute', 'Disponibilità relazionale', 'Disponibilità non relazionale']),
 ('4.1', 'Compute', ['Componenti per workload', 'Macchine virtuali', 'Container', 'Serverless', 'Elaborazione batch']),
 ('4.2', 'Architettura applicativa', ['Messaggistica', 'Architetture event-driven', 'Integrazione API', 'Caching applicativo', 'Configurazione applicativa', 'Deployment automatizzato']),
 ('4.3', 'Migrazioni', ['Migrazione con CAF', 'Assessment on-premises', 'Migrazione IaaS/PaaS', 'Migrazione database', 'Migrazione oggetti']),
 ('4.4', 'Reti', ['Connettività internet', 'Connettività ibrida', 'Prestazioni rete', 'Sicurezza rete', 'Bilanciamento e routing']),
]
ANCHORS = ['design-solutions-for-logging-and-monitoring', 'design-authentication-and-authorization-solutions',
           'design-governance', 'design-data-storage-solutions-for-relational-data',
           'design-data-storage-solutions-for-semi-structured-and-unstructured-data', 'design-data-integration',
           'design-solutions-for-backup-and-disaster-recovery', 'design-for-high-availability',
           'design-compute-solutions', 'design-an-application-architecture', 'design-migrations', 'design-network-solutions']
guide = BASE + 'credentials/certifications/resources/study-guides/az-305'
objectives = []
for (group, title, labels), anchor in zip(GROUPS, ANCHORS):
    for i, label in enumerate(labels, 1):
        objectives.append({'id': f'{group}.{i}', 'domain': group[0], 'group': group, 'label_it': label,
                           'source_id': 'EXAM-GUIDE', 'source_url': guide + '#' + anchor,
                           'source_bullet_ordinal': i, 'label_type': 'original_concise_paraphrase',
                           'learning_status': 'not_started'})
(DATA / 'objectives.json').write_text(json.dumps({'exam': 'AZ-305', 'skills_effective_on': '2026-04-17',
    'guide_last_updated_on': '2026-03-19', 'verified_on': '2026-10-15',
    'domains': [{'id': '1', 'label_it': 'Identità, governance, monitoraggio', 'weight': '25–30%'},
                {'id': '2', 'label_it': 'Storage', 'weight': '20–25%'},
                {'id': '3', 'label_it': 'Continuità operativa', 'weight': '15–20%'},
                {'id': '4', 'label_it': 'Infrastruttura', 'weight': '30–35%'}],
    'groups': [{'id': g, 'label_it': t, 'expected_bullets': len(ls), 'source_anchor': a} for (g,t,ls),a in zip(GROUPS,ANCHORS)],
    'objectives': objectives}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def ids(value):
    return value.split() if value else []

seeds = []
def add(rid, path, kind, mapping='', why='', days=60):
    seeds.append({'id': rid, 'url': path if path.startswith('https://') else BASE + path,
                  'kind': kind, 'objective_ids': ids(mapping), 'mapping_scope': 'direct' if mapping else 'reference',
                  'selection_reason_it': why, 'recheck_days': days,
                  'review_status': 'pending_content_review'})

add('EXAM-GUIDE', guide, 'exam_guide', why='Baseline del programma; ogni ID locale corrisponde a un bullet tramite sezione e posizione.', days=30)
add('EXAM-CERT', 'credentials/certifications/azure-solutions-architect/', 'exam', why='Distinguere superamento AZ-305 da requisiti della certificazione Expert.', days=30)
add('EXAM-COURSE', 'training/courses/az-305t00', 'course', why='Perimetro ufficiale dei percorsi da censire.', days=30)
for rid, slug, mapping in [
 ('LP-PREREQ','microsoft-azure-architect-design-prerequisites',''),
 ('LP-IDENTITY','design-identity-governance-monitor-solutions',''),
 ('LP-DATA','design-data-storage-solutions',''),
 ('LP-BCDR','design-business-continuity-solutions',''),
 ('LP-INFRA','design-infranstructure-solutions',''),
 ('LP-WAF','azure-well-architected-framework','')]:
    add(rid, 'training/paths/'+slug+'/', 'learn_path', mapping, 'Percorso incluso nel syllabus ufficiale AZ-305T00; inventario ricorsivo di moduli e unità.', 60)

# Logging, monitoring, identity, governance: direct coverage for each atomic objective.
DOCS = [
 ('MON-OVERVIEW','azure/azure-monitor/overview','1.1.1 1.1.3','Confini di log, metriche, tracing e servizi di osservabilità.'),
 ('MON-WORKSPACES','azure/azure-monitor/logs/workspace-design','1.1.1','Scelta di workspace, isolamento, costi e retention.'),
 ('MON-DIAGNOSTIC','azure/azure-monitor/platform/diagnostic-settings','1.1.2','Destinazioni e vincoli dei log delle risorse.'),
 ('MON-DCR','azure/azure-monitor/data-collection/data-collection-rule-overview','1.1.2','Raccolta e trasformazione con DCR; distinguere diagnostic settings.'),
 ('MON-APPINSIGHTS','azure/azure-monitor/app/app-insights-overview','1.1.3','Telemetria applicativa e correlazione delle dipendenze.'),
 ('MON-ALERTS','azure/azure-monitor/alerts/alerts-overview','1.1.3','Scelta tra alert metrici e basati su log.'),
 ('ID-AUTH','entra/identity/hybrid/connect/choose-ad-authn','1.2.1 1.2.2','Confronto architetturale fra PHS, PTA e federazione.'),
 ('ID-CA','entra/identity/conditional-access/overview','1.2.1','Accesso condizionale e segnali di rischio.'),
 ('ID-MANAGED','entra/identity/managed-identities-azure-resources/overview','1.2.2 1.2.3','Identità di workload e accesso senza credenziali gestite in applicazione.'),
 ('ID-EXTERNAL','entra/external-id/external-identities-overview','1.2.1 1.2.2','Distinguere workforce B2B e customer identity.'),
 ('ID-RBAC','azure/role-based-access-control/overview','1.2.3','Scope, ruoli e autorizzazioni del piano Azure.'),
 ('ID-ONPREM','entra/identity/app-proxy/overview-what-is-app-proxy','1.2.4','Pubblicazione protetta e accesso alle applicazioni on-premises.'),
 ('ID-DOMAIN','entra/identity/domain-services/overview','1.2.1 1.2.4','Kerberos/LDAP e applicazioni dipendenti da dominio.'),
 ('ID-KEYVAULT','azure/key-vault/general/basic-concepts','1.2.5','Separare segreti, chiavi e certificati; scenari di servizio.'),
 ('GOV-HIERARCHY','azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org','1.3.1','Gerarchia per delega, isolamento e organizzazione.'),
 ('GOV-TAGS','azure/azure-resource-manager/management/tag-resources','1.3.1','Strategia tagging e limiti operativi.'),
 ('GOV-POLICY','azure/governance/policy/overview','1.3.2','Policy, iniziative ed enforcement della conformità.'),
 ('GOV-IDENTITY','entra/id-governance/identity-governance-overview','1.3.3','Ciclo di vita e governance degli accessi.'),
 ('GOV-PIM','entra/id-governance/privileged-identity-management/pim-configure','1.3.3','Accesso privilegiato temporaneo e controllato.'),
 ('GOV-REVIEWS','entra/id-governance/access-reviews-overview','1.3.3','Revisione periodica degli accessi.'),
 ('DATA-SQL-CHOICE','azure/azure-sql/azure-sql-iaas-vs-paas-what-is-overview','2.1.1 4.3.4','Confronto SQL Database, Managed Instance e SQL su VM.'),
 ('DATA-POSTGRES','azure/postgresql/flexible-server/overview','2.1.1','Alternativa relazionale gestita per motore PostgreSQL.'),
 ('DATA-MYSQL','azure/mysql/flexible-server/overview','2.1.1','Alternativa relazionale gestita per motore MySQL.'),
 ('DATA-SQL-TIERS','azure/azure-sql/database/service-tiers-vcore','2.1.2','General Purpose, Business Critical e Hyperscale.'),
 ('DATA-SQL-DTU','azure/azure-sql/database/service-tiers-dtu','2.1.2','Modello DTU da confrontare con vCore in base ai requisiti.'),
 ('DATA-SQL-SERVERLESS','azure/azure-sql/database/serverless-tier-overview','2.1.2 2.1.3','Provisioned/serverless e scaling del compute.'),
 ('DATA-SQL-POOLS','azure/azure-sql/database/elastic-pool-overview','2.1.3','Condivisione risorse per database con picchi differenti.'),
 ('DATA-SQL-HYPERSCALE','azure/azure-sql/database/service-tier-hyperscale','2.1.2 2.1.3','Scalabilità e vincoli specifici Hyperscale.'),
 ('DATA-SQL-SECURITY','azure/azure-sql/database/security-overview','2.1.4','Accesso, rete, auditing e protezione crittografica.'),
 ('DATA-COSMOS-CHOICE','azure/cosmos-db/introduction','2.2.1','Modello e caratteristiche Cosmos DB; integrare con confronto dei data model.'),
 ('DATA-TABLE-CHOICE','azure/cosmos-db/table/support','2.2.1','Tabella comparativa Table Storage e servizio Table Cosmos DB.'),
 ('DATA-STORE-CHOICE','azure/architecture/guide/technology-choices/data-store-overview','2.1.1 2.2.1 2.2.2 2.2.3','Decisioni guidate dal modello di accesso, consistenza e operatività.'),
 ('DATA-BLOB','azure/storage/blobs/storage-blobs-overview','2.2.2','Object storage e modelli di utilizzo.'),
 ('DATA-FILES','azure/storage/files/storage-files-introduction','2.2.2','File share gestite e requisiti SMB/NFS.'),
 ('DATA-BLOB-TIERS','azure/storage/blobs/access-tiers-overview','2.2.3','Access tier, frequenza letture e recupero dati.'),
 ('DATA-PREMIUM','azure/storage/blobs/storage-blob-block-blob-premium','2.2.3','Prestazioni e casi per block blob premium.'),
 ('DATA-REDUNDANCY','azure/storage/common/storage-redundancy','2.2.4 3.2.3','LRS/ZRS/GRS/GZRS, durabilità e disponibilità.'),
 ('DATA-PROTECTION','azure/storage/blobs/data-protection-overview','2.2.4 3.1.4','Versioni, eliminazione temporanea, immutabilità e backup.'),
 ('DATA-STORAGE-SECURITY','azure/storage/common/storage-service-encryption','2.2.4','Crittografia e gestione delle chiavi per Storage.'),
 ('DATA-ADF','azure/data-factory/introduction','2.3.1','Orchestrazione e integrazione batch/ibrida.'),
 ('DATA-ADF-SSIS','azure/data-factory/concepts-integration-runtime','2.3.1','Runtime Azure, self-hosted e SSIS.'),
 ('DATA-ANALYTICS-CHOICE','azure/architecture/data-guide/technology-choices/analytical-data-stores','2.3.2','Confronto architetturale degli store analitici.'),
 ('DATA-SYNAPSE','azure/synapse-analytics/overview-what-is','2.3.1 2.3.2','Analisi integrata e componenti Synapse.'),
 ('DATA-DATABRICKS','azure/databricks/introduction/','2.3.1 2.3.2','Lakehouse e workload di analisi.'),
 ('DATA-STREAM','azure/stream-analytics/stream-analytics-introduction','2.3.2','Analisi streaming e confronto col batch.'),
 ('DATA-LAKE','azure/storage/blobs/data-lake-storage-introduction','2.2.2 2.3.1 2.3.2','Gerarchia e storage per analytics.'),
 ('BCDR-OBJECTIVES','azure/well-architected/reliability/metrics','3.1.1','Definire RTO/RPO e verificarli sul workload completo.'),
 ('BCDR-ASR','azure/site-recovery/site-recovery-overview','3.1.1 3.1.2','Disaster recovery per VM Azure e workload ibridi.'),
 ('BCDR-BACKUP-MATRIX','azure/backup/backup-support-matrix','3.1.2 3.1.3 3.1.4','Matrice di supporto per workload e limiti del backup.'),
 ('BCDR-VM','azure/backup/backup-azure-vms-introduction','3.1.2','Backup VM e comportamento del ripristino.'),
 ('BCDR-SQL','azure/azure-sql/database/automated-backups-overview','2.1.4 3.1.3','PITR/LTR e caratteristiche dei backup SQL gestiti.'),
 ('BCDR-SQLVM','azure/backup/backup-azure-sql-database','3.1.3','Backup application-aware di SQL Server su VM.'),
 ('BCDR-COSMOS','azure/cosmos-db/continuous-backup-restore-introduction','3.1.3','Backup continuo e ripristino puntuale Cosmos DB.'),
 ('BCDR-BLOB','azure/backup/blob-backup-overview','3.1.4','Backup operativo e vaulted di blob.'),
 ('BCDR-FILES','azure/backup/azure-file-share-backup-overview','3.1.4','Backup e ripristino delle condivisioni file.'),
 ('HA-VM','azure/virtual-machines/availability','3.2.1','Zone, availability set e failure domain.'),
 ('HA-APP','azure/reliability/reliability-app-service','3.2.1','Affidabilità di App Service, zone e regioni.'),
 ('HA-AKS','azure/reliability/reliability-aks','3.2.1','Affidabilità AKS e responsabilità del workload.'),
 ('HA-SQL','azure/azure-sql/database/high-availability-sla','3.2.2','Alta disponibilità SQL per tier e zone.'),
 ('HA-SQL-GEO','azure/azure-sql/database/failover-group-sql-db','3.1.3 3.2.2','Continuità geografica e failover SQL.'),
 ('HA-POSTGRES','azure/reliability/reliability-database-postgresql','3.2.2','Alta disponibilità per PostgreSQL gestito.'),
 ('HA-COSMOS','azure/cosmos-db/high-availability','3.2.3','Distribuzione geografica e disponibilità Cosmos DB.'),
 ('HA-COSMOS-CONSISTENCY','azure/cosmos-db/consistency-levels','2.2.1 3.2.3','Compromessi consistenza, disponibilità e latenza.'),
 ('COMP-CHOICE','azure/architecture/guide/technology-choices/compute-decision-tree','4.1.1','Albero decisionale per scegliere il modello compute.'),
 ('COMP-VMSS','azure/virtual-machine-scale-sets/overview','4.1.2','VM Scale Sets e modelli di orchestrazione.'),
 ('COMP-CONTAINERS','azure/architecture/guide/choose-azure-container-service','4.1.3','Confronto AKS, Container Apps e Container Instances.'),
 ('COMP-ACA','azure/container-apps/overview','4.1.3 4.1.4','Hosting gestito per servizi e job containerizzati.'),
 ('COMP-FUNCTIONS','azure/azure-functions/functions-scale','4.1.4','Scelta del piano Functions per scaling e rete.'),
 ('COMP-LOGIC','azure/logic-apps/logic-apps-overview','4.1.4','Orchestrazione serverless e integrazione.'),
 ('COMP-BATCH','azure/batch/batch-technical-overview','4.1.5','Pool, job e task per elaborazione parallela.'),
 ('APP-MESSAGING','azure/service-bus-messaging/compare-messaging-services','4.2.1 4.2.2','Service Bus, Event Grid ed Event Hubs a confronto.'),
 ('APP-SERVICEBUS','azure/service-bus-messaging/service-bus-messaging-overview','4.2.1','Code, topic, transazioni e semantica di consegna.'),
 ('APP-EVENT-STYLE','azure/architecture/guide/architecture-styles/event-driven','4.2.2','Produttori/consumatori e compromessi event-driven.'),
 ('APP-EVENTHUBS','azure/event-hubs/event-hubs-about','4.2.2','Streaming, partizioni e consumer group.'),
 ('APP-APIM','azure/api-management/api-management-key-concepts','4.2.3','Gateway, policy e integrazione delle API.'),
 ('APP-CACHE-PATTERN','azure/architecture/patterns/cache-aside','4.2.4','Cache-aside, invalidazione e coerenza.'),
 ('APP-REDIS','azure/redis/overview','4.2.4','Servizio attuale per caching Redis gestito.'),
 ('APP-CONFIG','azure/azure-app-configuration/overview','4.2.5','Configurazioni condivise e feature flag.'),
 ('APP-DEPLOY','azure/architecture/microservices/ci-cd','4.2.6','Confronto pipeline CI/CD e GitOps sul workload.'),
 ('APP-BICEP','azure/azure-resource-manager/bicep/overview','4.2.6','Deployment dichiarativo dell’infrastruttura.'),
 ('APP-SLOTS','azure/app-service/deploy-staging-slots','4.2.6','Strategia di rilascio e swap applicativo.'),
 ('MIG-CAF','azure/cloud-adoption-framework/migrate/','4.3.1','Metodo di migrazione con vincoli organizzativi e tecnici.'),
 ('MIG-ASSESS','azure/migrate/migrate-services-overview','4.3.2 4.3.3','Discovery, assessment e migrazione di workload.'),
 ('MIG-SERVER','azure/migrate/server-migrate-overview','4.3.3','Migrazione dei server e opzioni operative.'),
 ('MIG-DATABASE','azure/dms/dms-tools-matrix','4.3.4','Matrice attuale degli strumenti per sorgente e destinazione.'),
 ('MIG-STORAGE','azure/storage/common/storage-migration-overview','4.3.5','Scelta degli strumenti di migrazione dello storage.'),
 ('MIG-AZCOPY','azure/storage/common/storage-use-azcopy-v10','4.3.5','Trasferimenti online e caratteristiche AzCopy.'),
 ('MIG-DATABOX','azure/databox/data-box-overview','4.3.5','Trasferimento offline e vincoli logistici.'),
 ('NET-CHOICE','azure/architecture/networking/get-started','4.4.1 4.4.2 4.4.3 4.4.4','Scelte di topologia e connettività; orientamento, non fonte primaria per i dettagli.'),
 ('NET-OUTBOUND','azure/virtual-network/ip-services/default-outbound-access','4.4.1','Uscita esplicita e modifiche dei default di rete.'),
 ('NET-NAT','azure/nat-gateway/nat-overview','4.4.1 4.4.3','SNAT, connessioni e progettazione outbound.'),
 ('NET-HYBRID','azure/architecture/reference-architectures/hybrid-networking/','4.4.2','Confronto VPN ed ExpressRoute per reti ibride.'),
 ('NET-EXPRESSROUTE','azure/expressroute/design-architecture-for-resiliency','4.4.2 4.4.3','Ridondanza dei circuiti e connettività resiliente.'),
 ('NET-PEERING','azure/virtual-network/virtual-network-peering-overview','4.4.3','Peering e vincoli di transito.'),
 ('NET-FIREWALL','azure/firewall/overview','4.4.4','Controllo centralizzato del traffico.'),
 ('NET-PRIVATE','azure/private-link/private-endpoint-overview','4.4.4','Private endpoint, isolamento e implicazioni DNS.'),
 ('NET-DNS','azure/private-link/private-endpoint-dns-integration','4.4.4','Risoluzione privata in topologie ibride.'),
 ('NET-DDOS','azure/ddos-protection/ddos-protection-overview','4.4.4','Protezione dagli attacchi di rete.'),
 ('NET-LB-CHOICE','azure/architecture/guide/technology-choices/load-balancing-overview','4.4.5','Scelta L4/L7 e regionale/globale.'),
 ('NET-FRONTDOOR','azure/frontdoor/front-door-overview','4.4.3 4.4.5','Routing globale e accelerazione HTTP.'),
 ('NET-APPGW','azure/application-gateway/overview','4.4.5','Delivery L7 regionale e integrazione WAF.'),
 ('NET-LB','azure/load-balancer/load-balancer-overview','4.4.5','Bilanciamento L4 e sonde.'),
]
for rid, path, mapping, why in DOCS:
    kind = 'comparison' if any(x in rid for x in ('CHOICE', 'TIERS', 'MATRIX', 'AUTH')) or rid == 'APP-MESSAGING' else 'documentation'
    add(rid, path, kind, mapping, why)

for rid, path, mapping, why in [
 ('WAF-HOME','azure/well-architected/','', 'Quadro delle decisioni e delle revisioni di workload.'),
 ('WAF-RELIABILITY','azure/well-architected/reliability/','3.1.1 3.2.1 3.2.2 3.2.3','Resilienza e revisione dei failure mode.'),
 ('WAF-SECURITY','azure/well-architected/security/','1.2.1 1.2.3 1.2.5 4.4.4','Decisioni di sicurezza e responsabilità.'),
 ('WAF-COST','azure/well-architected/cost-optimization/','2.1.2 2.2.3 4.1.1','Trade-off economici delle alternative.'),
 ('WAF-PERFORMANCE','azure/well-architected/performance-efficiency/','2.1.3 4.1.1 4.4.3','Capacity planning e colli di bottiglia.'),
 ('WAF-OPERATIONS','azure/well-architected/operational-excellence/','1.1.3 4.2.6','Operabilità e deployment affidabile.'),
 ('CAF-HOME','azure/cloud-adoption-framework/','4.3.1','Organizzazione dell’adozione del cloud.'),
 ('CAF-LZ','azure/cloud-adoption-framework/ready/landing-zone/','1.3.1 1.3.2 4.4.2','Fondazione di piattaforma per workload.'),
 ('ARC-WEB','azure/architecture/web-apps/app-service/architectures/baseline-zone-redundant','3.2.1 4.1.4 4.4.5','Caso progettuale con diagramma: applicazione web affidabile.'),
 ('ARC-AKS','azure/architecture/reference-architectures/containers/aks/baseline-aks','3.2.1 4.1.3 4.4.4','Caso progettuale con diagramma: piattaforma AKS.'),
 ('ARC-HUB','azure/architecture/networking/architecture/hub-spoke','1.3.1 4.4.2 4.4.4','Caso progettuale con diagramma: rete hub-spoke.'),
 ('ARC-DR','azure/architecture/web-apps/guides/multi-region-app-service/multi-region-app-service','3.1.1 3.2.1 4.4.5','Caso progettuale con diagramma: servizio web multiregione.'),
 ('ARC-DATA','azure/architecture/data-guide/relational-data/etl','2.3.1 2.3.2','Caso progettuale con diagramma: pipeline dati.'),
 ('LIFE-REDIS','azure/azure-cache-for-redis/retirement-faq','4.2.4','Registro di ritiro del servizio e migrazione verso Managed Redis.'),
 ('LIFE-REDIS-NEWS','azure/azure-cache-for-redis/cache-whats-new','4.2.4','Cronologia: rimozione del blocco per clienti esistenti nel luglio 2026.'),
 ('LIFE-B2C','azure/active-directory-b2c/faq','1.2.1 1.2.2','Limiti commerciali B2C e distinzione da External ID.'),
 ('LIFE-ADS','azure-data-studio/whats-happening-azure-data-studio','4.3.4','Verifica dello stato di Azure Data Studio.'),
 ('LIFE-LB','azure/load-balancer/skus','4.4.5','Confronto SKU e stato del Basic Load Balancer.'),
 ('LIFE-MONITOR','azure/azure-monitor/agents/azure-monitor-agent-migration','1.1.1 1.1.2','Agenti moderni e migrazione dal legacy.'),
 ('LAB-CASESTUDIES','https://github.com/MicrosoftLearning/AZ-305-DesigningMicrosoftAzureInfrastructureSolutions','official_exercises','Repository MicrosoftLearning di casi ed esercizi, da usare con le fonti attuali.'),
]:
    if rid.startswith('LIFE-'):
        kind = 'lifecycle'
    elif rid.startswith('ARC-'):
        kind = 'reference_architecture'
    elif rid.startswith('WAF-'):
        kind = 'well_architected'
    elif rid.startswith('CAF-'):
        kind = 'cloud_adoption'
    else:
        kind = 'official_exercises'
    add(rid, path, kind, '' if mapping == 'official_exercises' else mapping, why, 30 if kind == 'lifecycle' else 60)

add('CASE-AWARE', 'https://www.microsoft.com/en/customers/story/1610015881656149117-aware-partner-professional-services-azure-cosmos-db', 'customer_story',
    '2.1.1 2.2.1 2.3.2', 'Caso reale Microsoft: scelta combinata PostgreSQL/Cosmos DB. Evidenza narrativa, non specifica tecnica.', 90)
add('LAB-INDEX', 'https://microsoftlearning.github.io/AZ-305-DesigningMicrosoftAzureInfrastructureSolutions/', 'official_exercises',
    '', 'Indice pubblico dei casi MicrosoftLearning, collegato dal readme ufficiale. Verificare attualità dei singoli casi.', 60)

(DATA / 'seeds.json').write_text(json.dumps(seeds, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{len(objectives)} objectives; {len(seeds)} candidate resources')
