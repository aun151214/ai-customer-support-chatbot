from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"question", "answer"}


def load_faq_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"FAQ file not found: {path}")

    return pd.read_csv(path)


def validate_faq_data(df: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"FAQ CSV is missing required column(s): {missing}")

    if df.empty:
        raise ValueError("FAQ CSV is empty.")

    if df["question"].isna().any() or df["answer"].isna().any():
        raise ValueError("FAQ CSV contains empty question or answer values.")
