# src/preprocess.py

from pathlib import Path
from typing import Optional

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Features and target for student mark prediction
FEATURE_COLS = [
    "studytime",
    "failures",
    "absences",
    "Medu",
    "Fedu",
    "G1",
    "G2",
]

TARGET_COL = "G3"  # final mark to predict


def get_project_root() -> Path:
    """
    Returns the project root folder (student-mark-predictions/).
    Assumes this file is under src/.
    """
    return Path(__file__).resolve().parents[1]


def load_data(csv_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Loads the student dataset from data/student_marks.csv by default.
    """
    if csv_path is None:
        csv_path = get_project_root() /"data/student_dataset_10k.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    # Sanity check: required columns
    required_cols = FEATURE_COLS + [TARGET_COL]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    return df


def create_preprocessor() -> ColumnTransformer:
    """
    Preprocessing pipeline for numeric features:
    - Impute missing numeric values using median
    - Scale features with StandardScaler
    """
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, FEATURE_COLS),
        ]
    )

    return preprocessor
