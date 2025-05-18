import os

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from simple_chat_agent import SimpleChatAgent

class SimpleChat:
    def __init__(self):
        self.modelId = "simple-chat"

    async def run(self):
        agent = SimpleChatAgent()

        kafkaServer = os.getenv("KAFKA_BOOTSTRAP","localhost:9092")
        print(f"kafka server:{kafkaServer}")

        self.consumer = AIOKafkaConsumer(
            self.modelId+"-input",
            bootstrap_servers=kafkaServer,
            group_id="simple-chart-model",
            enable_auto_commit=True,
            # auto_commit_interval_ms=1000*600,
            session_timeout_ms=1000*600,
            auto_offset_reset="earliest"
        )

        self.producer = AIOKafkaProducer(
            bootstrap_servers=kafkaServer
        )

        print("start consumer...")
        await self.consumer.start()
        print("start producer...")
        await self.producer.start()
        try:
            async for msg in self.consumer:
                print("received message...")
                print("{}:{:d}:{:d} key={} value={}"
                      .format(msg.topic,msg.partition,msg.offset,msg.key,msg.value))
                async for msg_chunk, metadata in agent.astream(msg.key,msg.value):
                    # print(msg_chunk)
                    await self.producer.send(
                        topic=self.modelId+"-output",
                        key=msg.key,
                        value=msg_chunk.content.encode("utf-8"))
                # await self.consumer.commit()

        finally:
            await self.producer.stop()
            print("producer stopped")
            await self.consumer.stop()
            print("consumer stopped")
    
