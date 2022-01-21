"""
Simple web scraper which retrieves a list of company names from a trucking website.
"""
import requests
from lxml import html
from pprint import pprint

MAX_PAGES = 10
RESULTS_PER_PAGE = 21
DEFAULT_ROWS = 6
DEFAULT_COLS = 3

EXPECTED_RESULTS = MAX_PAGES * RESULTS_PER_PAGE


def get_page(skip):
    """
    Get HTML representation of webpage
    :param skip: pagination value
    :return: HTML object
    """
    url = f"https://cdllife.com/trucking/companies?skip={skip}"
    resp = requests.get(url)
    if resp.status_code != 200:
        log_error(f'Received non-200 response from URL: {url}')
    else:
        return html.fromstring(resp.content)


def get_names_from_page(page):
    """
    Get list of company names from webpage
    :param page: the webpage as HTML
    :return: (list) company names
    """
    # 3 rows of 3 cols, then 3 rows of 4 cols
    names = []
    row_cols = DEFAULT_COLS
    for row in range(2, DEFAULT_ROWS + 2):  # rows start at 2 in xpath
        if row > 4:
            row_cols = 4
        for col in range(1, row_cols+1):
            company_name = get_elm_text(page, row, col)
            names.append(company_name)
    return names


def get_elm_text(page, row, col):
    """
    Get Company name from HTML element
    :param page: HTML webpage
    :param row: row number for target element
    :param col: column number for target element
    :return: (str) company name
    """
    elm_xpath = f"//*[@id=\"sapper\"]/main/div/div[2]/div[{row}]/div[{col}]/a/div/div/div[2]/h2"
    try:
        elm = page.xpath(elm_xpath)[0]
        return elm.text
    except Exception as e:
        log_error(f"element not found at xpath: '{elm_xpath}'. Exception: {e}")


def log_error(msg):
    print(f'--- ERROR --- {msg}')


if __name__ == '__main__':
    company_names = []

    for page_num in range(0, MAX_PAGES):  # results 0-220
        page = get_page(page_num * RESULTS_PER_PAGE)
        company_names += filter(None, get_names_from_page(page))

    assert len(company_names) == EXPECTED_RESULTS
    pprint(company_names)
