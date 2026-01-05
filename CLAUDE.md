# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Kubeflow Pipelines (KFP) template for ML workflows built with Python, uv, and Ruff. The project uses a component-based architecture where ML tasks (feature engineering, training, evaluation, inference, export) are packaged as containerized KFP components and orchestrated into pipelines.

## Development Commands

### Package Management
- Install dependencies: `uv sync`
- Add a dependency: `uv add <package>`

### Testing
- Run all tests: `uv run nox -s test`
- Run tests with JUnit XML output: `uv run nox -s test -- --junitxml=<path>`
- Run a single test file: `uv run pytest tests/path/to/test__file.py`
- Coverage requirements: minimum 75% branch coverage (configured in pytest.ini)

### Code Quality
- Format code (Ruff): `uv run nox -s fmt -- --ruff`
- Format SQL (SQLFluff): `uv run nox -s fmt -- --sqlfluff`
- Lint with all tools: `uv run nox -s lint -- --pyright --ruff --sqlfluff`
- Lint with Pyright only: `uv run nox -s lint -- --pyright`
- Lint with Ruff only: `uv run nox -s lint -- --ruff`
- Lint with SQLFluff only: `uv run nox -s lint -- --sqlfluff`

### Pipeline Compilation
Compile and upload a pipeline to Kubeflow:
```bash
uv run nox -s compile_pipeline -- \
  --env dev \
  --pipeline_name sample-pipeline \
  --tag test \
  --model_type sample
```

## Architecture

### Core Concepts

**Task-based execution model**: The project uses a dual-mode architecture:
1. **Pipeline mode** (pipelines/): Compiles and uploads KFP pipeline definitions
2. **Task execution mode** (main.py): Runs individual tasks within containers

**Main entry points**:
- `main.py` - Task executor (runs inside KFP containers)
- `pipelines/main.py` - Pipeline compiler (builds and uploads pipeline YAML)

### Directory Structure

**const/** - Shared enumerations
- `Environment` (dev, prod)
- `ModelType` (sample, etc.)
- `Task` (feature_engineering, training, evaluation, inference, export)

**environments/** - Environment-specific settings
- Each environment (dev.py, prod.py) provides `get_env_settings()` returning project_id and location
- Dynamically loaded via `load_env_settings(env)` in environments/settings.py

**tasks/** - ML task implementations
- Each task has: `__init__.py`, `run.py`, `settings.py`
- All tasks implement the `BaseTask` protocol (must have `__init__` and `run()`)
- Task mapping in main.py routes model_type + task enum to correct implementation
- Tasks are instantiated and executed via `task.run()`

**pipelines/** - KFP pipeline definitions
- `components.py` - KFP container components (each runs `uv run main.py` with task args)
- `graphs/` - Pipeline graph definitions (e.g., sample.py)
- `settings.py` - Pipeline compilation arguments with environment-based configuration
- Pipeline registry in pipelines/main.py maps ModelType to pipeline graph functions

### Key Patterns

**Enum-based routing**: ModelType and Task enums drive dynamic dispatch
- `task_maps` in main.py: ModelType → Task → Task class
- `pipeline_types` in pipelines/main.py: ModelType → pipeline function

**Settings pattern**: Uses pydantic-settings with CLI parsing
- `CLIArgs` classes parse command-line arguments
- Settings classes in each task (e.g., TrainingSettings) load task-specific config
- `PipelineCompileArgs.build()` constructs environment-aware pipeline config

**Container-based execution**: All pipeline components execute via containers
- Components call `uv run main.py` with --task, --model_type, --execution_date args
- Image paths are templated using `{{$.inputs.parameters['image']}}`
- Container specs defined in pipelines/components.py

## Adding New Pipelines

1. Add new ModelType to const/model_type.py
2. Create pipeline graph in pipelines/graphs/<name>.py with `get_pipeline(args)` function
3. Register in pipelines/main.py `pipeline_types` dict
4. Create task implementations in tasks/ for each pipeline stage
5. Register tasks in main.py `task_maps`

## Testing Conventions

- Test files: `test__*.py` format (note double underscore)
- Test structure mirrors source structure in tests/
- Use pytest fixtures from tests/conftest.py
- Tests require 75% branch coverage to pass
