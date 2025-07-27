import json
from datetime import datetime
from pathlib import Path
from typing import Tuple

CRED_FILE = Path(__file__).parent.parent / "database/user-creds.json"

def validate_credentials(id: str, api_key: str) -> Tuple[bool, str]:
    try:
        with open(CRED_FILE, "r") as f:
            users = json.load(f)

        for user in users:
            if user.get("id") == id and user.get("api-key") == api_key:
                expiry_str = user.get("date")
                if not expiry_str:
                    return False, "Missing expiration date for this user"

                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
                today = datetime.today().date()

                if today > expiry_date:
                    return False, f"Access expired on {expiry_date}"
                return True, "Credentials are valid"

        return False, "Invalid ID or API key"
    
    except Exception as e:
        return False, f"Server error: {e}"
