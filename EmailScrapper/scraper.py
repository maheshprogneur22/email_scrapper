# import re
# import time
# import html
# from bs4 import BeautifulSoup
# import undetected_chromedriver as uc
#
# EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
#
# def scrape_emails_from_url_list(urls):
#     results = []
#
#     options = uc.ChromeOptions()
#     options.headless = False  # Set to True after debugging
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#
#     # options.binary_location = "/usr/bin/google-chrome"
#
#     driver = uc.Chrome(options=options)
#
#     for url in urls:
#         try:
#             print(f"\n Scraping: {url}")
#             driver.get(url)
#
#             # Wait for full JavaScript rendering
#             print(" Waiting for JS to render...")
#             time.sleep(5)  # increase if needed
#
#             html_content = driver.page_source
#             soup = BeautifulSoup(html_content, 'html.parser')
#
#             # Extract emails from text
#             text = soup.get_text()
#             raw_emails = re.findall(EMAIL_REGEX, text)
#
#             # Extract emails from mailto links
#             mailto_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("mailto:")]
#             mailto_emails = []
#             for link in mailto_links:
#                 decoded = html.unescape(link)
#                 email = decoded[7:]
#                 mailto_emails.append(email)
#
#             all_emails = set(raw_emails + mailto_emails)
#             print(f" Found emails: {all_emails}")
#
#             results.append({'url': url, 'emails': ', '.join(all_emails)})
#
#         except Exception as e:
#             print(f" Error scraping {url}: {e}")
#             results.append({'url': url, 'emails': f"Error: {str(e)}"})
#
#     driver.quit()
#     return results
#
# # Run for testing
# if __name__ == "__main__":
#     urls = ["https://www.indiafilings.com/search/mvk-housing-llp-cin-ACM-3650"]
#     emails_found = scrape_emails_from_url_list(urls)
#     print("\n📦 Final extracted emails:", emails_found)


import re
import html
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

async def scrape_single_url(url, browser):
    page = await browser.new_page()
    try:
        print(f"\n Scraping: {url}")
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state('networkidle')

        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        text = soup.get_text()
        raw_emails = re.findall(EMAIL_REGEX, text)

        mailto_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("mailto:")]
        mailto_emails = [html.unescape(link)[7:] for link in mailto_links]

        all_emails = set(raw_emails + mailto_emails)
        print(f" Found emails: {all_emails}")
        return {'url': url, 'emails': ', '.join(all_emails)}
    except Exception as e:
        print(f" Error scraping {url}: {e}")
        return {'url': url, 'emails': f"Error: {str(e)}"}
    finally:
        await page.close()

async def scrape_emails_from_url_list_async(urls):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for url in urls:
            result = await scrape_single_url(url, browser)
            results.append(result)
        await browser.close()
    return results

def scrape_emails_from_url_list(urls):
    return asyncio.run(scrape_emails_from_url_list_async(urls))
