from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# NB: The targeted website only seems to have posts from page 13

def get_screenshots(page_to_start,page_to_stop):
    """
    This python scripts uses Selenium library to crawl websites, dismiss pop-ups/alerts and take full page screeshots.
    To save on browser load time, I have set headless to true to avoid loading the UI.
    """
    options = Options()
    # Setting headless to True allows us to access Chrome for screenshot capture but without a user interface
    options.headless = True
    for page_number in range(page_to_start,page_to_stop+1):
        url=f"https://community.conrad.com/discussion/{page_number}"
        # Create a driver instance (driver) for the Chrome web browser
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

        # Fetch (driver.get) the community page specified in the URL to take a screenshot of it.
        driver.get(url)

        # set the page size to full scroll width &heaight to allow full page capture
        full_width  = driver.execute_script('return document.body.parentNode.scrollWidth')
        full_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(full_width, full_height)

        # Get page number to save screenshort by page number
        page_number=url.split("/")[-1]

        # Find the consent popup and click button to dismiss first before screenshot
        driver.find_element("xpath", '/html/body/div[1]/div[2]/div/div/a[1]').click()

        # Saves the fetched response as the screenshot
        driver.save_screenshot(f'screenshots/{page_number}.png')
        print(f"{url} captured and saved...")
        time.sleep(2)
        # Close (driver.quit) the driver and exit the program
        driver.quit()
get_screenshots(1,5)

