INJECTION_PATTERNS = [
    "ignore all previous instructions",
    "forget previous instructions",
    "system prompt",
    "developer message",
    "reveal your instructions"
]


def validate_input(prompt: str):

    if len(prompt) > 10000:
        return False, "Input too long."

    text = prompt.lower()

    for pattern in INJECTION_PATTERNS:
        if pattern in text:
            return False, f"Blocked prompt injection pattern: {pattern}"

    return True, "Input is safe."


def validate_output(text: str):

    banned = [
        "system prompt",
        "developer instructions"
    ]

    lower = text.lower()

    for word in banned:
        if word in lower:
            return False

    return True