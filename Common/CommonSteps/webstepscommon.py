from behave import step
from Common.CommonFuncs import webcommon


@step("I go to '{page}' page")
def go_to_page(context, page):

    print(f"Navigation to the page: {page}")
    webcommon.go_to(context, page)


