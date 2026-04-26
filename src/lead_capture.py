from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


def save_lead(leads_path: Path, name: str, email: str, message: str) -> None:
    leads_path.parent.mkdir(parents=True, exist_ok=True)

    new_row = pd.DataFrame(
        [
            {
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "name": name,
                "email": email,
                "message": message,
            }
        ]
    )

    if leads_path.exists():
        existing = pd.read_csv(leads_path)
        combined = pd.concat([existing, new_row], ignore_index=True)
    else:
        combined = new_row

    combined.to_csv(leads_path, index=False)
