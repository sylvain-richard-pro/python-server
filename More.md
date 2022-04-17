# Next step.

*un peu de franglais* ;)


1. Premièrement.
- Définir de l'usage de ce service:
  - A quoi sert ce service? But du service.
  - Client Interne/Externe.
  - Nombre d'events par jour, par minutes.
  - Nombre d'appel linéaire ou avec des pics d'activitées.
- Prendre en compte les contraintes:
  - SLA Contrats de Service.
  - Technologies déjà utilisées par l'entreprise.

En fonction définir un niveau de sécurité attendu en fonction du budget alloué.
> (application, data, network, resilience, access, global view)

2. Définir l'architecture
- Faire loadtest pour dimensionner l'architecture (avoid SPOF)
- Etre en conformité avec DICT et TOGAF.
- Choix du hosting: IaaS, PaaS, SaaS, Serveur Physique, VM, Container
- Définir un GAP pour arriver à cette architecture.

# Axe d'amélioration

On défini les priorités des taches via les principes WoSCoW.
> M - Must have, S - Should have, C - Could have, W - Won't have. 

> Toutes ces priorités sont à discuter/adapter avec l'équipe.

## "Must Have" todolist:
- Décider d'une architecture cible avant de continuer.
- Discuss with team to get/exchange some ideas.
- Parametrage pour Flask de PROD.
- Tracabilité : tracing/audit
- Logging framework (to replace print usage ;)  )
- Securité SSL/Tls entre les differents composants: 
  - entre "Serveur Python" et Mongodb.
  - entre CLI et "Serveur Python".
- Protection du réseau avec un WAP, des firewalls, VNET isolés, BOT protection.

## "Should Have"
- Improve code / more control and better headling exception
- Use restFul API endpoint (currently look like WS)  /events/
  - Add swagger
- Secure access to WebAPI.
  - Protect backend with API Gateway.
  - Export to developper and with API Catalog 
- Declare Mongodb index on start_event (avoir une reflexion sur ce sujet)

## "Could Have"
- Add update method endpoint to update stop_event timestamp
- DevSecOps pipeline:
  - Top ten OWASP + Vulneranility scanner
  - control dependancy SCA /application
  - SAST sonarqube / SAST python bandit
  - DAST arachni

## "Won't have"
- Mongodb redondant. Elastic (tuning)
- python webAPI redondance Et tenir la charge. Multiple instance behind a LB. 
- securité user password/certificat dans un vault.
- CLI: écrire des CLI en python avec une meilleur gestion/présentation.
- IaC Ansible (rebuild secure architecture)


Any other ideas?
