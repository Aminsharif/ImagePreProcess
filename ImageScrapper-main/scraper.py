# import os
# import time
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# import random


# def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
#     def scroll_to_end(wd):
#         wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(sleep_between_interactions)

#         # build the google query

#     search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
#     # load the page
#     wd.get(search_url.format(q=query))
#     print(search_url.format(q=query),'^^^^^^^^^^^^^^^^^^^^^')

#     res = set()
#     image_urls = set()
#     image_count = 0
#     results_start = 0
#     while image_count < max_links_to_fetch:
#         scroll_to_end(wd)

#         # get all image thumbnail results
#         thumbnail_results = wd.find_elements_by_css_selector("img.YQ4gaf")
#         number_results = len(thumbnail_results)

#         print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

#         for img in thumbnail_results[results_start:number_results]:
#             # try to click every thumbnail such that we can get the real image behind it
#             try:
#                 wd.execute_script("arguments[0].scrollIntoView(true);", img)
#                 time.sleep(random.uniform(0.5, 1.0))  # Randomized delay

#                 # Optionally, use ActionChains to move to the element
#                 actions = ActionChains(wd)
#                 actions.move_to_element(img).perform()
#                 img.click()
#                 time.sleep(sleep_between_interactions)
#             except Exception:
#                 print('exception.......')
#                 continue

#             # extract image urls
#             actual_images = wd.find_elements_by_css_selector('img.sFlh5c.FyHeAf.iPVvYb')

#             print(actual_images,'**************')
#             for actual_image in actual_images:
#                 if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
#                     image_urls.add(actual_image.get_attribute('src'))

#             image_count = len(image_urls)

#             if len(image_urls) >= 3:
#                 print(f"Found: {len(image_urls)} image links, done!")
#                 break
#         else:
#             print("Found:", len(image_urls), "image links, looking for more ...")
#             time.sleep(30)
#             return
#             load_more_button = wd.find_element_by_css_selector(".mye4qd")
#             if load_more_button:
#                 wd.execute_script("document.querySelector('.mye4qd').click();")

#         # move the result startpoint further down
#         results_start = len(thumbnail_results)

#     return image_urls


# def persist_image(folder_path:str,url:str, counter):
#     try:
#         image_content = requests.get(url).content

#     except Exception as e:
#         print(f"ERROR - Could not download {url} - {e}")

#     try:
#         f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
#         f.write(image_content)
#         f.close()
#         print(f"SUCCESS - saved {url} - as {folder_path}")
#     except Exception as e:
#         print(f"ERROR - Could not save {url} - {e}")


# def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
#     target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)

#     try:
#         with webdriver.Chrome(executable_path=driver_path) as wd:
#             res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
#             print(len(res), '#################')
#     except Exception as e:
#         print(e)


#     counter = 0
#     for elem in res:
#         persist_image(target_folder, elem, counter)
#         counter += 1


# # How to execute this code
# # Step 1 : pip install selenium. pillow, requests
# # Step 2 : make sure you have chrome installed on your machine
# # Step 3 : Check your chrome version ( go to three dot then help then about google chrome )
# # Step 4 : Download the same chrome driver from here  " https://chromedriver.storage.googleapis.com/index.html "
# # Step 5 : put it inside the same folder of this code


# DRIVER_PATH = './chromedriver'
# search_term = 'Cat'
# #num of images you can pass it from here  by default it's 10 if you are not passing
# number_images = 10
# search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=10)


# import os
# import time
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import mimetypes
# import logging
# import random
# from fake_useragent import UserAgent
# import traceback
# from selenium.webdriver.common.action_chains import ActionChains

# # Configure logging
# logging.basicConfig(
#     filename='image_scraper.log',
#     level=logging.INFO,  # Change to DEBUG for more verbose output
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: float = 1.0):
#     def scroll_to_end(wd):
#         wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.uniform(0.5, 1.5))  # Randomized delay

#     search_url = f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img"


#     print(search_url,'$$$$$$$$$$$$$$$$$$$$$$$$$$$')
#     # Load the page
#     try:
#         wd.get(search_url)
#     except Exception as e:
#         logging.error(f"ERROR - Could not load search URL: {e}\n{traceback.format_exc()}")
#         print(f"ERROR - Could not load search URL: {e}")
#         return set()

#     image_urls = set()
#     image_count = 0
#     results_start = 0

#     wait = WebDriverWait(wd, 10)

#     while image_count < max_links_to_fetch:
#         scroll_to_end(wd)

#         # Wait for thumbnails to load
#         try:
#             # Update the CSS selector based on manual inspection
#             thumbnail_results = wait.until(
#                 EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.YQ4gaf"))
#             )
#         except Exception as e:
#             logging.error(f"Error loading thumbnails: {e}\n{traceback.format_exc()}")
#             print(f"Error loading thumbnails: {e}")
#             break

#         number_results = len(thumbnail_results)
#         logging.info(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
#         print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

#         for img in thumbnail_results[results_start:number_results]:
            
#             # try:
#             #     # wd.execute_script("arguments[0].scrollIntoView(true);", img)
#             #     # time.sleep(random.uniform(0.5, 1.0))  # Randomized delay

#             #     # # Optionally, use ActionChains to move to the element
#             #     # actions = ActionChains(wd)
#             #     # actions.move_to_element(img).perform()
#             #     # img.click()
#             #     # time.sleep(sleep_between_interactions)

#             #     wd.execute_script("arguments[0].scrollIntoView(true);", img)
#             #     # wd.execute_script("window.scrollBy(0, -100);")  # Adjust this offset as needed
#             #     img.click()
#             #     original_class = img.get_attribute("class")
#             #     class_name = original_class.replace(" ", ".")
#             #     print(f"Class name of the element: {class_name}")


#             # except Exception as e:
#             #     logging.warning(f"Could not click image thumbnail: {e}\n{traceback.format_exc()}")
#             #     print(f"Could not click image thumbnail: {e}")
#             #     continue

           

#             # actual_images = wd.find_elements(By.CSS_SELECTOR, f"img.{class_name}")
#             # print(actual_images, '######################')
#             # for actual_image in actual_images:
#             #     src = actual_image.get_attribute('src')
#             #     if src and 'http' in src:
#             #         image_urls.add(src)

#             img_src = img.get_attribute("src")
#             print(f"Downloading Image: {img_src}")
#             if "https://" in img_src:
#                 image_urls.add(img_src)

#             image_count = len(image_urls)

#             if image_count >= max_links_to_fetch:
#                 logging.info(f"Found: {len(image_urls)} image links, done!")
#                 print(f"Found: {len(image_urls)} image links, done!")
#                 break
#             else:
#                 logging.info(f"Found: {len(image_urls)} image links, looking for more ...")
#                 print(f"Found: {len(image_urls)} image links, looking for more ...")
#                 time.sleep(30)
#                 # Attempt to load more images
#                 try:
#                     load_more_button = wd.find_element(By.CSS_SELECTOR, ".mye4qd")
#                     wd.execute_script("document.querySelector('.mye4qd').click();")
#                     logging.info("Clicked 'Load More' button.")
#                     print("Clicked 'Load More' button.")
#                 except Exception as e:
#                     logging.info(f"No more images found or error clicking load more button: {e}\n{traceback.format_exc()}")
#                     print("No more images found or error clicking load more button.")
#                     break

#         results_start = len(thumbnail_results)

#     return image_urls

# def persist_image(folder_path: str, url: str, counter: int):
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         image_content = response.content
#         content_type = response.headers.get('Content-Type')
#         extension =  '.jpg'
#     except Exception as e:
#         logging.error(f"ERROR - Could not download {url} - {e}\n{traceback.format_exc()}")
#         print(f"ERROR - Could not download {url} - {e}")
#         return

#     try:
#         file_path = os.path.join(folder_path, f'img_{counter}{extension}')
#         with open(file_path, 'wb') as f:
#             f.write(image_content)
#         logging.info(f"SUCCESS - saved {url} as {file_path}")
#         print(f"SUCCESS - saved {url} as {file_path}")
#     except Exception as e:
#         logging.error(f"ERROR - Could not save {url} - {e}\n{traceback.format_exc()}")
#         print(f"ERROR - Could not save {url} - {e}")

# def search_and_download(search_term: str, target_path='./images', number_images=4):
#     target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

#     if not os.path.exists(target_folder):
#         os.makedirs(target_folder)

#     # Set up User-Agent rotation
#     ua = UserAgent()
#     user_agent = ua.random

#     # Set up Chrome options
#     chrome_options = webdriver.ChromeOptions()
#     # Comment out headless mode for debugging
#     # chrome_options.add_argument('--headless')  # Runs Chrome in headless mode.
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument(f'user-agent={user_agent}')

#     # Initialize the WebDriver using webdriver-manager
#     try:
#         # service = Service(ChromeDriverManager().install())
#         driver_path ='D:\Python\ImageScrapper-main\ImageScrapper-main\chromedriver.exe'
#         wd = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

#         # wd = webdriver.Chrome(service=service, options=chrome_options)
#     except Exception as e:
#         logging.error(f"ERROR - Could not initialize WebDriver: {e}\n{traceback.format_exc()}")
#         print(f"ERROR - Could not initialize WebDriver: {e}")
#         return

#     try:
#         res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
#     finally:
#         wd.quit()

#     if res is None:
#         res = set()

#     counter = 0
#     for elem in res:
#         persist_image(target_folder, elem, counter)
#         counter += 1
#         # Optional: Introduce a small random delay to be polite
#         time.sleep(random.uniform(0.1, 0.5))

# if __name__ == "__main__":
#     search_term = 'airplane'
#     search_and_download(search_term=search_term, number_images=10)




import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import mimetypes
import logging
import random
from fake_useragent import UserAgent
import traceback
from selenium.webdriver.common.action_chains import ActionChains
import base64  
from PIL import Image
import io

logging.basicConfig(
    filename='image_scraper.log',
    level=logging.INFO,  # Change to DEBUG for more verbose output
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: float = 1.0):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(0.5, 1.5))  # Randomized delay

    search_url = f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img"


    print(search_url,'$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # Load the page
    try:
        wd.get(search_url)
    except Exception as e:
        logging.error(f"ERROR - Could not load search URL: {e}\n{traceback.format_exc()}")
        print(f"ERROR - Could not load search URL: {e}")
        return set()

    results_start = 0

    wait = WebDriverWait(wd, 10)


    # scroll_to_end(wd)
    for _ in range(max_links_to_fetch):  # Adjust the number based on the number of images wanted
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for images to load

    try:
        # Update the CSS selector based on manual inspection
        # thumbnail_results = wait.until(
        #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.YQ4gaf"))
        # )
        thumbnail_results = wd.find_elements_by_css_selector('img[class="YQ4gaf"]')
    except Exception as e:
        logging.error(f"Error loading thumbnails: {e}\n{traceback.format_exc()}")
        print(f"Error loading thumbnails: {e}")
        

    number_results = len(thumbnail_results)
    logging.info(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
    print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

    target_path='./images'
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for i, img in enumerate(thumbnail_results):
        img_url = img.get_attribute("src")
        if img_url and img_url.startswith('http'):
            img_response = requests.get(img_url)
            img_name = f"{i + 1}.jpg"  
            img_path = os.path.join(target_folder, img_name)

                # Save the image to computer
            with open(img_path, "wb") as img_file:
                    img_file.write(img_response.content)
        elif img_url and img_url.startswith('data:image/jpeg;base64'):
                # Decode base64 image data and save it
            img_data = img_url.split('base64,')[1]
            img = Image.open(io.BytesIO(base64.b64decode(img_data)))
            img_name = f"{i + 1}.jpg"  
            img_path = os.path.join(target_folder, img_name)
            img.save(img_path)


def search_and_download(search_term: str, number_images):
    
    ua = UserAgent()
    user_agent = ua.random

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    # Comment out headless mode for debugging
    # chrome_options.add_argument('--headless')  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'user-agent={user_agent}')

    # Initialize the WebDriver using webdriver-manager
    try:
        # service = Service(ChromeDriverManager().install())
        driver_path ='D:\Python\ImageScrapper-main\ImageScrapper-main\chromedriver.exe'
        wd = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

        # wd = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"ERROR - Could not initialize WebDriver: {e}\n{traceback.format_exc()}")
        print(f"ERROR - Could not initialize WebDriver: {e}")
        return

    try:
        fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
    finally:
        wd.quit()

   
if __name__ == "__main__":
    search_term = 'bus'
    search_and_download(search_term=search_term, number_images=20)



# import os
# import io
# import time
# import base64  
# import requests
# from PIL import Image
# from urllib.parse import quote
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

# # Enter query for Google search
# query = "plastic"

# # Convert the query into URL format
# query_url = quote(query)

# # Specify the desired folder path on the desktop
# folder_name = os.path.join('C:\\Users\\mahmu\\OneDrive\\Desktop', query)

# try:
#     # Create the folder if it doesn't exist
#     os.makedirs(folder_name)
# except Exception as e:
#     print(f"An error occurred: {str(e)}")

# # Initialize the Edge web browser using options and a service
# wd = './chromedriver'

# # URL for Google Images search
# # url = f"https://www.google.com/search?q={query_url}&tbm=isch"
# url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query_url}&oq={query_url}&gs_l=img"
# # load the page
# wd.get(url.format(q=query))


# # Simulate scrolling to load more images
# for _ in range(10):  # Adjust the number based on the number of images wanted
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)  # Wait for images to load

# try:
#     # Find all image elements
#     img_elements = driver.find_elements_by_css_selector('img.rg_i')
#     print(img_elements)
# except Exception as e:
#     print(f"An error occurred: {str(e)}")

# # Download and save images
# for i, img in enumerate(img_elements):
#     img_url = img.get_attribute("src")
#     if img_url and img_url.startswith('http'):
#         img_response = requests.get(img_url)
#         img_name = f"{i + 1}.jpg"  
#         img_path = os.path.join(folder_name, img_name)

#         # Save the image to computer
#         with open(img_path, "wb") as img_file:
#             img_file.write(img_response.content)
#     elif img_url and img_url.startswith('data:image/jpeg;base64'):
#         # Decode base64 image data and save it
#         img_data = img_url.split('base64,')[1]
#         img = Image.open(io.BytesIO(base64.b64decode(img_data)))
#         img_name = f"{i + 1}.jpg"  
#         img_path = os.path.join(folder_name, img_name)
#         img.save(img_path)

# print(f"Images have been downloaded and saved in the folder: {folder_name}")

# # Close the web browser
# driver.quit()
