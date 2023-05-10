#!/bin/bash

check_lint_command_exist(){
    if ! command -v $1 &> /dev/null; then
        echo "You have not installed $1. Please install this python package with: pip install $1"
    fi
}

check_lint_command_exist flake8
check_lint_command_exist isort
check_lint_command_exist black

check_format() {
    case "$1" in
        flake8)
            echo "$(date): $1 starting......"
            find . -name "*.py" -exec $1 {} +
            ;;
        isort)
            echo "$(date): $1 starting......"
            find . -name "*.py" -exec $1 --check-only {} +
            ;;
        black)
            echo "$(date): $1 starting......"
            find . -name "*.py" -exec $1 --check {} +
            ;;
        *)
            echo "$1 is not supported."
            exit 1
    esac

    exit_status=$?
    if [ $exit_status -eq 0 ]; then
        echo "$(date): $1 All done!"
    fi
}

check_format flake8
check_format isort
check_format black