from datetime import datetime


def convert_timestamp():
    print("Unix Timestamp to Date Converter")
    print("--------------------------------")
    print("Enter a Unix timestamp to convert, or press 'q' to quit")

    while True:  # Loop until user chooses to quit
        user_input = input("\nEnter Unix timestamp (or 'q' to quit): ")

        # Check if user wants to quit
        if user_input.lower() == 'q':
            print("Goodbye!")
            break  # Exit the loop

        # Try to convert the timestamp
        try:
            timestamp = int(user_input)
            dt_object = datetime.fromtimestamp(timestamp)
            formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")

            print(f"Unix Timestamp: {timestamp}")
            print(f"Converted Date: {formatted_date}")

        except ValueError:
            print("Error: Please enter a valid numeric timestamp or 'q' to quit")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


# Run the program
if __name__ == "__main__":
    convert_timestamp()
