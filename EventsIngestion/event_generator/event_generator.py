import json
import random
import time
from datetime import datetime as dt
from confluent_kafka import SerializingProducer
from faker import Faker

from models import (
    BaseEvent,
    SearchEvent,
    AddToCartEvent,
    PlaceOrderEvent,
    ChargedEvent,
    LoginEvent,
    AppLaunchedEvent,
)

fake = Faker()

# Limit the variables
SEARCH_QUERIES = [
    "laptop", "smartphone", "headphones", "running shoes", "backpack",
    "coffee maker", "office chair", "gaming console", "wireless mouse", "fitness tracker",
    "bluetooth speaker", "kindle", "sunglasses", "digital camera", "electric toothbrush"
]

PRODUCT_CATALOG = [
    {"product_id": "prod-001", "product_name": "Laptop Pro", "price": 1299.99},
    {"product_id": "prod-002", "product_name": "Smartphone X", "price": 999.99},
    {"product_id": "prod-003", "product_name": "Noise-Canceling Headphones", "price": 199.99},
    {"product_id": "prod-004", "product_name": "Running Shoes", "price": 89.99},
    {"product_id": "prod-005", "product_name": "Travel Backpack", "price": 79.99},
    {"product_id": "prod-006", "product_name": "Espresso Coffee Maker", "price": 249.99},
    {"product_id": "prod-007", "product_name": "Ergonomic Office Chair", "price": 149.99},
    {"product_id": "prod-008", "product_name": "Gaming Console", "price": 399.99},
    {"product_id": "prod-009", "product_name": "Wireless Mouse", "price": 29.99},
    {"product_id": "prod-010", "product_name": "Fitness Tracker", "price": 129.99},
    {"product_id": "prod-011", "product_name": "Bluetooth Speaker", "price": 59.99},
    {"product_id": "prod-012", "product_name": "E-Reader", "price": 89.99},
    {"product_id": "prod-013", "product_name": "Polarized Sunglasses", "price": 49.99},
    {"product_id": "prod-014", "product_name": "Digital SLR Camera", "price": 549.99},
    {"product_id": "prod-015", "product_name": "Electric Toothbrush", "price": 39.99}
]

PAYMENT_METHODS = ["credit_card", "paypal", "apple_pay", "google_pay"]

LOGIN_METHODS = ["email", "facebook", "google", "twitter"]

APP_VERSIONS = ["1.0.0", "1.1.0", "1.2.5", "2.0.0"]

# Fixed number of users & devices
NUM_USERS = 50
NUM_DEVICES = 75

user_ids = [fake.uuid4() for _ in range(NUM_USERS)]
device_ids = [fake.uuid4() for _ in range(NUM_DEVICES)]

# Map each user to 1-2 devices
user_device_map = {}
for user_id in user_ids:
    associated_devices = random.sample(device_ids, random.randint(1, 2))
    user_device_map[user_id] = associated_devices


def generate_events():
    # Select a user and one of their devices
    user_id = random.choice(user_ids)
    device_id = random.choice(user_device_map[user_id])

    # Default properties
    event_data = {
        "event_id": random.choice(['app_launched', 'login', 'search', 'add_to_cart', 'place_order', 'charged']),
        "event_category": random.choice(['category_A', 'category_B']),
        "timestamp": time.time_ns(),
        "user_id": user_id,
        "insert_id": fake.uuid4(),
        "source_id": random.choice(["web", "mobile_app", "email_campaign", "social_media"]),
        "device_id": device_id,
        "event_date": dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    }

    event_id = event_data["event_id"]

    try:
        if event_id == "search":
            event_data["search_query"] = random.choice(SEARCH_QUERIES)
            event = SearchEvent(**event_data)
        elif event_id == "add_to_cart":
            product = random.choice(PRODUCT_CATALOG)
            event_data.update({
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "quantity": random.randint(1, 5),
                "price": product["price"]
            })
            event = AddToCartEvent(**event_data)
        elif event_id == "place_order":
            event_data["order_id"] = fake.uuid4()
            items = []
            total = 0.0
            for _ in range(random.randint(1, 5)):
                product = random.choice(PRODUCT_CATALOG)
                quantity = random.randint(1, 3)
                price = product["price"]
                item_total = price * quantity
                total += item_total
                items.append({
                    "product_id": product["product_id"],
                    "product_name": product["product_name"],
                    "quantity": quantity,
                    "price": price
                })
            event_data["order_total"] = round(total, 2)
            event_data["items"] = items
            event = PlaceOrderEvent(**event_data)
        elif event_id == "charged":
            event_data.update({
                "payment_method": random.choice(PAYMENT_METHODS),
                "amount": round(random.uniform(20.0, 500.0), 2)
            })
            event = ChargedEvent(**event_data)
        elif event_id == "login":
            event_data["login_method"] = random.choice(LOGIN_METHODS)
            event = LoginEvent(**event_data)
        elif event_id == "app_launched":
            event_data["app_version"] = random.choice(APP_VERSIONS)
            event = AppLaunchedEvent(**event_data)
        else:
            # For any other event types, use BaseEvent
            event = BaseEvent(**event_data)

        return event.dict()
    except Exception as e:
        print(f"Error generating event: {e}")
        return None


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def main():
    topic = 'events'
    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9092'
    })
    curr_time = dt.now()

    while (dt.now() - curr_time).seconds < 500:
        try:
            event = generate_events()
            if event:
                print(event)
                producer.produce(
                    topic=topic,
                    key=event['insert_id'],
                    value=json.dumps(event),
                    on_delivery=delivery_report
                )
                producer.poll(0)
            time.sleep(5)
        except BufferError:
            print("Buffer full! Waiting...")
            time.sleep(1)
        except Exception as e:
            print(f"Exception in main loop: {e}")

    # Flush any remaining messages
    producer.flush()


if __name__ == "__main__":
    main()
