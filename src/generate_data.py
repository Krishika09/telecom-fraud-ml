import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Number of fake call records
NUM_RECORDS = 5000

data = []

for _ in range(NUM_RECORDS):
    caller_id = random.randint(9000000000, 9999999999)
    receiver_id = random.randint(8000000000, 8999999999)

    call_duration = np.random.exponential(scale=60)  # average 60 sec
    call_duration = round(call_duration, 2)

    timestamp = datetime.now() - timedelta(
        minutes=random.randint(0, 60 * 24 * 30)
    )

    origin_region = random.choice(["Delhi", "Mumbai", "Kolkata", "Chennai"])
    target_region = random.choice(["Delhi", "Mumbai", "Kolkata", "Chennai"])

    data.append([
        caller_id,
        receiver_id,
        call_duration,
        timestamp,
        origin_region,
        target_region
    ])

df = pd.DataFrame(data, columns=[
    "caller_id",
    "receiver_id",
    "call_duration",
    "timestamp",
    "origin_region",
    "target_region"
])

df.to_csv("data/call_data.csv", index=False)

print("Fake telecom data generated successfully!")
