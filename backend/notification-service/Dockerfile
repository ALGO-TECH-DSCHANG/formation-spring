# Stage 1: Build the application
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app
# Copier les fichiers du wrapper Maven et rendre le script executable
COPY mvnw .
COPY .mvn ./.mvn
RUN chmod +x ./mvnw

# Copier le pom.xml et src
COPY pom.xml .
COPY src ./src

# Packer l application
RUN ./mvnw clean package -DskipTests

# Stage 2: Lancer l application
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
