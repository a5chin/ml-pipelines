from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import nox
from pydantic_settings import BaseSettings

from composer import ComposerSettings
from const import Environment, ModelType
from environments.settings import load_env_settings


class CLIArgs(BaseSettings):
    """CLIArgs is a class that extends BaseSettings to handle command line arguments."""

    cov_report: str = ""
    junitxml: str = ""
    ruff: bool = False
    sqruff: bool = False
    ty: bool = False

    env: Environment = Environment.DEV
    tag: str = "test"
    model_type: ModelType = ModelType.SAMPLE

    @property
    def composer_project_id(self) -> str:
        """Get the GCP project ID for Composer based on the environment.

        Returns:
            str: The GCP project ID corresponding to the current environment.

        """
        return {
            Environment.DEV: "dev",
            Environment.PROD: "prod",
        }[self.env]

    @property
    def composer_bucket_name(self) -> str:
        """Get the GCS bucket name for Composer based on the environment.

        Returns:
            str: The GCS bucket name corresponding to the current environment.

        """
        return {
            Environment.DEV: "dev-bucket",
            Environment.PROD: "prod-bucket",
        }[self.env]

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

    def dump_for_composer(self) -> ComposerSettings:
        """Dump Airflow setting file as JSON.

        Args:
            env (Environment): The target Environment.
            model_type (ModelType): The target model type.

        Returns:
            ComposerSettings: The settings for Composer.

        """
        env_settings = load_env_settings(self.env)

        return ComposerSettings(
            project_id=env_settings.project_id,
            location=env_settings.location,
            environment=self.env,
            tag=self.tag,
            model_type=self.model_type,
        )


@nox.session(python=False)
def fmt(session: nox.Session) -> None:
    """Format the code using Ruff and sqruff.

    Args:
        session (nox.Session): The Nox session object.

    Examples:
        >>> uv run nox -s fmt -- \
        ...     --ruff \
        ...     --sqruff

    """
    args = CLIArgs.parse(session.posargs)

    if args.ruff:
        session.run("uv", "run", "ruff", "format", ".")
        session.log("✅ Ruff formatting completed successfully.")
    if args.sqruff:
        session.run("uv", "run", "sqruff", "fix")
        session.log("✅ sqruff formatting completed successfully.")


@nox.session(python=False)
def lint(session: nox.Session) -> None:
    """Lint the code using Ruff, sqruff, and ty.

    Args:
        session (nox.Session): The Nox session object.

    Examples:
        >>> uv run nox -s lint -- \
        ...     --ruff \
        ...     --sqruff \
        ...     --ty

    """
    args = CLIArgs.parse(session.posargs)

    if args.ruff:
        session.run("uv", "run", "ruff", "check", ".", "--fix")
        session.log("✅ Ruff linting completed successfully.")
    if args.sqruff:
        session.run("uv", "run", "sqruff", "lint", ".")
        session.log("✅ sqruff linting completed successfully.")
    if args.ty:
        session.run("uv", "run", "ty", "check")
        session.log("✅ ty linting completed successfully.")


@nox.session(python=False)
def test(session: nox.Session) -> None:
    """Run tests using pytest.

    Args:
        session (nox.Session): The Nox session object.

    Examples:
        >>> uv run nox -s test -- \
        ...     --cov_report xml \
        ...     --junitxml junit.xml

    """
    args = CLIArgs.parse(session.posargs)

    command = ["uv", "run", "pytest", "--cov", "--cov-branch"]
    if args.cov_report:
        command.append(f"--cov-report={args.cov_report}")
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
        ...     --env dev \
        ...     --tag test \
        ...     --model_type sample

    """
    args = CLIArgs.parse(session.posargs)

    command = [
        "uv",
        "run",
        "-m",
        "pipelines.main",
        "--env",
        args.env,
        "--tag",
        args.tag,
        "--model_type",
        args.model_type,
    ]

    session.run(*command)

    session.log(
        f"✅ Compile {args.env}-{args.model_type}-pipeline completed successfully."
    )


@nox.session(python=False)
def deploy_dags(session: nox.Session) -> None:
    """Deploy Airflow DAGs to Composer.

    Example:
        >>> uv run nox -s deploy_dags -- \
        ...     --env dev \
        ...     --tag latest \
        ...     --model_type sample

    """
    args = CLIArgs.parse(session.posargs)
    settings = args.dump_for_composer()
    settings_file = Path(f"composer/dags/{settings.model_type}.json")

    with settings_file.open("w", encoding="utf-8") as f:
        json.dump(settings.model_dump(), f)

    command = [
        "gcloud",
        "storage",
        "cp",
        "-r",
        "composer/dags/*",
        f"gs://{args.composer_bucket_name}/dags",
        "--project",
        args.composer_project_id,
    ]

    session.run(*command, external=True)

    settings_file.unlink()

    session.log("✅ Airflow DAGs deployed successfully")
