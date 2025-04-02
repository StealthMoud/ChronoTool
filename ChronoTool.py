import argparse
from datetime import datetime
import pytz
import sys

BANNER =r"""
   _____ _                        _______          _ 
  / ____| |                      |__   __|        | |
 | |    | |__  _ __ ___  _ __   ___ | | ___   ___ | |
 | |    | '_ \| '__/ _ \| '_ \ / _ \| |/ _ \ / _ \| |
 | |____| | | | | | (_) | | | | (_) | | (_) | (_) | |
  \_____|_| |_|_|  \___/|_| |_|\___/|_|\___/ \___/|_|                       
                    v0.1.0 - Time Conversion Utility   
"""
def UnixToDatetime(timestamp, timezone=None, outputFormat="%Y-%m-%d %H:%M:%S"):
    """Convert Unix timestamp to human-readable date."""
    try:
        if len(str(timestamp)) > 10:
            timestamp = timestamp / 1000
        dtObject = datetime.fromtimestamp(timestamp)
        if timezone:
            tz = pytz.timezone(timezone)
            dtObject = pytz.utc.localize(dtObject).astimezone(tz)
        return dtObject.strftime(outputFormat)
    except Exception as e:
        return f"Error: {str(e)}"

def DatetimeToUnix(dateStr, timezone=None):
    """Convert human-readable date to Unix timestamp."""
    try:
        dtObject = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
        if timezone:
            tz = pytz.timezone(timezone)
            dtObject = tz.localize(dtObject)
        return int(dtObject.timestamp())
    except Exception as e:
        return f"Error: {str(e)}"

def ProcessBatchFile(filePath, timezone=None, outputFormat="%Y-%m-%d %H:%M:%S"):
    """Process timestamps from a file."""
    try:
        with open(filePath, 'r') as f:
            for line in f:
                timestamp = line.strip()
                if timestamp.isdigit():
                    result = UnixToDatetime(int(timestamp), timezone, outputFormat)
                    print(f"{timestamp} -> {result}")
                else:
                    print(f"Skipping invalid line: {timestamp}")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

def InteractiveMode():
    """Run ChronoTool in interactive mode."""
    print(BANNER)
    print("Enter a Unix timestamp or date (YYYY-MM-DD HH:MM:SS), or 'q' to quit")
    while True:
        userInput = input("\nInput: ").strip()
        if userInput.lower() == 'q':
            print("Goodbye!")
            break
        if userInput.isdigit():
            result = UnixToDatetime(int(userInput))
            print(f"Result: {result}")
        else:
            result = DatetimeToUnix(userInput)
            print(f"Result: {result}")

def Main():
    parser = argparse.ArgumentParser(
        description="ChronoTool: A time conversion utility",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-t', '--timestamp', type=int, help="Convert Unix timestamp to date")
    parser.add_argument('-d', '--date', help="Convert date (YYYY-MM-DD HH:MM:SS) to Unix timestamp")
    parser.add_argument('-f', '--format', default="%Y-%m-%d %H:%M:%S", help="Output date format (e.g., %%Y-%%m-%%d)")
    parser.add_argument('-z', '--timezone', help="Time zone (e.g., US/Pacific)")
    parser.add_argument('-i', '--input', help="File with timestamps (one per line)")

    args = parser.parse_args()

    print(BANNER)

    if args.timestamp:
        result = UnixToDatetime(args.timestamp, args.timezone, args.format)
        print(f"{args.timestamp} -> {result}")
    elif args.date:
        result = DatetimeToUnix(args.date, args.timezone)
        print(f"{args.date} -> {result}")
    elif args.input:
        ProcessBatchFile(args.input, args.timezone, args.format)
    else:
        InteractiveMode()

if __name__ == "__main__":
    Main()