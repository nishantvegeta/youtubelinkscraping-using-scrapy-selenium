import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from mysql.connector import Error

class YoutubeTrendingSpider(scrapy.Spider):
    name = 'youtube_trending'
    allowed_domains = ['youtube.com']
    start_urls = ['https://www.youtube.com/feed/trending']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # MySQL database connection setup
        self.db_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='5744',
            database='youtube_trending_db'
        )
        self.db_cursor = self.db_conn.cursor()

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

    def save_to_db(self, link):
        """Save the video link to the MySQL database."""
        try:
            # SQL query to insert the video link into the `trending_new` table
            insert_query = "INSERT INTO trending_new (link) VALUES (%s)"
            self.db_cursor.execute(insert_query, (link,))
            self.db_conn.commit()  # Commit the transaction
            self.logger.info(f"Link saved to database: {link}")
        except mysql.connector.Error as err:
            self.logger.error(f"Error while saving to database: {err}")

    def close(self, reason):
        """Close the MySQL connection when the spider finishes."""
        if self.db_conn.is_connected():
            self.db_cursor.close()
            self.db_conn.close()
            self.logger.info("MySQL connection closed.")