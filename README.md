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