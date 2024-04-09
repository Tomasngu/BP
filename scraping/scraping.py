from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import shutil
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .drive_upload import *
import cv2


BUTTON_NUM_TO_STREAM = {
        1: 7,
        2: 5,
        3: 6,
        4: 8,
        5: 1,
        6: 2,
        7: 3,
        8: 4
}



def scrape_one_stream(directory, driver, camera_num, current_time):
    """
    Captures a fullscreen screenshot of a specified camera's live stream from the Prague Zoo website.

    Parameters:
    - directory (str): Path to save the screenshot.
    - driver (selenium.webdriver): Selenium WebDriver for web interaction.
    - camera_num (int): Number identifying the camera stream (1 to 8).
    - current_time (str): Current time in string format for filename uniqueness.
    """
    BUTTON_NUM_TO_STREAM = {
        1: 7,
        2: 5,
        3: 6,
        4: 8,
        5: 1,
        6: 2,
        7: 3,
        8: 4}

    stream_num = BUTTON_NUM_TO_STREAM[camera_num]
    url = f'https://www.zoopraha.cz/multimedia/prenos-z-udoli-slonu-zive?cam={stream_num}&res=h&start={stream_num}'
    driver.get(url)
    time.sleep(1)
    #driver.save_screenshot('a.png')
    try:
        cookie_button = driver.find_element(By.ID, 'acceptAll')
        cookie_button.click()  # If the element is found, click it
    except ElementNotInteractableException:
        pass
        #print('Element not clickable.')
    except NoSuchElementException:
        #print('Element not found')
        pass

    action = ActionChains(driver)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'playerSLONI')))
    # Replace with the correct ID or selector
    video_player = driver.find_element(By.ID, 'playerSLONI')
    action.double_click(video_player).perform()
    # driver.save_screenshot('b.png')
    dst = os.path.join(directory, f'screenshot{camera_num}_{current_time}.png')
    driver.save_screenshot(dst)
    crop_img(dst)


def crop_img(dst):
    """
    Crops image to the desired size 

    Args:
        dst (str): The image path
    """
    image_np = cv2.imread(dst)
    image_np = cv2.resize(image_np, (1920, 1080), interpolation=cv2.INTER_AREA)
    h, _, _ = image_np.shape
    image_np = image_np[0+35:h-45]
    cv2.imwrite(dst, image_np)


def scraping(directory):
    """
    Performs web scraping using Selenium, saves screenshots of a website,
    and stores them in the specified directory.

    Args:
        directory (str): The directory to save the screenshots.

    Returns:
        None
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    # Setup the driver
    now = datetime.now()
    current_time = now.strftime("%d_%m__%H_%M")
    chrome_options = Options()
    
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920,1080')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=chrome_options)
    #time.sleep(1)
    for i in range(1, 9):
        scrape_one_stream(directory, driver, i, current_time)
    driver.quit()
    
def scrape_one_stream_whole(directory, camera_num):
    """
    Performs web scraping using Selenium of only one camera

    Args:
        directory (str): The directory to save the screenshots.
        camera_num (int): The camera number

    Returns:
        None
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    # Setup the driver
    now = datetime.now()
    current_time = now.strftime("%d_%m__%H_%M")
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920,1080')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)    
    scrape_one_stream(directory, driver, camera_num, current_time)

def main():
    directory = './scraped_images'
    scraping(directory)
    # upload_to_drive(directory, 'test_3')


if __name__ == '__main__':
    main()
