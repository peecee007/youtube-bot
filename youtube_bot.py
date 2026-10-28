import random
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------- CONFIG --------------------
URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

PROXIES = [
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://proxy3:8080"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.6045.159 Mobile Safari/537.36"
]

COMMENTS = [
    "Great video!", "Love the content!", "Thanks for sharing!",
    "Nice explanation!", "This helped a lot."
]

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


# -------------------- HELPERS --------------------
def random_proxy():
    return random.choice(PROXIES)


def random_ua():
    return random.choice(USER_AGENTS)


def random_comment():
    return random.choice(COMMENTS)


def random_watch_time():
    # watch between 30 s and 3 min
    return random.randint(30, 180)


def like_video(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="like-button"]').click()
        logging.info("Liked video")
    except Exception:
        logging.warning("Could not like video")


def subscribe(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="subscribe-button"]').click()
        logging.info("Subscribed")
    except Exception:
        logging.warning("Could not subscribe")


# -------------------- MAIN LOOP --------------------
def view_and_interact(url):
    proxy = random_proxy()
    ua = random_ua()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(f"--proxy-server={proxy}")
    options.add_argument(f"user-agent={ua}")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # wait for video tag
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        driver.find_element(By.TAG_NAME, "video").click()

        # random watch duration
        time.sleep(random_watch_time())

        # like & subscribe (50 % chance each)
        if random.random() < 0.5:
            like_video(driver)
        if random.random() < 0.5:
            subscribe(driver)

        # comment
        comment = random_comment()
        comment_box = driver.find_element(By.ID, "comment")
        comment_box.send_keys(comment)
        driver.find_element(By.ID, "submit-comment").click()
        logging.info(f"Posted comment: {comment}")

        logging.info("View completed")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        driver.quit()


# run a few times
for _ in range(5):
    view_and_interact(URL)