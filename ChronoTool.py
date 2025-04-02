from datetime import datetime

def UnixToDatetime(timestamp):
    """Convert Unix timestamp to human-readable date."""
    try:
        dtObject = datetime.fromtimestamp(timestamp)
        return dtObject.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error: {str(e)}"

def InteractiveMode():
    """Run ChronoTool in interactive mode."""
    print("Unix Timestamp to Date Converter")
    print("--------------------------------")
    print("Enter a Unix timestamp to convert, or press 'q' to quit")

    while True:
        userInput = input("\nEnter Unix timestamp (or 'q' to quit): ")
        if userInput.lower() == 'q':
            print("Goodbye!")
            break
        try:
            timestamp = int(userInput)
            result = UnixToDatetime(timestamp)
            print(f"Unix Timestamp: {timestamp}")
            print(f"Converted Date: {result}")
        except ValueError:
            print("Error: Please enter a valid numeric timestamp or 'q' to quit")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    InteractiveMode()