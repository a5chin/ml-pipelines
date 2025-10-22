from pydantic_settings import BaseSettings

from const import Environment, ModelType, Task
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

    env: Environment = Environment.DEV
    model_type: ModelType = ModelType.SAMPLE
    task: Task = Task.FEATURE_ENGINEERING


task_maps: dict[ModelType, dict[Task, type[BaseTask]]] = {
    ModelType.SAMPLE: {
        Task.FEATURE_ENGINEERING: FeatureEngineeringTask,
        Task.TRAINING: TrainingTask,
        Task.EVALUATION: EvaluationTask,
        Task.INFERENCE: InferenceTask,
        Task.EXPORT: ExportTask,
    }
}


def main() -> None:
    """Run Tasks main function."""
    args = CLIArgs()

    task = task_maps[args.model_type][args.task]()
    task.run()


if __name__ == "__main__":  # pragma: no cover
    main()
