```bash
docker exec \
    --workdir /opt/kafka/bin -it \
    demo-kafka-1 \
    ./kafka-topics.sh \
    --bootstrap-server localhost:9092 \
    --create --topic simple-chat-input

docker exec \
    --workdir /opt/kafka/bin -it \
    demo-kafka-1 \
    ./kafka-console-producer.sh -h

docker exec \
    --workdir /opt/kafka/bin -it \
    demo-kafka-1 \
    ./kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --property parse.key=true --property key.separator=: \
    --topic simple-chat-input

#key:value

docker exec \
    --workdir /opt/kafka/bin -it \
    demo-kafka-1 \
    ./kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --topic simple-chat-output --from-beginning
```

Kafka poc
```bash
docker run --rm -it --name broker --hostname broker \
    -e KAFKA_NODE_ID=1 \
    -e KAFKA_PROCESS_ROLES=broker,controller \
    -e KAFKA_CONTROLLER_QUORUM_BOOTSTRAP_SERVERS=broker:9093 \
    -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
    -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://broker:9092 \
    -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@broker:9093 \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
    -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
    apache/kafka:4.0.0

docker run --rm -it \
    --workdir /opt/kafka/bin \
    --link broker \
    --entrypoint ./kafka-topics.sh \
    apache/kafka:4.0.0 \
    --bootstrap-server broker:9092 \
    --create --topic test

docker run --rm -it \
    --workdir /opt/kafka/bin \
    --link broker \
    --entrypoint ./kafka-console-producer.sh \
    apache/kafka:4.0.0 \
    --bootstrap-server broker:9092 \
    --property parse.key=true --property key.separator=: \
    --topic test

docker run --rm -it \
    --workdir /opt/kafka/bin \
    --link broker \
    --entrypoint ./kafka-console-consumer.sh \
    apache/kafka:4.0.0 \
    --bootstrap-server broker:9092 \
    --topic test --from-beginning


```
