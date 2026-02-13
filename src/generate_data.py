import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ===============================
# GLOBAL CONFIGURATION
# ===============================

TOTAL_CALLERS = 800
FRAUD_RATIO = 0.05
DAYS_OF_SIMULATION = 30

REGIONS = ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore", "Hyderabad"]

random.seed(42)
np.random.seed(42)

# ===============================
# CREATE CALLER POPULATION
# ===============================

num_fraud_callers = int(TOTAL_CALLERS * FRAUD_RATIO)
num_normal_callers = TOTAL_CALLERS - num_fraud_callers

normal_callers = [random.randint(9000000000, 9999999999) for _ in range(num_normal_callers)]
fraud_callers = [random.randint(9000000000, 9999999999) for _ in range(num_fraud_callers)]

all_callers = normal_callers + fraud_callers

print(f"Normal callers: {len(normal_callers)}")
print(f"Fraud callers: {len(fraud_callers)}")

# ===============================
# GENERATE CALLS FOR NORMAL USERS
# ===============================

call_records = []

start_date = datetime.now()

for caller in normal_callers:

    calls_per_day = random.randint(1, 10)

    for day in range(DAYS_OF_SIMULATION):

        for _ in range(calls_per_day):

            # Mostly day calls
            if random.random() < 0.05:
                hour = random.randint(22, 23)
            else:
                hour = random.randint(8, 21)

            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            timestamp = start_date - timedelta(days=day)
            timestamp = timestamp.replace(hour=hour, minute=minute, second=second)

            duration = max(20, np.random.normal(180, 40))

            origin_region = random.choice(REGIONS)
            target_region = origin_region if random.random() < 0.7 else random.choice(REGIONS)

            receiver_id = random.randint(8000000000, 8999999999)

            call_records.append([
                caller,
                receiver_id,
                round(duration, 2),
                timestamp,
                origin_region,
                target_region,
                0  # normal label
            ])
# ===============================
# GENERATE CALLS FOR FRAUD USERS
# ===============================

for caller in fraud_callers:

    calls_per_day = random.randint(50, 150)

    for day in range(DAYS_OF_SIMULATION):

        for _ in range(calls_per_day):

            # 50% night calls
            if random.random() < 0.5:
                hour = random.choice([22, 23, 0, 1, 2, 3, 4, 5])
            else:
                hour = random.randint(9, 21)

            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            timestamp = start_date - timedelta(days=day)
            timestamp = timestamp.replace(hour=hour, minute=minute, second=second)

            duration = np.random.exponential(scale=20)

            origin_region = random.choice(REGIONS)
            target_region = random.choice(REGIONS)

            receiver_id = random.randint(8000000000, 8999999999)

            call_records.append([
                caller,
                receiver_id,
                round(duration, 2),
                timestamp,
                origin_region,
                target_region,
                1  # fraud label
            ])
# ===============================
# SAVE DATASET
# ===============================

columns = [
    "caller_id",
    "receiver_id",
    "call_duration",
    "timestamp",
    "origin_region",
    "target_region",
    "true_label"
]

df = pd.DataFrame(call_records, columns=columns)

df.to_csv("data/call_data.csv", index=False)

print("High-quality telecom dataset generated successfully!")
print(f"Total records: {len(df)}")
