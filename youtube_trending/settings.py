import shutil
import os

BOT_NAME = 'youtube_trending'

SPIDER_MODULES = ['youtube_trending.spiders']
NEWSPIDER_MODULE = 'youtube_trending.spiders'

# Scrapy-Selenium settings
SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = r'C:\Program Files\geckodriver-v0.35.0-win64\geckodriver.exe' # Geckodriver must be in your PATH
SELENIUM_DRIVER_ARGUMENTS = ['-headless']  # Optional: Run in headless mode

USE_SELENIUM = True  # Change this to False if you're not using Selenium

if USE_SELENIUM and not os.path.isfile(SELENIUM_DRIVER_EXECUTABLE_PATH):
    raise RuntimeError("geckodriver not found. Please ensure it is installed and available in your PATH.")


DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,  # This line is critical
}

ROBOTSTXT_OBEY = True  # Follow robots.txt rules
