from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

notifications = []


def send_notification(name: str):

    time.sleep(5)

    notifications.append(
        f"Notification sent to {name}"
    )

    print(f"Notification sent to {name}")


@app.get("/")
def home():

    return {
        "message": "Day 19 - Background Tasks"
    }


@app.post("/register/{name}")
def register(
    name: str,
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        send_notification,
        name
    )

    return {
        "message": f"{name} registered successfully."
    }


@app.get("/notifications")
def get_notifications():

    return {
        "notifications": notifications
    }