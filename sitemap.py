import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Sitemap:
    cities = {}
    services = {}
    cities_path = "sitemap_cities.json"
    services_path = "sitemap_services.json"
    cities_url = "https://www.styleseat.com/sitemap"
    services_url = "https://www.styleseat.com/sitemap/addison+il"

    def __init__(self):
        self.cities = self.get_data(self.cities_url, self.cities_path)
        self.services = self.get_data(self.services_url, self.services_path)


    def get_data(self, url: str, path: str) -> dict:
        if not os.path.exists(path):
            self.scrap(url, path)

        with open(path, "r") as file:
            return json.load(file)


    def scrap(self, url: str, path: str) -> None:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
            By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/ul/li[1]/a')))

        hrefs = driver.find_elements(By.XPATH, '//*[@id="content"]/div[2]/div/div[*]/ul/li[*]/a')
        data = {}
        for href in hrefs:
            data[href.get_attribute("href").split("/")[-1]] = href.text

        with open(path, "w") as file:
            json.dump(data, file, indent=4)  # indent is number of spaces of tab

        driver.close()

