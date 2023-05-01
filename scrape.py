# A simple script for use cased based scraping of paginated results. 
# Author: Tania Andersen and ChatGPT. tan .at. ing .dot. dk
# Alpha version. License: The Unlicense.

import getpass
import os
from typing import List
from urllib.parse import urljoin, urlparse
from playwright.sync_api import Playwright, sync_playwright, TimeoutError
import time
from random import randint, uniform


DETAIL_PAGES = 'detail_pages'

file_number = 0


def _login(page, login_selector: str, password_selector: str, login_url: str, username: str,
           wait_for_login_interaction: bool = False) -> None:
    # Go to the login page
    _goto_and_wait(login_url, page)

    # Fill in the login form
    page.fill(login_selector, username)
    _random_sleep(page)
    page.fill(password_selector, getpass.getpass(prompt='Enter your password: '))
    page.press(password_selector, 'Enter')

    # Wait for the user interaction if the parameter is set to True
    if wait_for_login_interaction:
        input('Waiting for user interaction. Press Enter to continue...')


def _extract_detail_urls(page, detail_url_selector: str, base_url: str = '') -> List[str]:
    # Check if the element with the specified selector exists on the page
    if not page.query_selector(detail_url_selector):
        print("Warning: no URLs found for selector '{}'".format(detail_url_selector))
        return []

    # Extract the detail page URLs from the current page
    urls = [a.get_attribute('href') for a in page.query_selector_all(detail_url_selector)]

    # Check if any URLs were found
    if not urls:
        print("Warning: no URLs found for selector '{}'".format(detail_url_selector))

    # Prefix the base URL if href is a partial URL
    urls = [urljoin(base_url, url) for url in urls]

    return urls


def _create_page(p):
    # Launch a new browser instance
    browser = p.chromium.launch(headless=False)

    # Create a new context
    context = browser.new_context()

    # Create a new page
    page = context.new_page()

    return browser, page


def _create_detail_pages_folder():
    # Create folder to save detail pages
    if not os.path.exists(DETAIL_PAGES):
        os.mkdir(DETAIL_PAGES)


def _download_detail_page(page, detail_url):
    global file_number
    _goto_and_wait(detail_url, page)
    file_name = os.path.join(DETAIL_PAGES, f"pagesource_{file_number:04d}.html")
    file_number += 1
    print(f"Downloading page source to {file_name}")
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(page.content())


def _goto_and_wait(detail_url: str, page: Page) -> None:
    print(f"Loading url: {detail_url}")
    page.goto(detail_url)
    _random_sleep(page)


def _scrape_pages(
        page,
        pagination_url_template: str,
        first_page: int,
        last_page: int,
        detail_url_selector: str
) -> None:
    _create_detail_pages_folder()

    for page_num in range(first_page, last_page + 1):
        # Go to the next page of the search results
        page_url = pagination_url_template.replace('*', str(page_num))
        _goto_and_wait(page_url, page)

        # Extract the detail page URLs from the current page
        detail_urls = _extract_detail_urls(page, detail_url_selector, base_url=page_url)

        # Download the detail pages to DETAIL_PAGES folder
        for detail_url in detail_urls:
            _download_detail_page(page, detail_url)


def _random_sleep(page: Page) -> None:
    # Wait for a random amount of time between 2 and 6 seconds
    time.sleep(uniform(2, 5))

    # Get the page viewport size
    viewport = page.viewport_size

    # Calculate the center point of the viewport
    center_x = int(viewport["width"] / 2)
    center_y = int(viewport["height"] / 2)

    # Move the mouse around randomly
    for _ in range(randint(2, 3)):
        x = center_x + randint(-100, 100)
        y = center_y + randint(-100, 100)
        page.mouse.move(x, y)

        # Wait for a short period of time between each move
        time.sleep(uniform(0.1, 0.2))

    # Scroll to the bottom of the page
    page.evaluate(
        '(async () => { await new Promise(resolve => { window.scrollTo(0, document.body.scrollHeight); setTimeout(resolve, 2000); }); })()')


def scrape(
        pagination_url_template: str,
        first_page: int,
        last_page: int,
        detail_url_selector: str,
        wait_for_login_interaction: bool = False,
        username: str = None,
        username_selector: str = None,
        password_selector: str = None,
        login_url: str = None
) -> None:
    with sync_playwright() as p:
        browser, page = _create_page(p)

        # Login
        if username and username_selector and password_selector and login_url:
            _login(page, username_selector, password_selector, login_url, username, wait_for_login_interaction)

        # Go to the first page of the search results
        # page.goto(url)

        # Scrape the search result pages
        _scrape_pages(page, pagination_url_template, first_page, last_page, detail_url_selector)

        browser.close()

# An example:
scrape(
    pagination_url_template='http://books.toscrape.com/catalogue/page-*.html',
    first_page=1,
    last_page=5,
    detail_url_selector='article > h3 > a'
)
