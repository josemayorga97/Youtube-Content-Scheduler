from seleniumbase import Driver
from PgYoutube import YoutubeClass


driver = Driver(uc=True)
driver.maximize_window()


yt_instance = YoutubeClass()
yt_instance.login_to_youtube(driver)
yt_instance.automate_content_planner(driver)
