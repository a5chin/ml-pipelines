from typing import Any

import nox
from pydantic_settings import BaseSettings

from const import Environment, ModelType


class CLIArgs(BaseSettings, cli_parse_args=True, cli_ignore_unknown_args=True):
    """CLIArgs is a class that extends BaseSettings to handle command line arguments."""

    junitxml: str = ""
    pyright: bool = False
    ruff: bool = False

    env: Environment = Environment.DEV
    pipeline_name: str = "sample-pipeline"
    tag: str = "test"
    model_type: ModelType = ModelType.SAMPLE

    @classmethod
    def parse(cls, posargs: list[str]) -> CLIArgs:
        """Parse command line arguments from the provided list.

        Args:
            posargs (list[str]): List of positional arguments from the command line.

        Returns:
            CLIArgs: An instance of `CLIArgs` populated with the parsed arguments.

        """
        arg_name: str | None = None
        kwargs: dict[str, Any] = {}

        for arg in posargs:
            if arg.startswith("--"):
                arg_name = arg[2:]
                kwargs[arg_name] = True
            elif arg_name is not None:
                kwargs[arg_name] = arg
                arg_name = None

        return cls(**kwargs)


@nox.session(python=False)
def fmt(session: nox.Session) -> None:
    """Format the code using Ruff.

    Args:
        session (nox.Session): The Nox session object.

    Examples:
        >>> uv run nox -s fmt

    """
    session.run("uv", "run", "ruff", "format", ".")

    session.log("✅ Formatting completed successfully.")


@nox.session(python=False)
def lint(session: nox.Session) -> None:
    """Lint the code using Pyright and Ruff.

    Args:
        session (nox.Session): The Nox session object.

    Examples:
        >>> uv run nox -s lint -- --pyright --ruff

    """
    args = CLIArgs.parse(session.posargs)

    if args.pyright:
        session.run("uv", "run", "pyright")
        session.log("✅ Pyright linting completed successfully.")
    if args.ruff:
        session.run("uv", "run", "ruff", "check", ".", "--fix")
        session.log("✅ Ruff linting completed successfully.")


@nox.session(python=False)
def test(session: nox.Session) -> None:
    """Run tests using pytest.

    Args:
        session (nox.Session): The Nox session object.

    Examples:
        >>> uv run nox -s test

    """
    args = CLIArgs.parse(session.posargs)

    command = ["uv", "run", "pytest"]
    if args.junitxml:
        command.append(f"--junitxml={args.junitxml}")

    session.run(*command)

    session.log("✅ Testing completed successfully.")


@nox.session(python=False)
def compile_pipeline(session: nox.Session) -> None:
    """Run Compile Pipeline.

    Args:
        session (nox.Session): The Nox session object.

    Examples:
        >>> uv run -m nox -s compile_pipeline -- \
        >>> --env dev \
        >>> --pipeline_name sample-pipeline \
        >>> --tag test \
        >>> --model_type sample

    """
    args = CLIArgs.parse(session.posargs)

    command = [
        "uv",
        "run",
        "-m",
        "pipelines.main",
        "--env",
        args.env,
        "--pipeline_name",
        args.pipeline_name,
        "--tag",
        args.tag,
        "--model_type",
        args.model_type,
    ]

    session.run(*command)

    session.log(f"✅ Compile {args.env}-{args.pipeline_name} completed successfully.")
