from datetime import datetime
import pytz

def UnixToDatetime(timestamp, timezone=None):
    """Convert Unix timestamp to human-readable date."""
    try:
        # Handle millisecond timestamps
        if len(str(timestamp)) > 10:
            timestamp = timestamp / 1000
        dtObject = datetime.fromtimestamp(timestamp)
        if timezone:
            tz = pytz.timezone(timezone)
            dtObject = pytz.utc.localize(dtObject).astimezone(tz)
        return dtObject.strftime("%Y-%m-%d %H:%M:%S")
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

def InteractiveMode():
    """Run ChronoTool in interactive mode."""
    print("ChronoTool - Time Conversion")
    print("----------------------------")
    print("Enter a Unix timestamp or date (YYYY-MM-DD HH:MM:SS), or 'q' to quit")

    while True:
        userInput = input("\nInput: ").strip()
        if userInput.lower() == 'q':
            print("Goodbye!")
            break
        if userInput.isdigit():
            result = UnixToDatetime(int(userInput))
            print(f"Unix Timestamp: {userInput}")
            print(f"Converted Date: {result}")
        else:
            result = DatetimeToUnix(userInput)
            print(f"Date: {userInput}")
            print(f"Unix Timestamp: {result}")

if __name__ == "__main__":
    InteractiveMode()