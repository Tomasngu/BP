from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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


def find_or_create_folder(service, folder_name):
    # Search for the folder
    results = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false",
        spaces='drive',
        fields='files(id, name)').execute()
    items = results.get('files', [])

    # If found, return the first folder's ID
    if items:
        print(f"Found folder: {items[0]['name']} with ID: {items[0]['id']}")
        return items[0]['id']
    else:
        # If not found, create the folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Folder created: {folder_name} with ID: {folder.get('id')}")
        return folder.get('id')

from googleapiclient.http import MediaFileUpload

def upload_file(service, file_name, file_path, folder_id, mime_type='image/png'):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def auth():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("./token.json"):
    creds = Credentials.from_authorized_user_file("./token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())  
  service = build("drive", "v3", credentials=creds)

  return service

def upload_to_drive(dir, target):
    service = auth()
    folder_id = find_or_create_folder(service, target)
    for filename in os.listdir(dir):
        upload_file(service, filename, os.path.join(dir, filename), folder_id)

def scraping(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    # Setup the driver
    now = datetime.now()
    current_time = now.strftime("%d_%m__%H_%M")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--no-sandbox')
    

    # Set up the Chrome WebDriver with headless option
    driver = webdriver.Chrome(options=chrome_options)   
    BUTTON_NUM_TO_STREAM = {
        1:7,
        2:5,
        3:6,
        4:8,
        5:1,
        6:2,
        7:3,
        8:4}
    time.sleep(1)
    for i in range(1, 9):
        stream_num = BUTTON_NUM_TO_STREAM[i]
        url = f'https://www.zoopraha.cz/multimedia/prenos-z-udoli-slonu-zive?cam={stream_num}&res=h&start={stream_num}'
        driver.get(url)
        time.sleep(1)
        driver.save_screenshot('a.png')
        try:
            cookie_button = driver.find_element(By.CLASS_NAME, 'cc-allow')
            cookie_button.click()  # If the element is found, click it
        except ElementNotInteractableException:
            print('Element not clickable.')
        except NoSuchElementException:
            print('Element not found')
            
        action = ActionChains(driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'playerSLONI')))
        video_player = driver.find_element(By.ID, 'playerSLONI')  # Replace with the correct ID or selector
        action.move_to_element(video_player).perform()
        play_button = driver.find_element(By.CLASS_NAME, "jw-icon-playback")
        play_button.click()

        fullscreen_button = driver.find_element(By.CLASS_NAME, "jw-icon-fullscreen")
        fullscreen_button.click()
        time.sleep(1)
        dst = os.path.join(dir, f'screenshot{i}_{current_time}.png')
        driver.save_screenshot(dst)
    driver.quit()

def main():
    dir = './images'
    scraping(dir)
    upload_to_drive(dir, 'SLONI')

if __name__ == '__main__':
    main()
