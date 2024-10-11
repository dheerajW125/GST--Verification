from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import json
from bson.json_util import dumps
import pandas as pd

 

 

def format_content(content):

    content = (

        content.replace("BUSINESS NAME", "BUSINESS_NAME")

        .replace("ENTITY TYPE", "ENTITY_TYPE")

        .replace("NATURE OF BUSINESS", "NATURE_OF_BUSINESS")

        .replace("Supplier of Services", "Supplier_of_Services")

        .replace("DEPARTMENT COD", "DEPARTMENT_COD")

        .replace("REGISTRATION TYPE", "REGISTRATION_TYPE")

        .replace("REGISTRATION DATE", "REGISTRATION_DATE")

        .replace("RANGE UMRER", "RANGE_UMRER")

    )

   

    lines = content.strip().split("\n")

    print(lines)

 

    formatted_data = {}

   

 

    # Split the text into key-value pairs

    try:

        for i in range(0, len(lines), 2):

            key = lines[i].strip()

            value = lines[i + 1].strip()

            formatted_data[key] = value

    except:

        return {"gst_val": "invalid"}

 

    return formatted_data

 

 

def valid(gst):

    print("GST",gst)

    options = Options()

 

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--allow-running-insecure-content")

    options.add_argument("--ignore-certificate-errors")

    options.add_argument("--log-level=3")

    options.add_argument("--mute-audio")

    options.add_experimental_option("excludeSwitches", ["enable-logging"])

 

    # Path to your ChromeDriver executable

    driver_path = r"C:\Users\dheer\Downloads\chromedriver-win64\chromedriver.exe"

    service = Service(executable_path=driver_path)

 

    # Initialize the WebDriver with service and options

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://cleartax.in/gst-number-search/")

   

    WebDriverWait(driver, 10).until(

        EC.visibility_of_element_located((By.XPATH, '//*[@id="input"]'))

    ).send_keys(gst)

   

    WebDriverWait(driver, 10).until(

        EC.visibility_of_element_located(

            (By.XPATH, '//*[@id="__next"]/div/div[4]/div[1]/div[2]/div[1]/div/button')

        )

    ).click()

   

    try:

        WebDriverWait(driver, 2).until(

            EC.presence_of_element_located(

                (

                    By.XPATH,

                    '//*[@id="__next"]/div/div[4]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/small',

                )

            )

        )

        results_element = WebDriverWait(driver, 20).until(

            EC.presence_of_element_located(

                (

                    By.XPATH,

                    '//*[@id="__next"]/div/div[4]/div[1]/div[2]/div[2]/div[1]/div/div',

                )

            )

        )

        content = results_element.text

        formatted_data = format_content(content)

        driver.quit()

        return formatted_data

    except (TimeoutException, NoSuchElementException):

        driver.quit()

        return {"gst_val": "invalid"}

# Store GST data into Excel
def store_to_excel(data):
    df = pd.DataFrame([data])  # Create DataFrame from the data
    df.to_excel('gst_data.xlsx', index=False)  # Save DataFrame to an Excel file

a = valid("27AHCPD8893P2ZJ") #exmple GST number
store_to_excel(a)
print(a)
