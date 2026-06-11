from pydantic import BaseModel

from const import ModelType  # noqa: TC001


class ComposerSettings(BaseModel):
    """The settings for Composer."""

    project_id: str
    location: str
    environment: str
    tag: str
    model_type: ModelType
