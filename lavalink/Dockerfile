FROM eclipse-temurin:17-jdk-jammy

WORKDIR /opt/lavalink

RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

# 실행
CMD ["java", "-jar", "Lavalink.jar"]
