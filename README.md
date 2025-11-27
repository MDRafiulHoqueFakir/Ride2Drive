# Ride2Drive Automation

This project is a **Playwright-based automation framework** for the Ride2Drive application, featuring **Self-Healing** capabilities and an **Automatic Test Generator**.

## Features

### 🛡️ Self-Healing Framework
The project includes a `SelfHealingPage` wrapper that makes tests robust against UI changes.
- **Automatic Recovery**: Intercepts failed selector interactions (click, fill, etc.).
- **Heuristic Analysis**: Analyzes broken selectors to extract intent (ID, Name, Label).
- **Fuzzy Matching**: Uses intelligent fuzzy matching to find the closest interactive element if the exact ID/Name is changed.

### 🤖 Test Case Generator
A tool to automatically bootstrap test scripts.
- **Crawler**: Scans a target URL for interactive elements (inputs, buttons, dropdowns).
- **Code Generation**: Outputs a ready-to-run Playwright Python script.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MDRafiulHoqueFakir/Ride2Drive.git
   ```
2. Install dependencies:
   ```bash
   pip install playwright
   playwright install
   ```

## Usage

### Running the Main Test
The main automation script demonstrates the self-healing capability (it intentionally uses a broken selector to show recovery).
```bash
python Ride2Drive.py
```

### Generating New Tests
To generate a test script for a website:
```bash
python test_generator.py
```
This will create `generated_ride2drive_test.py`.

## Project Structure
- `Ride2Drive.py`: Main E2E test script.
- `self_healing.py`: Core logic for the Self-Healing Page Object.
- `test_generator.py`: Script to generate automation code from a URL.
- `verify_healing.py`: A utility script to verify the self-healing logic.
