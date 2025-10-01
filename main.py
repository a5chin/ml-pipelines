from pydantic_settings import BaseSettings

from const import Environments, ModelTypes, Tasks
from tasks import (
    BaseTask,
    EvaluationTask,
    ExportTask,
    FeatureEngineeringTask,
    InferenceTask,
    TrainingTask,
)


class CLIArgs(BaseSettings, cli_parse_args=True):
    """CLI Arguments."""

    env: Environments = Environments.DEV
    model_type: ModelTypes = ModelTypes.SAMPLE
    task: Tasks = Tasks.FEATUREENGINEERING


task_maps: dict[ModelTypes, dict[Tasks, type[BaseTask]]] = {
    ModelTypes.SAMPLE: {
        Tasks.FEATUREENGINEERING: FeatureEngineeringTask,
        Tasks.TRAING: TrainingTask,
        Tasks.EVALUATION: EvaluationTask,
        Tasks.INFERENCE: InferenceTask,
        Tasks.EXPORT: ExportTask,
    }
}


def main() -> None:
    """Run Tasks main function."""
    args = CLIArgs()

    task = task_maps[args.model_type][args.task]()
    task.run()


if __name__ == "__main__":  # pragma: no cover
    main()
