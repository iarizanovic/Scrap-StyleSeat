import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_salon(driver) -> str:
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])

    # Get Salon URL
    url = driver.current_url.split('?')[0]
    data = url + '","'
    print(url)

    if url == "https://www.styleseat.com/m/404":
        driver.close()
        return ""

    # Wait for page loading
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
            '//*[@data-testid="profile-service-item-revamp-book-button"]')))
    except:
        pass

    # Get Salon title
    title = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="react-root"]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/h2'))).text
    data += title.replace('"', "'") + '","'

    # Get Salon subtitle
    subtitle = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="react-root"]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div/div[2]/div[2]/div'))).text
    data += subtitle.replace('"', "'") + '","'

    # Get information from right column
    right_column = driver.find_element(By.XPATH,
        '//*[@id="react-root"]/div/div/div/div/div/div[1]/div/div[2]/div/div[2]').text.splitlines()
    # Get Policy
    try:
        data += "\\n".join(right_column[right_column.index('No-Show / Late Cancellation Policy') + 1:]).replace('"', "'") + '","'
    except:
        data += '","'
    else:
        right_column = right_column[0:right_column.index('No-Show / Late Cancellation Policy')]
    # Get Hours of Operation and parsing
    try:
        hours = " ".join(right_column[right_column.index('Hours of Operation') + 1:])
    except:
        data += '","'
    else:
        hours = hours.replace(" Closed", "  Closed")
        hours = hours.replace(" -  ", "-")
        hours = hours.replace(":  ", "\n")
        hours = hours.replace(": ", "\n")
        hours = hours.replace("  ", "\n")
        hours = hours.replace("-", " - ")
        hours = hours.splitlines()
        hours_str = ""
        for i in range(int(len(hours)/2)):
            hours_str += hours[i] + ": " + hours[int(len(hours)/2) + i] + ", "
        data += hours_str[:-2] + '","'
        right_column = right_column[0:right_column.index('Hours of Operation')]

    # Get About me section
    try:
        data += "\\n".join(right_column[right_column.index('About Me') + 1:]).replace('"', "'") + '","'
    except:
        data += '","'
    else:
        right_column = right_column[0:right_column.index('About Me')]

    # Get Salon location
    try:
        data += "\\n".join(right_column[right_column.index('Location') + 1:]).replace('"', "'") + '","'
    except:
        data += '","'

    # Get Salon location url
    try:
        location_url = driver.find_element(By.XPATH,
            '//*[@id="react-root"]/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/div/div[2]/div[1]/a').get_attribute("href")
    except:
        try:
            location_url = driver.find_element(By.XPATH,
                '//*[@id="react-root"]/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/div/div/div[1]/a').get_attribute("href")
        except:
            location_url = ""

    data += location_url + '","'

    # Get information from left column
    left_column_click = driver.find_elements(By.XPATH,
    '//*[@data-testid="profile-service-item-revamp-description"]')
    for lll in left_column_click:
        try:
            lll.click()
        except:
            pass

    left_column = driver.find_element(By.XPATH,
        '//*[@id="react-root"]/div/div/div/div/div/div[1]/div/div[2]/div/div[1]/div[2]').text
    data += left_column.replace('"', "'") + '","'

    # Get paths of images
    try:
        driver.find_element(By.XPATH,
            '//*[@id="react-root"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/img').click()
    except:
        data += '","'
    else:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="react-root"]/div/div/div[1]/button')))
        except:
            pass
        else:
# Get all photos (without this it scrape max 20 photos but much faster)
#            # Get count of the images
#            img_count = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/div')
#            img_count = int(img_count.text.split("/")[1])
#
#            # Click on the arrow right 'img_count' times
#            while img_count:
#                try:
#                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
#                        '//*[@id="react-root"]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div[1]/div[1]/div/div[3]/div[3]/div/div/div'))).click()
#                except:
#                    pass
#                else:
#                    img_count -= 1

            imgs = driver.find_elements(By.XPATH,
                '//*[@id="react-root"]/div/div/div[2]/div[1]/div/div/div/div/div/div[*]/div[*]/div/div/img')
            img_urls = ""
            for img in imgs:
                img_urls += img.get_attribute("src") + ','

            data += img_urls[:-1] + '","'

    # Close the tab
    driver.close()
    return data
