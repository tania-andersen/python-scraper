# Python Scraper
A simple usecase based scraping script for paginated result pages with links to detail pages. Written in Python with Playwright. Alpha version. License: The Unlicense.

ChatGPT wrote this documentation. It was fact-checked and edited by a human.

## scrape Function

The `scrape` function is a utility function for scraping web pages using Playwright. It takes the following parameters:

- `pagination_url_template` (required): A string that represents the URL template for the pages to be scraped. The template should include the page number as `*`. For example, `http://example.com/page-*`.
- `first_page` (required): An integer that represents the number of the first page to be scraped.
- `last_page` (required): An integer that represents the number of the last page to be scraped.
- `detail_url_selector` (required): A string that represents the CSS selector for the links to the detail pages.
- `wait_for_login_interaction` (optional): A boolean value that indicates whether the function should wait for a login interaction after the password submit, but before starting the scraping process, for adding a 2fa code and such. Default is `False`.
- `username` (optional): A string that represents the username to be used for login. Default is `None`.
- `username_selector` (optional): A string that represents the CSS selector for the username field on the login page. Default is `None`.
- `password_selector` (optional): A string that represents the CSS selector for the password field on the login page. Default is `None`.
- `login_url` (optional): A string that represents the URL of the login page. Default is `None`.

The function uses Playwright to launch a browser, navigate to the login page (if `username`, `username_selector`, `password_selector`, and `login_url` are provided), logs in (if `username` is provided), and then navigates to each page of the search results and extracts the URLs for the detail pages using the `detail_url_selector`. The detail pages are the downloaded to the folder detail_pages.

## Example

A simple example:

```python
scrape(
    pagination_url_template='http://books.toscrape.com/catalogue/page-*.html',
    first_page=1,
    last_page=5,
    detail_url_selector='article > h3 > a'
)
```

A full example:

```python
from scrape import scrape

pagination_url_template = "http://example.com/page-*"
first_page = 1
last_page = 5
detail_url_selector = "a.detail-link"
wait_for_login_interaction = True
username = "my_username"
username_selector = "#username"
password_selector = "#password"
login_url = "http://example.com/login"

scrape(
    pagination_url_template=pagination_url_template,
    first_page=first_page,
    last_page=last_page,
    detail_url_selector=detail_url_selector,
    wait_for_login_interaction=wait_for_login_interaction,
    username=username,
    username_selector=username_selector,
    password_selector=password_selector,
    login_url=login_url,
)
```
