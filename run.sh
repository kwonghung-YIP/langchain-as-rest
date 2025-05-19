#!/bin/bash

docker compose down

docker compose up -d --no-start --build
docker compose start kafka

KAFKA_CTR=kafka

docker exec \
    --workdir /opt/kafka/bin -it \
    $KAFKA_CTR \
    ./kafka-topics.sh \
    --bootstrap-server localhost:9092 \
    --create --topic simple-chat-input

docker exec \
    --workdir /opt/kafka/bin -it \
    $KAFKA_CTR \
    ./kafka-topics.sh \
    --bootstrap-server localhost:9092 \
    --create --topic simple-chat-output

docker compose start langchain

docker compose logs langchain

docker exec \
    --workdir /opt/kafka/bin -it \
    $KAFKA_CTR \
    ./kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --property parse.key=true --property key.separator=: \
    --topic simple-chat-input


