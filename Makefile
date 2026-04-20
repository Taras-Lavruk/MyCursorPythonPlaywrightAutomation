.PHONY: help test test-login test-login-headed test-login-report test-login-security install clean verify-env

# Virtual environment Python and pytest
VENV_BIN = .venv/bin
PYTEST = $(VENV_BIN)/pytest
PIP = $(VENV_BIN)/pip
PLAYWRIGHT = $(VENV_BIN)/playwright

# Load environment variables from .env if it exists
-include .env
export

# Use BROWSER from .env or default to chromium
BROWSER ?= chromium

# Default target
help:
	@echo "Available targets:"
	@echo "  install              - Install dependencies"
	@echo "  verify-env           - Verify environment configuration (.env)"
	@echo "  test                 - Run all tests"
	@echo "  test-login           - Run login page tests"
	@echo "  test-login-headed    - Run login tests with visible browser"
	@echo "  test-login-report    - Run login tests and generate HTML report"
	@echo "  test-login-security  - Run security-focused login tests"
	@echo "  test-login-parallel  - Run login tests in parallel"
	@echo "  test-login-video     - Run login tests with video recording"
	@echo "  clean                - Clean test reports and artifacts"

# Install dependencies
install:
	$(PIP) install -r requirements.txt
	$(PLAYWRIGHT) install $(BROWSER)

# Run all tests
test:
	$(PYTEST) -v --browser=$(BROWSER)

# Run login page tests
test-login:
	$(PYTEST) tests/e2e/test_login.py -v --browser=$(BROWSER)

# Run login tests with visible browser
test-login-headed:
	HEADLESS=false $(PYTEST) tests/e2e/test_login.py -v --browser=$(BROWSER)

# Run login tests and generate HTML report
test-login-report:
	mkdir -p reports
	$(PYTEST) tests/e2e/test_login.py -v --html=reports/login_test_report.html --self-contained-html --browser=$(BROWSER)
	@echo "Report generated: reports/login_test_report.html"

# Run security-focused tests
test-login-security:
	$(PYTEST) tests/e2e/test_login.py::TestLogin::test_login_handles_malicious_input -v --browser=$(BROWSER)
	$(PYTEST) tests/e2e/test_login.py::TestLogin::test_login_multiple_failed_attempts -v --browser=$(BROWSER)

# Run tests in parallel
test-login-parallel:
	$(PYTEST) tests/e2e/test_login.py -n auto -v --browser=$(BROWSER)

# Run tests with video recording
test-login-video:
	mkdir -p reports/videos
	RECORD_VIDEO=1 $(PYTEST) tests/e2e/test_login.py -v --browser=$(BROWSER)

# Clean reports and artifacts
clean:
	rm -rf reports/screenshots/* reports/videos/* reports/*.html
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# Verify environment configuration
verify-env:
	$(VENV_BIN)/python verify_env.py
