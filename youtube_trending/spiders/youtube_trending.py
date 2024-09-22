import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YoutubeTrendingSpider(scrapy.Spider):
    name = 'youtube_trending'
    allowed_domains = ['youtube.com']
    start_urls = ['https://www.youtube.com/feed/trending']

    def start_requests(self):
        yield SeleniumRequest(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        # Now you can access the Selenium driver
        driver = response.meta['driver']
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@id="video-title"]'))
            )
            video_links = driver.find_elements(By.XPATH,'//a[@id="video-title"]')
            links = [link.get_attribute('href') for link in video_links]

            limited_links = links[:10]

            if limited_links:
                self.logger.info(f"Video links are --> {limited_links}")
                for link in limited_links:
                    yield {'link':link}
            else:
                self.logger.warning("No video links found.")

        except Exception as e:
            self.logger.error(f"Error while retrieving video links : {e}")