import random
import time


def scroll_page(browser):
    scroll_time = random.uniform(0.5, 1.5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_time)
