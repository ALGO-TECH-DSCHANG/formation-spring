# AlgoTech Hub - Documentation Projet

AlgoTech Hub est une application microservices Spring Boot pour gérer un club (membres, événements, réservations) avec communication synchrone (OpenFeign) et asynchrone (RabbitMQ).

## 1. Vue d'ensemble

### Services
- `discovery-service` : registre Eureka (`:8761`)
- `api-gateway` : point d'entrée unique (`:8080` en local, `:8888` via Docker host)
- `member-service` : gestion des membres (`:8081`)
- `event-service` : gestion des événements (`:8082`)
- `booking-service` : gestion des réservations (`:8083`)
- `notification-service` : consommation RabbitMQ + persistance des notifications (`:8084`)

### Infrastructure
- MySQL 8 (4 bases)
- RabbitMQ (broker + management UI)
- Eureka (service discovery)

### Flux fonctionnel
1. Création d'un membre (trainer + student)
2. Création d'un événement (validation du `trainerId` via `member-service`)
3. Création d'une réservation (validation member/event via Feign)
4. Publication d'un message RabbitMQ
5. `notification-service` consomme et sauvegarde dans `notification_db.notification_logs`

## 2. Architecture technique

- `event-service` appelle `member-service` via Feign
- `booking-service` appelle `member-service` et `event-service` via Feign
- `booking-service` publie sur `algotech_exchange` avec `booking.routing.key`
- `notification-service` consomme la queue `notification_queue`
- Les services se déclarent dans Eureka et sont routés via `api-gateway`

## 3. Profils et configuration

Chaque service métier/gateway a un `application.yml` avec profil actif par défaut : `dev`.

- Profil `dev` : dépendances externes en `localhost`
- Profil `docker` : dépendances externes via noms de services Docker (`mysql-db`, `rabbitmq`, `discovery-service`)

## 4. Prérequis

### Pour exécution Docker
- Docker
- Docker Compose

### Pour exécution locale (hors Docker)
- Java 21
- Maven (ou `./mvnw`)
- Docker (uniquement pour MySQL + RabbitMQ)

## 5. Initialisation des données

Le script [backend/database/init.sql](backend/database/init.sql) crée automatiquement :
- `member_db`
- `event_db`
- `booking_db`
- `notification_db`

## 6. Lancement complet avec Docker (recommandé)

Depuis la racine du projet :

```bash
docker compose down -v --remove-orphans
docker compose up -d --build
```

Vérifier :

```bash
docker compose ps
docker compose logs -f discovery-service api-gateway member-service event-service booking-service notification-service
```

Accès utiles :
- Eureka : `http://localhost:8761`
- Gateway (point d'entrée API) : `http://localhost:8888`
- RabbitMQ Management : `http://localhost:15672` (user: `user`, pass: `password`)
- phpMyAdmin : `http://localhost:8088`

## 7. Lancement local (dev) pas à pas

### 7.1 Démarrer l'infra (MySQL + RabbitMQ)

```bash
docker compose up -d mysql-db rabbitmq phpmyadmin
```

### 7.2 Démarrer les services (ordre conseillé)

Ouvre un terminal par service :

```bash
cd backend/discovery-service && ./mvnw spring-boot:run
cd backend/api-gateway && ./mvnw spring-boot:run
cd backend/member-service && ./mvnw spring-boot:run
cd backend/event-service && ./mvnw spring-boot:run
cd backend/booking-service && ./mvnw spring-boot:run
cd backend/notification-service && ./mvnw spring-boot:run
```

Point d'entrée API local : `http://localhost:8080`

## 8. Ports et paramètres importants

### Ports
- Gateway : `8080` (host Docker: `8888`)
- Discovery : `8761`
- Member : `8081`
- Event : `8082`
- Booking : `8083`
- Notification : `8084`
- MySQL host : `3308`
- RabbitMQ : `5672` / management `15672`

### Credentials par défaut
- MySQL: user `root`, pass `password`
- RabbitMQ: user `user`, pass `password` (ne pas utiliser `guest`)

### URL JDBC (déjà corrigées)
Les URLs incluent `allowPublicKeyRetrieval=true&useSSL=false` pour éviter l'erreur MySQL "Public Key Retrieval is not allowed".

## 9. Entités de base par service

### member-service
- `Member`
  - `id` (Long)
  - `firstName` (String, obligatoire)
  - `lastName` (String, obligatoire)
  - `email` (String, obligatoire, unique)
  - `role` (Enum: `STUDENT`, `TRAINER`, `ADMIN`)
  - `skills` (String)

### event-service
- `ClubEvent`
  - `id` (Long)
  - `title` (String, obligatoire)
  - `description` (String)
  - `eventDate` (LocalDateTime, future, obligatoire)
  - `location` (String)
  - `trainerId` (Long, obligatoire)
  - `maxCapacity` (Integer, min 1)

### booking-service
- `Booking`
  - `id` (Long)
  - `memberId` (Long, obligatoire)
  - `eventId` (Long, obligatoire)
  - `bookingDate` (LocalDateTime)
  - `status` (Enum: `PENDING`, `CONFIRMED`, `CANCELLED`)

Règles:
- Vérifie existence member/event via Feign
- Vérifie la capacité événement
- Crée réservation avec `status=CONFIRMED`
- Publie une notification RabbitMQ

### notification-service
- `NotificationLog`
  - `id` (Long)
  - `recipientEmail` (String)
  - `subject` (String)
  - `message` (TEXT)
  - `sentAt` (LocalDateTime)

Note: ce service n'expose pas de contrôleur REST actuellement. Il consomme RabbitMQ et écrit en base.

## 10. Endpoints REST disponibles

Tous testables via Gateway:

### Member
- `POST /api/members`
- `GET /api/members`
- `GET /api/members/{id}`

### Event
- `POST /api/events`
- `GET /api/events`
- `GET /api/events/{id}`

### Booking
- `POST /api/bookings`
- `GET /api/bookings/member/{memberId}`

### Notification
- Pas d'endpoint REST exposé actuellement (`queue consumer` uniquement)

## 11. Scénario de test recommandé (ordre)

1. Créer un membre trainer
2. Créer un membre student
3. Créer un event avec `trainerId` du trainer
4. Créer un booking avec `memberId` du student et `eventId`
5. Vérifier en base `notification_db.notification_logs` qu'une notification est persistée

## 12. Collection Postman

Collection fournie :
- [postman/AlgoTech-Hub.postman_collection.json](postman/AlgoTech-Hub.postman_collection.json)

Importe la collection dans Postman puis ajuste seulement la variable:
- `baseUrl`

Valeurs:
- Local dev : `http://localhost:8080`
- Docker : `http://localhost:8888`

La collection capture automatiquement `trainerId`, `memberId`, `eventId`, `bookingId` pour enchaîner les appels.

## 13. Dépannage rapide

### Erreur MySQL: `Public Key Retrieval is not allowed`
- Vérifier que l'URL JDBC contient `allowPublicKeyRetrieval=true&useSSL=false`

### Erreur RabbitMQ: `PLAIN login refused: user 'guest'`
- Utiliser `user/password`, pas `guest`

### Erreur RabbitMQ: `NOT_FOUND - no queue 'notification_queue'`
- Vérifier que `booking-service` et `notification-service` déclarent la même queue/exchange/routing key

### Erreur Eureka: `UnknownHostException discovery-service`
- Vérifier que `discovery-service` est démarré et `Up`
- Vérifier profil (`dev` vs `docker`) et URL Eureka correspondante

## 14. Arrêt et nettoyage

```bash
docker compose down
docker compose down -v
```
