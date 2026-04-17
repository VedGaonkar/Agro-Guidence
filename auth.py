"""
auth.py — Simple Name Entry for Agro Guidance
No sign-in or sign-up required. User just enters their name to start.
"""


def start_session(name: str) -> dict:
    """
    Start a session with just a display name.
    Returns {"success": True, "user": {...}} or {"success": False, "message": "..."}
    """
    name = name.strip()
    if not name:
        return {"success": False, "message": "Please enter your name to continue."}

    return {
        "success": True,
        "user": {
            "name": name,
        },
    }
