# Start with a base image containing Java runtime
FROM openjdk:17-jdk-slim

LABEL org.opencontainers.image.authors="nileshsinha1731"

# Add the application's jar to the container
COPY target/accounts-0.0.1-SNAPSHOT.jar accounts-0.0.1-SNAPSHOT.jar

# execute the application
ENTRYPOINT ["java", "-jar", "accounts-0.0.1-SNAPSHOT.jar"]