FROM eclipse-temurin:17-jdk-jammy

WORKDIR /lavalink

COPY . .

EXPOSE 2333

CMD ["sh", "-c", "echo ${PROXY_HOST} ${PROXY_NAME} >> /etc/hosts && java -jar Lavalink.jar"]