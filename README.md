# ChronoTool
A versatile time conversion utility.

## Installation
1. Clone the repository: `git clone https://github.com/StealthMoud/ChronoTool.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage
- Interactive mode: `python ChronoTool.py`
- Convert timestamp: `python ChronoTool.py -t 1617235200`
- Convert date: `python ChronoTool.py -d "2025-04-02"`
- Relative time: `python ChronoTool.py -r "2 days ago"`
- Time delta: `python ChronoTool.py -delta "2025-01-01" "2025-12-31"`
- Batch process: `python ChronoTool.py -i timestamps.txt`
- Custom format: `python ChronoTool.py -t 1617235200 -f "long"`
- Time zone: `python ChronoTool.py -t 1617235200 -z "US/Pacific"`
- List time zones: `python ChronoTool.py -zlist`
- Export: `python ChronoTool.py -t 1617235200 -o output.txt`

## Features
- Bidirectional time conversion
- Relative time and time delta calculations
- Time zone support
- Custom output formats and styles
- Batch processing
- Logging and verbose mode
- Configuration via .chronotoolrc