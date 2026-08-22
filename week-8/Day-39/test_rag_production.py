import time

import requests


BASE_URL = "http://127.0.0.1:8000"


documents = [
    """
    Employees are allowed 12 casual leaves every year.
    Casual leave should be requested through the HR system.
    """,
    """
    Employees can work remotely with prior approval from
    their reporting manager.
    """,
    """
    The company provides medical insurance to all
    full-time employees.
    """
]


response = requests.post(
    f"{BASE_URL}/ingest",
    json={
        "documents": documents
    }
)

print("Ingestion Response:")
print(response.json())


job_id = response.json()["job_id"]

time.sleep(1)


response = requests.get(
    f"{BASE_URL}/ingest/{job_id}"
)

print("\nIngestion Status:")
print(response.json())


query = requests.post(
    f"{BASE_URL}/query",
    json={
        "query": "How many casual leaves are allowed?"
    }
)

print("\nFirst Query:")
print(query.json())


query = requests.post(
    f"{BASE_URL}/query",
    json={
        "query": "How many casual leaves are allowed?"
    }
)

print("\nSecond Query:")
print(query.json())


stats = requests.get(
    f"{BASE_URL}/stats"
)

print("\nStatistics:")
print(stats.json())