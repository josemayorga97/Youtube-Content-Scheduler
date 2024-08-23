from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import os


class YoutubeClass:

    # checks if progress label contains any number. Returns true if it does not contain any number.
    def check_progress_label(self, driver):

        progress_label = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.progress-label"))
        )

        label_text = progress_label.text.strip()
        # return any(char.isdigit() for char in label_text)
        return "%" in label_text

    def get_info_from_script(self):

        # Get the file path for script
        file_path = os.path.join(
            os.path.expanduser("~"),
            "Desktop",
            "Daily_accounts",
            "bread_fall_daily",
            "Script_bread_fall_daily_youtube.txt",
        )

        info_dict = {}
        try:
            with open(file_path, "r") as file:
                current_key = None
                for line in file:
                    line = line.strip()  # Remove leading/trailing whitespace

                    if ":" in line:
                        current_key, value = line.strip().split(":", 1)
                        info_dict[current_key.strip()] = value.strip()
                    else:
                        # Append to description if same key
                        if current_key == "Description":
                            info_dict[current_key] += "\n" + line
                        else:
                            # Handle unexpected line format (optional)
                            print(f"Warning: Unexpected line format: {line}")

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")

        return info_dict

    def login_to_youtube(self, driver):

        # navigates to youtube webpage
        driver.get("https://www.youtube.com")

        # initialize a implicit wait
        wait = WebDriverWait(driver, 3600)

        # clicks on sign in button
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a.yt-spec-button-shape-next--size-m")
            )
        ).click()

        # Types user's gmail
        driver.type("#identifierId", "username")

        # MODIFY NEXT LINES OF CODE AS NECESSARY TO LOG IN
        # clicks twice on "Continue" button
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.AjY5Oe"))
        ).click()
        driver.sleep(5)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.AjY5Oe"))
        ).click()

        # waits for the webpage to be loaded
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#logo")))

    def automate_content_planner(self, driver):

        # initialize a implicit wait
        wait = WebDriverWait(driver, 3600)

        # Retrieve information from the file
        info = self.get_info_from_script()

        # Convert the starting date string to a datetime object
        start_date = datetime.strptime(info["Start_date"], "%m/%d/%Y")

        # this is used to access try-except only once
        verification_popup_handled = False

        for i in range(int(info["Last_day_uploaded"]), int(info["Upload_until_day"])):

            # Add i days to the starting date
            current_date = start_date + timedelta(days=i)
            # Format the date as desired (e.g., MM/DD/YYYY)
            formatted_date = current_date.strftime("%d/%m/%Y")

            # navigates to youtube webpage again
            driver.get("https://www.youtube.com")

            # Clicks on "Create" button
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.ytd-topbar-menu-button-renderer")
                )
            ).click()

            # Clicks on "Upload Video" option
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#primary-text-container")
                )
            ).click()

            # Get the file path for video
            file_path = os.path.join(os.path.expanduser("~"), info["Data_path"])

            # uploads video
            input_field = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            input_field.send_keys(file_path)

            # initialize a implicit wait
            waitPopUp = WebDriverWait(driver, 30)

            if not verification_popup_handled:

                # Waits for verification pop-up, but handles potential absence
                try:
                    waitPopUp.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "#cancel-button")
                        )
                    )
                    # If the pop-up appears, clicks on "Next" button
                    option_elements = driver.find_elements(
                        By.CSS_SELECTOR, "div.yt-spec-touch-feedback-shape__fill"
                    )
                    option_elements[len(option_elements) - 1].click()

                    # Switch to the newly opened tab
                    driver.switch_to.window(driver.window_handles[-1])

                    # clicks on "Continue" button
                    wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "button.AjY5Oe")
                        )
                    ).click()

                    # Wait for the tab to close
                    waitPopUp.until(lambda driver: len(driver.window_handles) == 1)
                    print("Tab closed. Switching to remaining tab...")

                    # Switch to the current tab (assuming only one tab remains)
                    driver.switch_to.window(driver.window_handles[0])

                    # waits for the webpage to be loaded
                    wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#textbox"))
                    )

                    verification_popup_handled = (
                        True  # Set flag after handling the popup once
                    )

                except TimeoutException:
                    # If the pop-up doesn't appear, continue normally
                    print("Verification pop-up not found. Continuing...")

            # Add title
            driver.wait_for_element("#textbox")
            title_element = driver.find_elements("#textbox")[0]
            title_element.clear()
            title_element.send_keys(f"Day {i+1} ")

            # Add Description
            description_element = driver.find_elements("#textbox")[1]
            description_element.clear()
            description_element.send_keys(info["Description"])

            # Clicks on "No, it's not made for kids" option
            driver.find_elements("#offRadio")[1].click()

            # Clicks on "Next" button for 3 times
            for i in range(0, 3):
                driver.find_elements("#next-button")[0].click()

            # Clicks on "Schedule" container
            driver.find_element("#second-container-expand-button").click()

            # Selects date on calendar
            driver.find_element("#datepicker-trigger").click()
            date_element = driver.find_elements("input.style-scope.tp-yt-paper-input")[
                1
            ]
            date_element.clear()
            date_element.send_keys(formatted_date)
            date_element.send_keys(Keys.ENTER)

            # writes the date on input field
            time_element = driver.find_element("input.style-scope.tp-yt-paper-input")
            time_element.clear()
            time_element.send_keys(info["Time"])

            while True:
                if self.check_progress_label(driver):
                    print(
                        "Progress label contains a number. Checking again in 5 seconds..."
                    )
                    driver.sleep(5)
                else:
                    print("Progress label is empty. Continuing with the code...")
                    break

            driver.sleep(2)

            # clicks on the "Publish" button
            option_elements = driver.find_elements(
                By.CSS_SELECTOR, "div.yt-spec-touch-feedback-shape__fill"
            )
            option_elements[len(option_elements) - 1].click()
            driver.sleep(5)

            # clicks on the "Close" button
            option_elements = driver.find_elements(
                By.CSS_SELECTOR, "div.yt-spec-touch-feedback-shape__fill"
            )
            option_elements[len(option_elements) - 1].click()
