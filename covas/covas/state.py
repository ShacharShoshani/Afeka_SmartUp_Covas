from pathlib import Path
import json
from covas.constants import STATE_FILE


def save_active_profile(profile_name):
    data = {
        "active_profile": profile_name
    }

    with open(STATE_FILE, "w") as file:
        json.dump(data, file)


def load_active_profile():
    if not STATE_FILE.exists():
        return None

    try:
        with open(STATE_FILE, "r") as file:
            data = json.load(file)
        return data.get("active_profile")
    except (json.JSONDecodeError, IOError):
        return None