import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ==========================================
# CONFIGURATION (SCALED)
# ==========================================

TOTAL_CALLERS = random.randint(10000, 40000)
FRAUD_RATIO = random.uniform(0.015, 0.035)
DAYS_OF_SIMULATION = random.randint(1, 30)

REGIONS = ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore", "Hyderabad"]
REGIONS = random.sample(REGIONS, random.randint(3, 6))

# ==========================================
# FRAUD CHARACTERISTICS (VARIABLE PER DATASET)
# ==========================================

fraud_volume_multiplier = random.uniform(0.8, 1.3)
fraud_night_bias = random.uniform(0.2, 0.6)

# ==========================================
# CREATE CALLER POPULATION
# ==========================================

num_fraud = int(TOTAL_CALLERS * FRAUD_RATIO)
num_normal = TOTAL_CALLERS - num_fraud

normal_callers = [random.randint(9000000000, 9999999999) for _ in range(num_normal)]
fraud_callers = [random.randint(9000000000, 9999999999) for _ in range(num_fraud)]

print(f"Normal callers: {len(normal_callers)}")
print(f"Fraud callers: {len(fraud_callers)}")

# ==========================================
# GENERATE CALL DATA
# ==========================================

call_records = []
start_date = datetime.now()

# -------- NORMAL USERS --------
for caller in normal_callers:

    for day in range(DAYS_OF_SIMULATION):

        calls_today = random.randint(1, 5)
        if random.random() < 0.08:
            calls_today = random.randint(6, 20)
        for _ in range(calls_today):

            hour = random.randint(8, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            timestamp = start_date - timedelta(days=day)
            timestamp = timestamp.replace(hour=hour, minute=minute, second=second)

            duration = max(30, np.random.normal(160, 60))


            origin = random.choice(REGIONS)
            target = origin if random.random() < 0.8 else random.choice(REGIONS)

            receiver = random.randint(8000000000, 8999999999)

            call_records.append([
                caller,
                receiver,
                round(duration, 2),
                timestamp,
                origin,
                target,
                0
            ])

# -------- FRAUD USERS --------
for caller in fraud_callers:

    for day in range(DAYS_OF_SIMULATION):

        # Use fraud_volume_multiplier to vary call volume
        base_calls = random.randint(6, 35)
        calls_today = max(1, int(base_calls * fraud_volume_multiplier))


        for _ in range(calls_today):

            # Use fraud_night_bias to vary night call probability
            if random.random() < fraud_night_bias:
                hour = random.choice([22, 23, 0, 1, 2, 3, 4, 5])
            else:
                hour = random.randint(9, 21)

            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            timestamp = start_date - timedelta(days=day)
            timestamp = timestamp.replace(hour=hour, minute=minute, second=second)

            duration = max(20, np.random.normal(120, 60))


            origin = random.choice(REGIONS)
            target = random.choice(REGIONS)

            receiver = random.randint(8000000000, 8999999999)

            call_records.append([
                caller,
                receiver,
                round(duration, 2),
                timestamp,
                origin,
                target,
                1
            ])

# ==========================================
# SAVE DATA
# ==========================================

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

# (Noise injection removed - moved to train_model.py)
# ==========================================

df.to_csv("data/call_data.csv", index=False)

print("\n======================================")
print(" SCALED TELECOM DATA GENERATED ")
print("======================================")
print(f"Total records generated: {len(df)}")
print("======================================\n")
