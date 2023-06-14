from selenium import webdriver
from Common.CommonConfigs import urlconfig
import logging as logger
import time


def go_to(context, location, **kwargs):
    """
    Function to start instance of the specified browser and navigate to the specified url.\

    :param context:
    :param location:
    :param kwargs:
    :return:
    """

    if not location.startswith('http'):
        _url = urlconfig.URLCONFIG.get(location)
        base_url = urlconfig.URLCONFIG.get('base_url')
        url = base_url + _url

    browser = context.config.userdata.get('browser')
    if not browser:
        browser = 'chrome'

    if browser.lower() == 'chrome':
        # create instance of Firefox driver the browser type is not specified
        context.driver = webdriver.Chrome()
    elif browser.lower() == 'headlesschrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        context.driver = webdriver.Chrome(options=options)
    elif browser.lower() in ('ff', 'firefox'):
        # create instance of the Chrome driver
        context.driver = webdriver.Firefox()
    elif browser.lower() == 'edge':
        context.driver = webdriver.Edge()
    else:
        raise Exception(f"The browser type '{browser}' is not supported")

    # clean the url and go to the url
    url = url.strip()
    logger.info(f"Navigating to URL: {url}")
    context.driver.get(url)


def element_contains_text(context_or_element, expected_text, locator_type, locator_text, case_sensitive=False):

    if isinstance(context_or_element, webdriver.remote.webelement.WebElement):
        element = context_or_element
    else:
        element = context_or_element.driver.find_element(locator_type, locator_text)

    element_text = element.text
    if not case_sensitive:
        if expected_text.lower() in element_text.lower():
            return True
        else:
            return False
    else:
        return True if expected_text in element_text else False


def assert_element_contains_text(context_or_element, expected_text, locator_type, locator_text, case_sensitive=False):

    max_try = 5
    sleep_bn_try = 2

    for i in range(max_try):
        try:
            contains = element_contains_text(context_or_element, expected_text, locator_type, locator_text, case_sensitive)
            assert contains, "Element does not contain text"
            break
        except AssertionError:
            print(f"Checking if element contains text. Retry number: {i}")
            time.sleep(sleep_bn_try)
    else:
        raise Exception(f"Element with locator type '{locator_type}', and locator text '{locator_text}', "
                        f"does not contains the text '{expected_text}'. Retried {max_try * sleep_bn_try} seconds")