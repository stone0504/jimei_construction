# Jimei Site Monitor

This project monitors the Jimei website and captures screenshots at regular intervals.

## Features
- Automated website monitoring
- Screenshot capture functionality
- Configurable settings

## Requirements
- Python 3.7+
- Required packages: 
  - `selenium`
  - `schedule`

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Copy `config_demo.json` to `config.json` and modify settings:
```json
{
  "url": "https://example.com",
  "interval": 60,
  "output_dir": "screenshots"
}
```

## Usage
Run the main script:
```bash
python main.py
```

## File Structure
- `main.py` - Main application logic
- `screenshot.py` - Screenshot capture functionality
- `config_demo.json` - Example configuration file
- `.gitignore` - Specifies files to ignore in version control

## License
[MIT License](LICENSE)
