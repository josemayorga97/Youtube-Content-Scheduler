# Daily Video Scheduler for Youtube Videos

This Python project automates uploading videos to a Youtube channel according to a schedule defined in a text file.

## Features

* Login to Youtube using provided credentials.
* Upload video from a specified location.
* Add title and description from a script file.
* Schedule video for future publication.
* Handles verification pop-up (if encountered).
 
## Requirements

* Python 3.x
* Selenium WebDriver
* SeleniumBase (optional, simplifies browser interaction)
* A web driver (e.g., ChromeDriver) for your chosen browser

## Installation

* Install Python 3 from https://www.python.org/downloads/
* Install Selenium WebDriver from https://pypi.org/project/selenium/
* Install SeleniumBase (optional) from https://pypi.org/project/seleniumbase/
* Download the appropriate web driver for your browser and place it in a directory accessible by your system (check documentation for specific browser).

## Script.txt

* The text file must contain the following information:
```sh
Email: your_email@example.com
Password: your_password
Data_path: location of the video file
Description: Description text for the videos
Start_date: MM/DD/YYYY (format of your starting date)
Time: Time for scheduling (in HH:MM format)
Last_day_uploaded: Integer (last uploaded day)
Upload_until_day: Integer (day to stop uploading)
```

## Usage

* Install Selenium and SeleniumBase (if needed) using:
```sh
pip install selenium seleniumbase.
``` 
* Place your video file in the specified Data_path in Script.txt.
* Update any necessary information in the script file (email, password, etc.).
* To initiate the automation process use:
```sh
python main.py
``` 


## Notes

* This script uses Selenium for browser automation, which can be fragile due to frequent website changes. You might need to update selectors or logic if Youtube's interface changes significantly.
* Uploading videos to Youtube may be subject to their terms of service and API limitations. Always check their documentation for the latest information.

## Disclaimer

This script is provided for educational purposes only. Use it responsibly and in accordance with Youtube's terms of service. Remember to create high-quality content that adds value to your viewers.

