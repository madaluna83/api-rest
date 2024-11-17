import csv
import random
from datetime import datetime, timedelta

data_file = "senzori.txt"

def generate_random_data(num: int = 128):
    current_time = datetime.now()

    with open(data_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        for _ in range(num):
            sensor_type = random.choice(["temp", "umid"])

            if sensor_type == "temp":
                value = round(random.uniform(15, 30), 2)
            else:
                value = round(random.uniform(40, 80), 2)

            timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

            writer.writerow([timestamp, sensor_type, value])

            current_time -= timedelta(minutes=1)

generate_random_data()