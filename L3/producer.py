import pika
import time

connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
channel = connection.channel()

# Создаем exchange для событий
channel.exchange_declare(exchange="testing", exchange_type="direct")

# Имитация работы сервиса
for i in range(3):
    event_type = "payment" if i % 2 == 0 else "notification"
    message = f"Событие {i}: {event_type} в {time.strftime('%H:%M:%S')}"

    # Отправка с разными routing_key
    channel.basic_publish(
        exchange="testing",
        routing_key=event_type,
        body=message
    )
    print(f" [Consumer] Отправлено: {message}")
    time.sleep(2)

connection.close()