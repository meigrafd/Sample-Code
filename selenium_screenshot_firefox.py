from selenium import webdriver
import contextlib

@contextlib.contextmanager
def quitting(thing):
    yield thing
    thing.quit()

with quitting(webdriver.Firefox()) as driver:
    driver.implicitly_wait(10)
    driver.get('http://www.python.org/')
    driver.get_screenshot_as_file('python_org.png')
