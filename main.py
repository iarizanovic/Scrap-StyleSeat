import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import scrape_salon
from sitemap import Sitemap

sitemap = Sitemap()

# Init the scraped_ids file
scraped_ids = []
scraped_ids_file_path = "scraped_ids.csv"
if os.path.exists(scraped_ids_file_path):
    scraped_ids = open(scraped_ids_file_path).read().splitlines()

# Init the scraped_urls file
scraped_urls = []
scraped_urls_file_path = "scraped_urls.csv"
if os.path.exists(scraped_urls_file_path):
    scraped_urls = open(scraped_urls_file_path).read().splitlines()

# Init the data CSV file and add the header
csv_path = "styleseat_data.csv"
if not os.path.exists(csv_path):
    with open(csv_path, mode="a", encoding='utf-8') as csv_file:
        csv_file.write('"salon_id","city_name","city_tag","search_url","url","title","subtitle",'
                       '"policy","hours","about_me","location","location_url","services","images"\n')

# Open the CSV files
scraped_ids_file = open(scraped_ids_file_path, "a")
scraped_urls_file = open(scraped_urls_file_path, "a")
csv_file = open(csv_path, mode="a", encoding='utf-8')

# Init the web driver
driver = webdriver.Chrome()

for city_tag, city_name in sitemap.cities.items():
    for service in sitemap.services:
        url = f"https://www.styleseat.com/m/search/{city_tag}/{service}"

        # Check if url is scraped
        if scraped_urls.count(url):
            continue

        # Set new URL to the driver
        driver.switch_to.window(driver.window_handles[0])
        driver.get(url)
        driver.maximize_window()

        # Close and Open the CSV files (ideal place to waiting for saving data in files)
        # csv_file.close()
        # scraped_ids_file.close()
        # scraped_urls_file.close()
        # scraped_ids_file = open(scraped_ids_file_path, "a")
        # scraped_urls_file = open(scraped_urls_file_path, "a")
        # csv_file = open(csv_path, mode="a", encoding='utf-8')

        # Wait for page loading
        try:
            element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="react-root"]/div/div/div/div/div/div/section/div[1]/div[2]/div[1]/ol/li[1]/div')))
        # Avoid empty pages
        except:
            scraped_urls.append(url)
            scraped_urls_file.write(f"{url}\n")
            continue

        # Clicking on more results button
        while True:
            try:
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,
                    '//*[@id="react-root"]/div/div/div/div/div/div/section/div[1]/div[2]/div[1]/ol/li[*]/button'))).click()
            except:
                break

        # Get all Salons from page
        salons = driver.find_elements(
            By.XPATH, '//*[@id="react-root"]/div/div/div/div/div/div/section/div[1]/div[2]/div[1]/ol/li[*]')

        salon_counter = len(salons)
        for salon in salons:
            driver.switch_to.window(driver.window_handles[0])
            salon_id = salon.get_attribute("data-pro-id")
            if scraped_ids.count(salon_id):
                salon_counter -= 1
                continue

            data = '"' + salon_id + '","' + city_name + '","' + city_tag + '","' + url + '","'

            # Get data of Salon
            salon.click()
            data_tmp = scrape_salon(driver)
            if data_tmp == "":
                salon_counter -= 1
                continue
            else:
                data += data_tmp

            # Add row in CSV file
            data = '\\n'.join(data.splitlines())
            csv_file.write(data[:-2] + '\n')

            # Add Salon ID in scraped list
            scraped_ids.append(salon_id)
            scraped_ids_file.write(f"{salon_id}\n")
            salon_counter -= 1

        # Add scraped url in scraped list of url
        if salon_counter == 0:
            scraped_urls.append(url)
            scraped_urls_file.write(f"{url}\n")

# Close the window
driver.quit()

# Close files
csv_file.close()
scraped_ids_file.close()
scraped_urls_file.close()

# https://www.styleseat.com/m/v/kellyfrazier
# https://www.styleseat.com/m/v/tanyarullan
# https://www.styleseat.com/m/v/michaelscott4
# https://www.styleseat.com/m/v/darlenedorsett
