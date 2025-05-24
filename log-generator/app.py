import json
import random
import sys
import time
import uuid
from datetime import datetime

LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
MESSAGES = [
    "User logged in",
    "Payment successful",
    "Disk space low",
    "Order processed",
    "File uploaded",
    "Connection timeout"
]
SERVICES = ["order-processor", "user-service", "payment-gateway", "notification-service"]


def generate_structured_log(event_id):
    log = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": random.choice(LEVELS),
        "message": random.choice(MESSAGES),
        "service": random.choice(SERVICES),
        "request_id": str(uuid.uuid4()),
        "event_id": event_id
    }
    print(json.dumps(log), flush=True)


def generate_unstructured_log(event_id):
    timestamp = datetime.utcnow().isoformat() + "Z"
    level = random.choice(LEVELS)
    log = f"{timestamp} [{level}] Unstructured log: Something happened here! Event: {event_id}"
    print(log, flush=True)


def main():
    event_id = 1
    while True:
        if random.random() < 0.7:
            generate_structured_log(event_id)
        else:
            generate_unstructured_log(event_id)
        event_id += 1
        time.sleep(random.uniform(0.5, 2))


if __name__ == "__main__":
    main() 