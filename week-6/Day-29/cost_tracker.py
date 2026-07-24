import json
import os


class CostTracker:

    def __init__(self):
        self.file = "usage.json"

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump(
                    {
                        "tokens": 0,
                        "cost": 0
                    },
                    f
                )

    def load(self):
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def update(self, prompt_tokens, completion_tokens):

        total = prompt_tokens + completion_tokens

        price_per_1k = 0.001

        cost = (total / 1000) * price_per_1k

        data = self.load()

        data["tokens"] += total
        data["cost"] += cost

        self.save(data)

    def report(self):

        data = self.load()

        print("\n===== Usage Report =====")
        print(f"Total Tokens : {data['tokens']}")
        print(f"Estimated Cost : ${data['cost']:.6f}")