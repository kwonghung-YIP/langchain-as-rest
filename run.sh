#!/bin/bash

docker compose -p demo down

docker compose -p demo up -d --build

KAFKA_CTR=demo-kafka-1

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

docker exec \
    --workdir /opt/kafka/bin -it \
    $KAFKA_CTR \
    ./kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --property parse.key=true --property key.separator=: \
    --topic simple-chat-input


