import pika

def callback(ch, method, properties, body):
    print(f"\n [Service B] Получено событие типа '{method.routing_key}': {body.decode()}")

# Подключение
connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
channel = connection.channel()

# Привязка к разным типам событий
channel.exchange_declare(exchange="testing", exchange_type="direct")
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

# Подписка на два типа событий
for event_type in ["payment", "notification"]:
    channel.queue_bind(
        exchange="testing",
        queue=queue_name,
        routing_key=event_type
    )

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print(" [*] Ожидание событий от Consumer")
channel.start_consuming()
