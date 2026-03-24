.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running ty"
	@uv run ty check

.PHONY: release-dry
release-dry: ## Simulate the release process and show the next version
	@echo "🚀 Simulating release process..."
	@uv run semantic-release --noop version --print

.PHONY: release-stable
release-stable: ## Prepare project for stable 1.0.0 release (disables 0.x.x versions)
	@echo "🚀 Preparing for stable release..."
	@sed -i 's/allow_zero_version = true/allow_zero_version = false/' pyproject.toml
	@echo "Updated pyproject.toml: allow_zero_version = false"
	@echo "Next steps:"
	@echo "   1. git add pyproject.toml"
	@echo "   2. git commit -m 'chore: prepare for stable 1.0.0 release'"
	@echo "   3. Push to main - the next feat/fix commit will trigger 1.0.0"

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run python -m pytest --doctest-modules


.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
