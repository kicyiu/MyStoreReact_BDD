from behave import step, when, then
from Common.CommonFuncs import webcommon
from Common.CommonConfigs import locatorsconfig
from Common.CommonConfigs.urlconfig import URLCONFIG


@when("I click on the page name")
def i_click_on_the_page_name(context):

    locator_type = locatorsconfig.LOCATORS['page_name'].get('type')
    locator_text = locatorsconfig.LOCATORS['page_name'].get('locator')
    context.page_name_elem = webcommon.find_element(context, locator_type, locator_text)

    webcommon.click(context.page_name_elem)


@then("I should be redirected to '{page}' page")
def i_should_be_redirected_to_home_page(context, page):

    url = f"{URLCONFIG.get('base_url')}{URLCONFIG.get(page)}"
    webcommon.asset_current_url(context, url)


@when("I click on '{option}' option on the navbar")
def i_click_on_navbar_option(context, option):

    options_locator = locatorsconfig.NAV_BAR_LOCATORS['options']
    navbar_options_elems = webcommon.find_elements(context, options_locator.get('type'), options_locator.get('locator'))

    option_index = [i for i in range(len(navbar_options_elems)) if navbar_options_elems[i].text == option][0]
    selected_option = navbar_options_elems[option_index]

    selected_option.click()