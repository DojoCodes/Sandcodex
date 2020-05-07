from sandcodex.backend.config import interpreters


def list_interpreters():
    return {
        "interpreters": list(interpreters.keys())
    }, 200