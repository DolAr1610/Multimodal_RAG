import time
from datetime import datetime
from bs4 import BeautifulSoup
import json
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

BASE_TAG_URL = "https://www.deeplearning.ai/the-batch/tag/"
VALID_CATEGORIES = [
    "letters",
    "data-points",
    "research",
    "business",
    "science",
    "culture",
    "hardware",
    "ai-careers"
]


def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def load_all_articles(driver, url):
    wait = WebDriverWait(driver, 20)
    driver.get(url)
    time.sleep(3)

    category = url.split('/')[-2]
    all_articles_links = set()

    if category == "letters":
        last_url = ""
        while True:
            current_links = get_article_links_from_page(driver)
            all_articles_links.update(current_links)
            print(f"Collected {len(current_links)} articles on the current page in '{category}'")

            try:
                older_button = wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "justify-self-end"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", older_button)
                time.sleep(1)
                older_button.click()
                print(f"Clicked 'Older Posts' in'{category}'...")
                time.sleep(2)

                current_url = driver.current_url
                if current_url == last_url:
                    print("The URL did not change after the click, we are stopping the 'Older Posts' pagination.")
                    break
                last_url = current_url

            except (TimeoutException, NoSuchElementException):
                print("There is no 'Older Posts' button. Let's move on to the next category.")
                break

    else:
        while True:
            current_links = get_article_links_from_page(driver)
            all_articles_links.update(current_links)
            print(f"Collected {len(current_links)} articles on the current page in '{category}'")

            try:
                load_more_button = wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "buttons_secondary__8o9u6"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_button)
                time.sleep(1)
                load_more_button.click()
                print(f"Clicked 'Load More' in '{category}'...")
                time.sleep(2)
            except (TimeoutException, NoSuchElementException):
                print(
                    f"The 'Load More' button is unavailable or missing in '{category}'. Moving to the next category.")
                break

    return list(all_articles_links)


def get_article_links_from_page(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_links = set()
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.startswith("/the-batch/") and not href.startswith("/the-batch/tag/"):
            full_url = "https://www.deeplearning.ai" + href
            if "issue" not in full_url:
                all_links.add(full_url)
    return list(all_links)


def get_article_links():
    driver = initialize_driver()
    all_links = set()

    for category in VALID_CATEGORIES:
        url = f"{BASE_TAG_URL}{category}/"
        print(f"Loading the category: {url}")
        category_links = load_all_articles(driver, url)
        print(f"Found {len(category_links)} articles in category '{category}'")
        all_links.update(category_links)

    driver.quit()
    return list(all_links)


def parse_article(url, max_retries=3, delay=2):
    attempts = 0
    while attempts < max_retries:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            h1 = soup.find("h1")
            title = h1.get_text(strip=True) if h1 else ""
            description = ""
            if h1:
                span = h1.find("span")
                if span:
                    description = span.get_text(strip=True)
                    span.extract()
                title = h1.get_text(strip=True)

            image_tag = soup.find("meta", attrs={"property": "og:image"})
            image_url = image_tag["content"] if image_tag else None

            date_meta = soup.find("meta", attrs={"property": "article:published_time"})
            date_str = ""
            if date_meta:
                try:
                    date_raw = date_meta["content"]
                    date_str = datetime.fromisoformat(date_raw.split("T")[0]).strftime("%Y-%m-%d")
                except Exception:
                    date_str = date_meta["content"]

            content = ""
            main_content = soup.find("div", class_="prose--styled")

            if main_content:
                paragraphs = main_content.find_all(["p", "li"])
                content_lines = [p.get_text(strip=True) for p in paragraphs]
                content = "\n".join(content_lines)

            time.sleep(delay)

            return {
                "title": title.strip(),
                "description": description.strip(),
                "image_url": image_url,
                "date": date_str,
                "content": content.strip(),
                "source_url": url,
            }

        except (requests.RequestException, Exception) as e:
            attempts += 1
            print(f"Error parsing URL {url} (Attempt {attempts}/{max_retries}): {e}")
            time.sleep(delay * attempts)

    print(f"Article skipped due to repeated errors: {url}")
    return None


def run_parser_and_save_to_json(output_filename="data/articles_export.json"):
    print("Starting to parse article links...")
    all_article_urls = get_article_links()
    print(f"{len(all_article_urls)} unique links to articles collected.")

    parsed_articles = []
    print("\n Starting to parse article content...")
    for i, url in enumerate(all_article_urls):
        print(f"Parsing the article {i + 1}/{len(all_article_urls)}: {url}")
        article_data = parse_article(url)
        if article_data:
            parsed_articles.append(article_data)

    print(f"\n Parsing completed. {len(parsed_articles)} articles collected.")

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(parsed_articles, f, ensure_ascii=False, indent=4)
    print(f"All articles are saved in '{output_filename}'")

    print("\n Starting to parse articles...")
    try:
        with open(output_filename, "r", encoding="utf-8") as f:
            articles_to_filter = json.load(f)
    except FileNotFoundError:
        print(f"File '{output_filename}' not found for parse.")
        articles_to_filter = []

    initial_count = len(articles_to_filter)
    filtered_articles = [a for a in articles_to_filter if a.get("content") != "[image]"]
    filtered_count = len(filtered_articles)

    print(f"Articles for parse: {initial_count}")
    print(f"Parsed articles: {filtered_count}")

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(filtered_articles, f, ensure_ascii=False, indent=4)
    print(f"Parsed articles saved in '{output_filename}'")


if __name__ == "__main__":
    import os

    os.makedirs("data", exist_ok=True)
    run_parser_and_save_to_json()
