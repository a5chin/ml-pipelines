# ML Pipelines Template

<div align="center">

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

[![Versions](https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13%20|%203.14%20-green.svg)](https://www.python.org/downloads/)
![code coverage](https://raw.githubusercontent.com/a5chin/ml-pipelines/coverage-badge/coverage.svg?raw=true)

[![Docker](https://github.com/a5chin/ml-pipelines/actions/workflows/docker.yml/badge.svg)](https://github.com/a5chin/ml-pipelines/actions/workflows/docker.yml)
[![Format](https://github.com/a5chin/ml-pipelines/actions/workflows/format.yml/badge.svg)](https://github.com/a5chin/ml-pipelines/actions/workflows/format.yml)
[![Lint](https://github.com/a5chin/ml-pipelines/actions/workflows/lint.yml/badge.svg)](https://github.com/a5chin/ml-pipelines/actions/workflows/lint.yml)
[![Test](https://github.com/a5chin/ml-pipelines/actions/workflows/test.yml/badge.svg)](https://github.com/a5chin/ml-pipelines/actions/workflows/test.yml)

</div>

---

## 📑 Table of Contents

- [📋 Overview](#-overview)
- [📦 Prerequisites](#-prerequisites)
- [🚀 Getting Started](#-getting-started)
- [📁 Project Structure](#-project-structure)
- [🛠️ Development Commands](#️-development-commands)
- [🏗️ Architecture Overview](#️-architecture-overview)
- [➕ Adding New Pipelines](#-adding-new-pipelines)
- [📚 Related Resources](#-related-resources)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 📋 Overview

This is a production-ready template for building **Kubeflow Pipelines (KFP)** workflows with Python.
It provides a structured, scalable architecture for ML pipelines with containerized task execution, type-safe configuration, and comprehensive testing.

### ✨ Key Features

- 🔄 **Kubeflow Pipelines Integration**: Build, compile, and deploy KFP workflows
- 🧩 **Task-Based Architecture**: Modular ML tasks (feature engineering, training, evaluation, inference, export)
- 🌍 **Environment Management**: Multi-environment support (dev, prod) with isolated configurations
- ⚡ **Modern Python Tooling**: Built with [uv](https://github.com/astral-sh/uv) and [Ruff](https://github.com/astral-sh/ruff)
- 🔒 **Type Safety**: Full type hints with ty and Pydantic validation
- 📝 **SQL Linting**: Automated SQL quality checks with [SQLFluff](https://github.com/sqlfluff/sqlfluff) for BigQuery
- 🚀 **CI/CD Ready**: GitHub Actions workflows for testing, linting, and Docker builds

## 📦 Prerequisites

- 🐍 [Python 3.10+](https://www.python.org/downloads/) - Programming language
- 📦 [uv](https://docs.astral.sh/uv/getting-started/installation/) - Fast Python package installer and resolver
- 🐳 [Docker](https://docs.docker.com/get-docker/) - Container platform (for builds)
- ☸️ [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/v2/installation/) - ML workflow orchestration platform

> 💡 **Quick Install uv**:
> ```bash
> # macOS/Linux
> curl -LsSf https://astral.sh/uv/install.sh | sh
>
> # Windows
> powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
> ```

## 🚀 Getting Started

### 1️⃣ Install Dependencies

```bash
uv sync
```

### 2️⃣ Run Tests

```bash
uv run nox -s test
```

### 3️⃣ Compile a Pipeline

```bash
uv run nox -s compile_pipeline -- \
  --env dev \
  --pipeline_name sample-pipeline \
  --tag test \
  --model_type sample
```

## 📁 Project Structure

```
.
├── const/                          # Shared enumerations
│   ├── environment.py              # Environment enum (dev, prod)
│   ├── model_type.py               # Model type enum (sample, ...)
│   └── task.py                     # Task enum (feature_engineering, training, ...)
├── environments/                   # Environment-specific settings
│   ├── dev.py                      # Development environment config
│   ├── prod.py                     # Production environment config
│   └── settings.py                 # Settings loader
├── pipelines/                      # KFP pipeline definitions
│   ├── components.py               # KFP container components
│   ├── graphs/                     # Pipeline graph definitions
│   │   └── sample.py               # Sample pipeline graph
│   ├── main.py                     # Pipeline compiler & uploader
│   └── settings.py                 # Pipeline compilation settings
├── tasks/                          # ML task implementations
│   ├── base.py                     # BaseTask protocol
│   ├── feature_engineering/        # Feature engineering task
│   ├── training/                   # Model training task
│   ├── evaluation/                 # Model evaluation task
│   ├── inference/                  # Inference task
│   └── export/                     # Export task
├── tests/                          # Test suite (mirrors src structure)
├── main.py                         # Task executor (runs inside KFP containers)
├── noxfile.py                      # Task automation with Nox
├── pyproject.toml                  # Project dependencies & metadata
├── pytest.ini                      # Pytest configuration
├── ruff.toml                       # Ruff linter configuration
└── .sqlfluff                       # SQLFluff SQL linter configuration
```

**Key Files**:
- [`main.py`](./main.py) - Entry point for task execution in containers
- [`noxfile.py`](./noxfile.py) - Development task automation (test, lint, fmt, compile_pipeline)
- [`pyproject.toml`](./pyproject.toml) - Project configuration and dependencies
- [`.sqlfluff`](./.sqlfluff) - SQL linter configuration (BigQuery dialect)
- [`CLAUDE.md`](./CLAUDE.md) - Architecture guide for Claude Code

## 🛠️ Development Commands

### 🧪 Testing
```bash
# Run all tests
uv run nox -s test

# Run specific test file
uv run pytest tests/path/to/test__file.py

# Run with JUnit XML output
uv run nox -s test -- --junitxml=results.xml
```

### ✅ Code Quality
```bash
# Format code (Python)
uv run nox -s fmt -- --ruff

# Format SQL files
uv run nox -s fmt -- --sqlfluff

# Format all
uv run nox -s fmt -- --ruff --sqlfluff

# Run all linters
uv run nox -s lint -- --ruff --sqlfluff --ty

# Run individual linters
uv run nox -s lint -- --ruff     # Python linting
uv run nox -s lint -- --sqlfluff # SQL linting
uv run nox -s lint -- --ty       # Type checking
```

### 🔧 Pipeline Development
```bash
# Compile and upload pipeline
uv run nox -s compile_pipeline -- \
  --env <dev|prod> \
  --pipeline_name <name> \
  --tag <tag> \
  --model_type <sample|...>
```

## 🏗️ Architecture Overview

This project uses a **dual-mode architecture**:

1. **Pipeline Compilation Mode** (`pipelines/main.py`): Compiles KFP pipeline definitions to YAML and uploads to Kubeflow
2. **Task Execution Mode** (`main.py`): Runs individual tasks inside KFP containers

### 🔄 How It Works

1. 📝 **Define tasks** in `tasks/<task_name>/` with settings and run logic
2. 🔗 **Create pipeline graphs** in `pipelines/graphs/` that chain tasks together
3. 📋 **Register components**: tasks in `main.py` task_maps and pipelines in `pipelines/main.py` pipeline_types
4. 📦 **Compile pipeline** with `compile_pipeline` - generates KFP YAML and uploads to registry
5. ▶️ **Execute**: KFP runs pipeline - each component executes `main.py` with task-specific arguments in containers

## ➕ Adding New Pipelines

### Step-by-Step Guide

#### 1️⃣ Define Model Type
Add your model type to [`const/model_type.py`](./const/model_type.py):
```python
class ModelType(StrEnum):
    """Enumeration for different Model Types."""

    SAMPLE = "sample"
    YOUR_MODEL = "your_model"  # ← Add this
```

#### 2️⃣ Create Pipeline Graph
Create a new file `pipelines/graphs/your_model.py`:
```python
from typing import TYPE_CHECKING

from kfp import dsl
from pipelines.components import (
    evaluation,
    feature_engineering,
    training,
    inference,
    export,
)

if TYPE_CHECKING:
    from kfp.dsl.graph_component import GraphComponent
    from pipelines.settings import PipelineCompileArgs


def get_pipeline(args: PipelineCompileArgs) -> GraphComponent:
    """Get your model pipeline.

    Args:
        args (PipelineCompileArgs): Pipeline arguments for compilation.

    Returns:
        GraphComponent: Pipeline Graph Component.
    """

    @dsl.pipeline(name=args.pipeline_name)
    def pipeline_def(execution_date: str) -> None:
        fe_task = feature_engineering(
            image=args.image,
            execution_date=execution_date,
            model_type=args.model_type,
        ).set_display_name("Feature Engineering")

        training_task = (
            training(
                image=args.image,
                execution_date=execution_date,
                model_type=args.model_type,
            )
            .after(fe_task)
            .set_display_name("Train Model")
        )
        # Add more tasks...

    return pipeline_def
```

#### 3️⃣ Implement Tasks
Create task implementations in `tasks/<task_name>/run.py`:
```python
from logging import getLogger

from tasks.base import T_co
from tasks.training.settings import TrainingSettings

logger = getLogger(__name__)


class TrainingTask:
    """Training Task."""

    def __init__(
        self,
        *args: tuple[T_co],
        **kwargs: dict[str, T_co],
    ) -> None:
        """Initialize the Training Task."""
        self.settings = TrainingSettings()

    def run(self) -> None:
        """Run the Training Task."""
        logger.info("settings=%s", self.settings)
        # Your training logic here
```

#### 4️⃣ Register Components
**Register tasks** in [`main.py`](./main.py):
```python
task_maps: dict[ModelType, dict[Task, type[BaseTask]]] = {
    ModelType.SAMPLE: {
        Task.FEATURE_ENGINEERING: FeatureEngineeringTask,
        Task.TRAINING: TrainingTask,
        # ...
    },
    ModelType.YOUR_MODEL: {  # ← Add this
        Task.TRAINING: YourTrainingTask,
        # ...
    },
}
```

**Register pipeline** in [`pipelines/main.py`](./pipelines/main.py):
```python
from pipelines.graphs import sample, your_model

pipeline_types = {
    ModelType.SAMPLE: sample.get_pipeline,
    ModelType.YOUR_MODEL: your_model.get_pipeline,  # ← Add this
}
```

#### 5️⃣ Compile & Deploy
```bash
uv run nox -s compile_pipeline -- \
  --env dev \
  --pipeline_name your-model-pipeline \
  --tag v1.0.0 \
  --model_type your_model
```

> 💡 **Tip**: See [CLAUDE.md](./CLAUDE.md) for detailed architecture patterns and development guidelines.

---

## 📚 Related Resources

### Official Documentation
- 📘 [Kubeflow Pipelines v2](https://www.kubeflow.org/docs/components/pipelines/v2/) - KFP documentation
- 📦 [uv Documentation](https://docs.astral.sh/uv/) - Python package manager
- 🔍 [Ruff Documentation](https://docs.astral.sh/ruff/) - Linter and formatter
- 📝 [SQLFluff Documentation](https://docs.sqlfluff.com/) - SQL linter and formatter
- ✅ [ty](https://github.com/astral-sh/ty) - Static type checker
- 🧪 [Pytest](https://docs.pytest.org/) - Testing framework
- 🔧 [Nox](https://nox.thea.codes/) - Task automation tool

### Kubeflow Pipelines
- [KFP SDK Reference](https://kubeflow-pipelines.readthedocs.io/en/stable/) - Python SDK documentation
- [Container Components Guide](https://www.kubeflow.org/docs/components/pipelines/v2/components/container-components/) - Building container-based components
- [Pipeline Compilation](https://www.kubeflow.org/docs/components/pipelines/v2/compile-a-pipeline/) - Compiling pipelines to YAML

### Python Libraries
- [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type annotations
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) - Settings management from environment variables

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### Development Workflow

1. 🍴 **Fork** the repository
2. 📥 **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ml-pipelines.git
   cd ml-pipelines
   ```
3. 🌿 **Create** a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. 📦 **Install** dependencies:
   ```bash
   uv sync
   ```
5. ✏️ **Make** your changes with tests
6. 🎨 **Format** code:
   ```bash
   uv run nox -s fmt
   ```
7. 🔍 **Lint** code:
   ```bash
   uv run nox -s lint -- --ruff --ty
   ```
8. ✅ **Test** changes:
   ```bash
   uv run nox -s test
   ```
9. 💾 **Commit** your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
10. 📤 **Push** to your branch:
    ```bash
    git push origin feature/amazing-feature
    ```
11. 📮 **Submit** a pull request

### Code Standards

- ✅ Maintain **75%+ test coverage** (enforced by pytest)
- 🎨 Follow **Ruff** formatting and linting rules ([`ruff.toml`](./ruff.toml))
- 📝 Follow **SQLFluff** SQL formatting rules ([`.sqlfluff`](./.sqlfluff))
- 🔍 Pass **ty** type checking ([`ty.toml`](./ty.toml))
- 📝 Write **clear commit messages**
- 🧪 Add **tests** for new features
- 📚 Update **documentation** as needed

### Testing Naming Convention

Test files must follow the `test__*.py` format (note the double underscore):
- ✅ `test__base.py`
- ✅ `test__training.py`
- ❌ `test_base.py` (single underscore - won't be discovered)

---

## 📄 License

This project is licensed under the terms specified in the [LICENSE](./LICENSE) file.
