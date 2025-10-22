from kfp.dsl import ContainerSpec, container_component

from const import Task


@container_component
def feature_engineering(
    image: str,
    execution_date: str,
    model_type: str,
) -> ContainerSpec:
    """Feature Engineering component."""
    return ContainerSpec(
        image=str(image),
        command=["uv", "run", "main.py"],
        args=[
            "--execution_date",
            execution_date,
            "--task",
            Task.FEATURE_ENGINEERING,
            "--model_type",
            model_type,
        ],
    )


@container_component
def training(
    image: str,
    execution_date: str,
    model_type: str,
) -> ContainerSpec:
    """Training component."""
    return ContainerSpec(
        image=image,
        command=["uv", "run", "main.py"],
        args=[
            "--execution_date",
            execution_date,
            "--task",
            Task.TRAINING,
            "--model_type",
            model_type,
        ],
    )


@container_component
def evaluation(
    image: str,
    execution_date: str,
    model_type: str,
) -> ContainerSpec:
    """Evaluate component."""
    return ContainerSpec(
        image=image,
        command=["uv", "run", "main.py"],
        args=[
            "--execution_date",
            execution_date,
            "--task",
            Task.EVALUATION,
            "--model_type",
            model_type,
        ],
    )


@container_component
def inference(
    image: str,
    execution_date: str,
    model_type: str,
) -> ContainerSpec:
    """Inference component."""
    return ContainerSpec(
        image=image,
        command=["uv", "run", "main.py"],
        args=[
            "--execution_date",
            execution_date,
            "--task",
            Task.INFERENCE,
            "--model_type",
            model_type,
        ],
    )


@container_component
def export(
    image: str,
    execution_date: str,
    model_type: str,
) -> ContainerSpec:
    """Export component."""
    return ContainerSpec(
        image=image,
        command=["uv", "run", "main.py"],
        args=[
            "--execution_date",
            execution_date,
            "--task",
            Task.EXPORT,
            "--model_type",
            model_type,
        ],
    )
