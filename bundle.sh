#!/bin/env bash
if [ ! -d ~/.venv ]; then
    python -m venv .venv
fi
source .venv/bin/activate

python_version=$(python3 -V 2>&1 | awk '{print $2}' | cut -d. -f1-2)
# Check if the version is more than 3.11 (then we need to install pip)
if [[ "$python_version" > "3.11" ]]; then
    pip install --upgrade setuptools
fi
pip install -r requirements.txt
yes | pyinstaller --clean --onefile --windowed --name MealyMooreAnalyzer analyzer.py