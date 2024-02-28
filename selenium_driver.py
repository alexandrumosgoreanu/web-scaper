from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions() 
# options.add_argument("--headless")                  # Set the chrome webdriver to run in headless mode for scalability
options.add_experimental_option("detach", True)     # Keep browser open until .quit() is called
options.page_load_strategy = "normal"               # Wait until the ready state is complete
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

def get_rendered_html(url):
    driver.get(url)
    rendered_html = driver.page_source
    return rendered_html

def close_browser():
    driver.quit()