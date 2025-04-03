import argparse
from datetime import datetime, timedelta
import pytz
import sys
from dateutil import parser as DateParser
from colorama import init, Fore, Style
import humanfriendly
import configparser
import os
import logging

# Initialize colorama
init()

# Add configuration loading
CONFIG_FILE = os.path.expanduser("~/.chronotoolrc")
Config = configparser.ConfigParser()
if os.path.exists(CONFIG_FILE):
    Config.read(CONFIG_FILE)

# Setup logging
def SetupLogging(logFile=None):
    if logFile:
        logging.basicConfig(
            filename=logFile,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

BANNER = r"""
   _____ _                        _______          _ 
  / ____| |                      |__   __|        | |
 | |    | |__  _ __ ___  _ __   ___ | | ___   ___ | |
 | |    | '_ \| '__/ _ \| '_ \ / _ \| |/ _ \ / _ \| |
 | |____| | | | | | (_) | | | | (_) | | (_) | (_) | |
  \_____|_| |_|_|  \___/|_| |_|\___/|_|\___/ \___/|_|                       
                    v0.1.0 - Time Conversion Utility   
"""

def UnixToDatetime(timestamp, timezone=None, outputFormat="%Y-%m-%d %H:%M:%S", verbose=False):
    """Convert Unix timestamp to human-readable date."""
    try:
        if len(str(timestamp)) > 10:
            timestamp = timestamp / 1000
        dtObject = datetime.fromtimestamp(timestamp)
        if timezone:
            tz = pytz.timezone(timezone)
            dtObject = pytz.utc.localize(dtObject).astimezone(tz)
        if outputFormat == "short":
            outputFormat = "%Y-%m-%d"
        elif outputFormat == "long":
            outputFormat = "%B %d, %Y %H:%M:%S"
        elif outputFormat == "iso":
            outputFormat = "%Y-%m-%dT%H:%M:%SZ"
        result = dtObject.strftime(outputFormat)
        if verbose:
            print(f"{Fore.BLUE}Verbose: Input={timestamp}, Timezone={timezone}, Format={outputFormat}{Style.RESET_ALL}")
        return f"{Fore.GREEN}{result}{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"

def DatetimeToUnix(dateStr, timezone=None):
    """Convert human-readable date to Unix timestamp."""
    try:
        dtObject = DateParser.parse(dateStr)  # Flexible parsing
        if timezone:
            tz = pytz.timezone(timezone)
            dtObject = tz.localize(dtObject)
        return int(dtObject.timestamp())
    except Exception as e:
        return f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"

def ParseRelativeTime(relativeStr, timezone=None):
    """Convert relative time (e.g., '2 days ago') to Unix timestamp."""
    try:
        relativeStr = relativeStr.lower().strip()
        isPast = "ago" in relativeStr
        timespanStr = relativeStr.replace("ago", "").replace("from now", "").strip()
        seconds = humanfriendly.parse_timespan(timespanStr)
        now = datetime.now(pytz.utc if timezone is None else pytz.timezone(timezone))
        dtObject = now - timedelta(seconds=seconds) if isPast else now + timedelta(seconds=seconds)
        return int(dtObject.timestamp())
    except Exception as e:
        return f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"

def CalculateTimeDelta(input1, input2, timezone=None):
    """Calculate time difference between two inputs."""
    try:
        if input1.isdigit() and input2.isdigit():
            dt1 = datetime.fromtimestamp(int(input1) / (1000 if len(input1) > 10 else 1))
            dt2 = datetime.fromtimestamp(int(input2) / (1000 if len(input2) > 10 else 1))
        else:
            dt1 = DateParser.parse(input1)
            dt2 = DateParser.parse(input2)
        if timezone:
            tz = pytz.timezone(timezone)
            dt1 = tz.localize(dt1) if dt1.tzinfo is None else dt1
            dt2 = tz.localize(dt2) if dt2.tzinfo is None else dt2
        delta = dt2 - dt1
        return f"{Fore.YELLOW}{humanfriendly.format_timespan(delta.total_seconds())}{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"

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

History = []
def InteractiveMode():
    """Run ChronoTool in interactive mode."""
    print("Enter a Unix timestamp, date, or 'history' to see past inputs, or 'q' to quit")
    while True:
        try:
            userInput = input("\nInput: ").strip()
            if userInput.lower() == 'q':
                print("Goodbye!")
                break
            elif userInput.lower() == 'history':
                print(f"{Fore.YELLOW}History:{Style.RESET_ALL}")
                for i, entry in enumerate(History, 1):
                    print(f"{i}. {entry}")
            else:
                History.append(userInput)
                if userInput.isdigit():
                    result = UnixToDatetime(int(userInput))
                    print(f"Result: {result}")
                else:
                    result = DatetimeToUnix(userInput)
                    print(f"Result: {result}")
        except KeyboardInterrupt:
            print("\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

def Main():
    parser = argparse.ArgumentParser(
        description="ChronoTool: A time conversion utility",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-t', '--timestamp', type=int, help="Convert Unix timestamp to date")
    parser.add_argument('-d', '--date', help="Convert date (any format) to Unix timestamp")
    parser.add_argument('-r', '--relative', help="Convert relative time (e.g., '2 days ago') to timestamp")
    parser.add_argument('-delta', nargs=2, help="Calculate time difference between two inputs")
    parser.add_argument('-f', '--format', default=Config.get('Settings', 'format', fallback="%Y-%m-%d %H:%M:%S"),
                        help="Output date format (e.g., %%Y-%%m-%%d) or 'short', 'long', 'iso'")
    parser.add_argument('-z', '--timezone', default=Config.get('Settings', 'timezone', fallback=None),
                        help="Time zone (e.g., US/Pacific)")
    parser.add_argument('-i', '--input', help="File with timestamps (one per line)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    parser.add_argument('-l', '--log', help="Log output to file")
    parser.add_argument('-V', '--version', action='store_true', help="Show version and exit")
    parser.add_argument('-zlist', '--timezone-list', action='store_true', help="List available time zones")
    parser.add_argument('-o', '--output', help="Export results to file")

    args = parser.parse_args()

    if args.log:
        SetupLogging(args.log)
        logging.info("ChronoTool started")

    if args.version:
        print("ChronoTool v0.1.0")
        sys.exit(0)

    print(BANNER)

    if args.timezone_list:
        print(f"{Fore.YELLOW}Available Time Zones:{Style.RESET_ALL}")
        for tz in pytz.all_timezones:
            print(tz)
    elif args.timestamp:
        result = UnixToDatetime(args.timestamp, args.timezone, args.format, args.verbose)
        print(f"{args.timestamp} -> {result}")
        if args.output:
            with open(args.output, 'a') as f:
                f.write(f"{args.timestamp} -> {result}\n")
        if args.log:
            logging.info(f"Converted timestamp {args.timestamp} to {result}")
    elif args.date:
        result = DatetimeToUnix(args.date, args.timezone)
        print(f"{args.date} -> {Fore.CYAN}{result}{Style.RESET_ALL}")
        if args.output:
            with open(args.output, 'a') as f:
                f.write(f"{args.date} -> {result}\n")
        if args.log:
            logging.info(f"Converted date {args.date} to {result}")
    elif args.relative:
        result = ParseRelativeTime(args.relative, args.timezone)
        print(f"{args.relative} -> {Fore.CYAN}{result}{Style.RESET_ALL}")
        if args.output:
            with open(args.output, 'a') as f:
                f.write(f"{args.relative} -> {result}\n")
        if args.log:
            logging.info(f"Converted relative time {args.relative} to {result}")
    elif args.delta:
        result = CalculateTimeDelta(args.delta[0], args.delta[1], args.timezone)
        print(f"Time difference: {result}")
        if args.output:
            with open(args.output, 'a') as f:
                f.write(f"Time difference between {args.delta[0]} and {args.delta[1]}: {result}\n")
        if args.log:
            logging.info(f"Calculated time delta: {result}")
    elif args.input:
        ProcessBatchFile(args.input, args.timezone, args.format)
        if args.log:
            logging.info(f"Processed batch file {args.input}")
    else:
        InteractiveMode()

if __name__ == "__main__":
    Main()