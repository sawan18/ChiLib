🏛️ ChiLib: Chicago Public Library Finder

📝 Project Overview

---

ChiLib is a powerful Command-Line Interface (CLI) tool designed to help users find Chicago Public Library branches quickly and efficiently. The application retrieves library information from the official City of Chicago open data repository and provides an intuitive search experience based on ZIP codes.

---

✨ Key Features

🔍 Search libraries by ZIP code

📋 View detailed library information

🕒 Track search history

🚨 Robust error handling

🌈 Rich, colorful terminal interface

---

🛠️ Prerequisites

Python 3.8+

pip (Python package manager)

---

🚀 Installation

Clone the repository:

git clone https://github.com/sawan18/chilib.git

cd chilib

Create a virtual environment (recommended):

bash:-

python3 -m venv venv

source venv/bin/activate

On Windows, use 'venv\Scripts\activate'

Install required dependencies:

bash:-

pip install -r requirements.txt

pip install requests termcolor pyfiglet rich

---

📦 Dependencies

requests
termcolor
pyfiglet
rich
typing

---

🖥️ Usage
Run the application:
bashCopypython library_finder.py

---

Available Commands

Enter a 5-digit ZIP code to find libraries
help: Display command menu
history: View recent searches
full: View detailed search history
exit or quit: Close the application

---

Example
Copy📮 Enter ZIP code (or 'help'): 60601
✅ Found 2 libraries:
🏛️ Library #1: Harold Washington Library Center
...

---

🔧 Configuration

The default data source is the City of Chicago's open data API
Maximum search history is set to 100 entries
Logging is configured to library_finder.log

---

🐛 Error Handling

Invalid ZIP codes are gracefully handled
Network errors are logged and reported
Comprehensive exception management

---

📄 Logging

Application logs are stored in library_finder.log, capturing:

Successful data loads

Error events

Timestamp and log levels

---

🤝 Contributing

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

---

🙌 Acknowledgments

City of Chicago Open Data Portal
Python Community
Open-source libraries used in this project

---

📞 Contact
Project Link: https://github.com/sawan18/ChiLib
