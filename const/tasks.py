from enum import StrEnum


class Tasks(StrEnum):
    """Enumeration for different Tasks."""

    FEATUREENGINEERING = "feature-engineering"
    TRAING = "training"
    EVALUATION = "evaluation"
    INFERENCE = "inference"
    EXPORT = "export"
