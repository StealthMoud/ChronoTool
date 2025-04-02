# ChronoTool
A versatile time conversion utility.

## Installation
1. Clone the repository: `git clone https://github.com/StealthMoud/ChronoTool.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage
- Interactive mode: `python ChronoTool.py`
- Convert timestamp: `python ChronoTool.py -t 1617235200` or `--timestamp 1617235200`
- Convert date: `python ChronoTool.py -d "2025-04-02 12:00:00"`
- Batch process: `python ChronoTool.py -i timestamps.txt`
- Custom format: `python ChronoTool.py -t 1617235200 -f "%B %d, %Y"`
- Time zone: `python ChronoTool.py -t 1617235200 -z "US/Pacific"`

## Features
- Bidirectional time conversion (Unix to date and date to Unix)
- Time zone support with pytz
- Custom output formats
- Batch processing from files
- CLI and interactive modes