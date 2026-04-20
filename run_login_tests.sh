#!/bin/bash

# Login Test Runner Script
# Provides convenient commands to run different test scenarios

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create reports directory if it doesn't exist
mkdir -p reports/screenshots reports/videos

echo -e "${BLUE}=== Login Page Test Runner ===${NC}\n"

# Function to display menu
show_menu() {
    echo "Select test option:"
    echo "1) Run all login tests"
    echo "2) Run basic functionality tests only"
    echo "3) Run security tests only"
    echo "4) Run with HTML report"
    echo "5) Run in headless mode"
    echo "6) Run in headed mode (visible browser)"
    echo "7) Run with video recording"
    echo "8) Run in parallel"
    echo "9) Run single test (custom)"
    echo "0) Exit"
    echo ""
}

# Run tests based on selection
case "${1}" in
    1|all)
        echo -e "${GREEN}Running all login tests...${NC}"
        pytest tests/e2e/test_login.py -v
        ;;
    2|basic)
        echo -e "${GREEN}Running basic functionality tests...${NC}"
        pytest tests/e2e/test_login.py::TestLogin::test_login_page_loads \
               tests/e2e/test_login.py::TestLogin::test_login_form_elements_visible \
               tests/e2e/test_login.py::TestLogin::test_valid_login_redirects -v
        ;;
    3|security)
        echo -e "${GREEN}Running security tests...${NC}"
        pytest tests/e2e/test_login.py::TestLogin::test_login_handles_malicious_input \
               tests/e2e/test_login.py::TestLogin::test_login_multiple_failed_attempts -v
        ;;
    4|report)
        echo -e "${GREEN}Running tests with HTML report...${NC}"
        pytest tests/e2e/test_login.py -v --html=reports/login_test_report.html --self-contained-html
        echo -e "${YELLOW}Report generated: reports/login_test_report.html${NC}"
        ;;
    5|headless)
        echo -e "${GREEN}Running tests in headless mode...${NC}"
        HEADLESS=true pytest tests/e2e/test_login.py -v
        ;;
    6|headed)
        echo -e "${GREEN}Running tests in headed mode...${NC}"
        HEADLESS=false pytest tests/e2e/test_login.py -v
        ;;
    7|video)
        echo -e "${GREEN}Running tests with video recording...${NC}"
        RECORD_VIDEO=1 pytest tests/e2e/test_login.py -v
        echo -e "${YELLOW}Videos saved to: reports/videos/${NC}"
        ;;
    8|parallel)
        echo -e "${GREEN}Running tests in parallel...${NC}"
        pytest tests/e2e/test_login.py -n auto -v
        ;;
    9|custom)
        echo -e "${YELLOW}Enter test name (e.g., test_login_page_loads):${NC}"
        read test_name
        pytest tests/e2e/test_login.py::TestLogin::${test_name} -v
        ;;
    0|exit)
        echo -e "${GREEN}Exiting...${NC}"
        exit 0
        ;;
    *)
        show_menu
        read -p "Enter choice [0-9]: " choice
        $0 $choice
        ;;
esac

echo -e "\n${GREEN}✓ Tests completed!${NC}"
