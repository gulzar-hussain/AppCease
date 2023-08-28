# AppCease
AppCease is a Python application designed to provide users with control over running processes on their system. It offers a simple and intuitive way to monitor and manage processes, schedule the termination of specific processes, and keep track of the current time.

# Features
List active processes on your system.
Schedule the termination of a specific process at a user-defined time.
Display the current time in real-time.

## How to Use

Clone this repository to your local machine:
git clone https://github.com/gulzar-hussain/AppCease.git
### Navigate to the project directory:
cd appcease

### Install the required dependencies using pip:

pip install -r requirements.txt

### Run the application:
python appcease.py

The application will launch, displaying a list of active processes on your system. You can update the list manually using the "Update List" button.

To schedule the termination of a process:

Select a process from the list.
Enter a schedule time in the format "HH:MM" in the provided entry field.
Click the "Schedule Stop" button to set the termination time for the selected process.
The application will also display the current time in the "HH:MM:SS" format, updating every second.

At the scheduled time, the application will automatically terminate the selected process.

# Compatibility
AppCease is compatible with both Windows and Linux operating systems.

# Contribution
Contributions are welcome! If you have suggestions, bug reports, or would like to contribute code, feel free to open an issue or submit a pull request.
