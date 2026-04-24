# AlgoTech Club - Backend Microservices

Backend microservices pour la gestion des membres, evenements, reservations et notifications.

## 1) Vue d'ensemble

Services:
- `discovery-service` (Eureka Server, port `8761`)
- `api-gateway` (Gateway MVC, port `8080`)
- `member-service` (CRUD membres, port `8081`)
- `event-service` (CRUD evenements + validation trainer via Feign, port `8082`)
- `booking-service` (reservations + validation member/event + publication RabbitMQ, port `8083`)
- `notification-service` (consommation RabbitMQ + persistence logs, port `8084`)

Infrastructure:
- MySQL `8.4` sur `localhost:3308` (4 bases)
- RabbitMQ `3.13` sur `localhost:5672` (management `15672`)

## 2) Creation via Spring Initializr (de la base a l'etat actuel)

Chaque service a ete initialise via Spring Initializr (Maven, Jar, Java, package `com.algotech.club.*`) puis enrichi:

Parametres Initializr communs:
- Project: `Maven`
- Language: `Java`
- Packaging: `Jar`
- Group: `com.algotech.club`
- Artifact: nom du service (`discovery-service`, `member-service`, etc.)
- Name: nom du service
- Package name: adapte avec `_` (ex: `com.algotech.club.member_service`) car `-` est invalide en package Java
- Java: cible actuelle `25`

### discovery-service
- Initializr: `Actuator`, `Eureka Server`
- Ajout code: `@EnableEurekaServer`
- Role: registre de services

### api-gateway
- Initializr: `Actuator`, `Gateway`, `Eureka Discovery Client`
- Ajout config: routes `lb://...` et predicates `Path`
- Role: point d'entree unique

### member-service
- Initializr: `Web`, `Data JPA`, `Validation`, `Eureka Client`, `Actuator`
- Ajouts: entite `Member`, DTO/Mapper, API REST, OpenAPI (`springdoc`)
- Role: referentiel membres

### event-service
- Initializr: `Web`, `Data JPA`, `Validation`, `OpenFeign`, `Eureka Client`, `Actuator`
- Ajouts: `@EnableFeignClients`, validation trainer via `member-service`
- Role: gestion evenements

### booking-service
- Initializr: `Web`, `Data JPA`, `Validation`, `OpenFeign`, `AMQP`, `Eureka Client`, `Actuator`
- Ajouts: `@EnableFeignClients`, controle capacite event, publication RabbitMQ
- Role: gestion reservations + emission notifications async

### notification-service
- Initializr: `Web`, `Data JPA`, `AMQP`, `Eureka Client`, `Actuator`
- Ajouts: `@RabbitListener`, stockage des notifications dans `notification_logs`
- Role: reception et historisation des notifications

## 3) Versions et prerequis

Etat courant du projet:
- Java: `25`
- Spring Boot parent: `3.5.0`
- Spring Cloud BOM: `2025.0.0`
- Maven Compiler Plugin: `3.14.0`
- Lombok (annotation processor): `1.18.40`

Prerequis machine:
- JDK 25 actif dans `java -version` et `mvn -version`
- Maven 3.8+
- Docker + Docker Compose (pour MySQL et RabbitMQ)

## 4) Configuration critique par domaine

### 4.1 Enregistrement des services (Eureka)

`discovery-service/src/main/resources/application.yml`:
- `server.port: 8761`
- `spring.application.name: discovery-service`
- `eureka.client.register-with-eureka: false`
- `eureka.client.fetch-registry: false`

Tous les clients (gateway + services metier) pointent vers:
- `eureka.client.service-url.defaultZone: http://localhost:8761/eureka/`

Important:
- le nom logique de service vient de `spring.application.name`
- les routes Gateway utilisent ces noms (`lb://member-service`, etc.)

### 4.2 Base de donnees (MySQL)

Chaque service metier a sa base dediee:
- `member-service` -> `member_db`
- `event-service` -> `event_db`
- `booking-service` -> `booking_db`
- `notification-service` -> `notification_db`

Config commune (`application-dev.yml`):
- host: `localhost`
- port: `3308`
- user: `root`
- password: `password`
- `spring.jpa.hibernate.ddl-auto: update`

Script init SQL: `database/init.sql` (creation des 4 bases).

### 4.3 Gateway (routage)

`api-gateway/src/main/resources/application-dev.yml`:
- port `8080`
- routes:
  - `/api/members/**` -> `lb://member-service`
  - `/api/events/**` -> `lb://event-service`
  - `/api/bookings/**` -> `lb://booking-service`
  - `/api/notifications/**` -> `lb://notification-service`
- `spring.cloud.gateway.discovery.locator.enabled: true`

Note: la route `/api/notifications/**` est preconfiguree cote Gateway, mais aucun controller REST n'est expose actuellement dans `notification-service` (consommation RabbitMQ uniquement).

### 4.4 Communication inter-services (Feign)

- `event-service` -> `member-service` pour verifier le `trainerId`
- `booking-service` -> `member-service` et `event-service` pour valider la reservation

### 4.5 Messaging async (RabbitMQ)

`booking-service` publie une notification:
- Exchange: `algotech_exchange`
- Queue: `notification_queue`
- Routing key: `booking.routing.key`

`notification-service` consomme la meme queue via `@RabbitListener` et persiste en DB.

## 5) Profils et fichiers de config

Pattern utilise:
- `application.yml` -> nom service + `spring.profiles.active: dev` (sauf discovery)
- `application-dev.yml` -> ports, datasource, eureka, rabbitmq

## 6) Lancement local

Depuis la racine `backend/`:

```bash
./run-all.sh infra-up
./run-all.sh build
./run-all.sh start
./run-all.sh status
```

Arret:

```bash
./run-all.sh stop
./run-all.sh infra-down
```

Le script gere aussi `restart`, `logs`, et verifie Java 25+.

## 7) Demarrage manuel (ordre recommande)

1. `discovery-service`
2. `member-service`
3. `event-service`
4. `booking-service`
5. `notification-service`
6. `api-gateway`

Pourquoi cet ordre:
- Eureka doit etre pret avant l'enregistrement des clients
- `booking-service` depend de `member-service` + `event-service` + RabbitMQ

## 8) Endpoints principaux

Via gateway (`http://localhost:8080`):
- `POST /api/members`
- `GET /api/members`
- `GET /api/members/{id}`
- `POST /api/events`
- `GET /api/events`
- `GET /api/events/{id}`
- `POST /api/bookings`
- `GET /api/bookings/member/{memberId}`

Exemples payload:

```json
// POST /api/members
{
  "firstName": "Alice",
  "lastName": "Ngono",
  "email": "alice@example.com",
  "role": "TRAINER",
  "skills": "Java,Spring"
}
```

```json
// POST /api/events
{
  "title": "Spring Boot Masterclass",
  "description": "Session avancee",
  "eventDate": "2026-12-10T09:00:00",
  "location": "Douala",
  "trainerId": 1,
  "maxCapacity": 30
}
```

```json
// POST /api/bookings
{
  "memberId": 2,
  "eventId": 1
}
```

## 9) Verification rapide de l'architecture

- Eureka UI: `http://localhost:8761`
- Gateway health: `http://localhost:8080/actuator/health`
- RabbitMQ UI: `http://localhost:15672` (`user` / `password`)

Quand tout est OK:
- les 5 clients apparaissent enregistre dans Eureka
- une reservation cree une ligne dans `booking_db.bookings`
- `notification-service` consomme le message et cree une ligne dans `notification_db.notification_logs`

## 10) Points d'attention / troubleshooting

- Erreur `Unsupported class file major version 69`:
  - cause: framework trop ancien pour Java 25
  - etat corrige: Boot `3.5.0` + Cloud `2025.0.0`

- Service absent dans Eureka:
  - verifier `spring.application.name`
  - verifier `defaultZone` et ordre de demarrage

- Echec DB:
  - verifier MySQL `3308` et credentials `root/password`
  - verifier que `database/init.sql` a cree les bases

- Echec notifications:
  - verifier RabbitMQ `5672`
  - verifier constantes `EXCHANGE`, `QUEUE_NOTIFICATION`, `ROUTING_KEY` identiques dans booking/notification
