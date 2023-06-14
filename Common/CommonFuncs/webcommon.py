import pdb

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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
        context.driver = webdriver.Chrome(ChromeDriverManager().install())
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

    # adding implicit wait
    wait = int(kwargs['implicitly_wait']) if 'implicitly_wait' in kwargs.keys() else 15
    context.driver.implicitly_wait(wait)

    # clean the url and go to the url
    url = url.strip()
    logger.info(f"Navigating to URL: {url}")
    context.driver.get(url)


def asset_current_url(context, expected_url):
    """
    Function to get the current url and assert it is same as the expected url.
    :param context:
    :param expected_url:
    :return:
    """
    # get the current url
    current_url = context.driver.current_url

    if not expected_url.startswith('http') and not expected_url.startswith('https'):
        expected_url = 'https://' + expected_url + '/'

    assert current_url == expected_url, "The current url is not as expected." \
                                        " Actual: {}, Expected: {}".format(current_url, expected_url)

    print("The page url is as expected.")


def find_element(context, locator_type, locator_text):
    """
    Finds an element and returns the element object.
    :param context:
    :param locator_attribute: what to use to locate (example, id, class, xpath,....)
    :param locator_text: the locator text (ex. the id, the class, the name,...)
    """

    possible_locators = ["id", "xpath", "link text", "partial link text", "name", "tag name", "class name",
                          "css selector"]

    if locator_type not in possible_locators:
        raise Exception('The locator attribute provided is not in the approved attributes. Or the spelling and format'
                        ' does not match. The approved attributes are : %s ' % possible_locators)
    try:
        element = context.driver.find_elements(locator_type, locator_text)
        return element
    except Exception as e:
        raise Exception(e)


def find_elements(context, locator_attribute, locator_text):
    """
    Finds an element and returns the element object.
    :param context:
    :param locator_attribute: what to use to locate (example, id, class, xpath,....)
    :param locator_text: the locator text (ex. the id, the class, the name,...)
    """

    possible_locators = ["id", "xpath", "link text", "partial link text", "name", "tag name", "class name", "css selector"]

    if locator_attribute not in possible_locators:
        raise Exception('The locator attribute provided is not in the approved attributes. Or the spelling and format does not match.\
                            The approved attributes are : %s ' % possible_locators)
    try:
        element = context.driver.find_elements(locator_attribute, locator_text)
        return element
    except Exception as e:
        raise Exception(e)


def element_contains_text(context_or_element, expected_text, locator_type, locator_text, case_sensitive=False):
    if isinstance(context_or_element[0], webdriver.remote.webelement.WebElement):
        element = context_or_element[0]
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


def assert_element_contains_text(context_or_element, expected_text, locator_type=None, locator_text=None, case_sensitive=False):

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


def click(context_or_element, locator_type=None, locator_text=None):

    if isinstance(context_or_element[0], webdriver.remote.webelement.WebElement):
        element = context_or_element[0]
    else:
        element = context_or_element.driver.find_element(locator_type, locator_text)
    element.click()