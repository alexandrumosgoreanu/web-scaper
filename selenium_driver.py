from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

def create_driver():    
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless=new")                  # Set the chrome webdriver to run in headless mode for scalability
    options.add_experimental_option("detach", True)     # Keep browser open until .quit() is called
    options.add_argument("--ignore-certificate-errors") # Set up the WebDriver with options to disable images
    # options.add_argument("--disable-proxy-certificate-handler")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-impl-side-painting")
    # options.add_argument("--disable-setuid-sandbox")
    # options.add_argument("--disable-seccomp-filter-sandbox")
    # options.add_argument("--disable-breakpad")
    # options.add_argument("--disable-client-side-phishing-detection")
    # options.add_argument("--disable-cast")
    # options.add_argument("--disable-cast-streaming-hw-encoding")
    # options.add_argument("--disable-cloud-import")  
    # options.add_argument("--disable-popup-blocking")
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--disable-session-crashed-bubble")
    # options.add_argument("--disable-ipv6")
    # options.add_argument("--allow-http-screen-capture")
    # options.add_argument("--disable-notifications")
    # options.add_argument("--timeout=5")
    options.page_load_strategy = "normal"               # Wait until the ready state is complete
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(6)
    return driver


