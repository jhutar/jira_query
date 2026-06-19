.DEFAULT_GOAL := help
.PHONY: help bootstrap check check-all

help:
	@echo "Available targets:"
	@echo "  help                 - Show this help message"
	@echo "  bootstrap            - Install all development tools and hooks"
	@echo "  check                - Run checks on staged changes"
	@echo "  check-all            - Run checks on all files"

bootstrap:
	@echo "==> Installing Python 3.12 (via uv)..."
	uv python install 3.12
	@echo "==> Installing pre-commit..."
	uv tool install pre-commit || uv tool upgrade pre-commit
	@echo "==> Installing pre-commit hooks..."
	@PATH="$(HOME)/.local/bin:$(PATH)" pre-commit install
	@echo ""
	@echo "==> Bootstrap complete!"
	@echo "    Make sure $(HOME)/.local/bin is on your PATH."

check:
	pre-commit run

check-all:
	pre-commit run --all-files
