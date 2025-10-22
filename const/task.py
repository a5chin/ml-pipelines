from enum import StrEnum


class Task(StrEnum):
    """Enumeration for different Tasks."""

    FEATURE_ENGINEERING = "feature_engineering"
    TRAINING = "training"
    EVALUATION = "evaluation"
    INFERENCE = "inference"
    EXPORT = "export"
