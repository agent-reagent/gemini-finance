import requests
from bs4 import BeautifulSoup
import json

excluded_urls = ["finance.yahoo.com", "google.com/finance"]


def search_duckduckgo(keywords):
    url = f"https://duckduckgo.com/html/?q={'+'.join(keywords)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return ""


def parse_results(html, keywords):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.select(".result")
    parsed_results = []

    for result in results:
        try:
            link = result.select_one(".result__a").get(
                "href"
            )  # Changed selector for link
            title = result.select_one(".result__a").text  # Changed selector for title
            description = result.select_one(
                ".result__snippet"
            )  # Kept the same selector for description

            if description:
                description = description.text
            else:
                description = ""

            result_data = {
                "Link": link,
                "Title": title,
                "Description": description,
            }

            # Check if the link is not in excluded URLs
            if not any(excluded_url in link for excluded_url in excluded_urls):
                # Check if any keyword is in title, description, or link
                if any(
                    keyword.lower() in result_data["Title"].lower()
                    or keyword.lower() in result_data["Description"].lower()
                    or keyword.lower() in result_data["Link"].lower()
                    for keyword in keywords
                ):
                    print(result_data)
                    parsed_results.append(result_data)
        except Exception as e:
            print(f"Error parsing result: {e}")

    return parsed_results


# keywords = ["tatasteel", "finance", "news"]


def perform_search(keywords):
    html = search_duckduckgo(keywords)

    if html:
        results = parse_results(html, keywords)
        if results:
            with open("results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        else:
            print("No results found.")
    else:
        print("Failed to fetch search results.")


# if __name__ == "__main__":
# perform_search(keywords = keywords)
