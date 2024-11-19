import time
from typing import List, Dict
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def scrape_the_ladders(search_keyword: str = "", page: int = 2) -> List[Dict[str, str]]:
    # Set the search parameters
    base_url = "https://www.theladders.com/jobs/searchresults-jobs"
    job_data = []  # List to store job dictionaries

    # Iterate through pages
    for page in range(1, page + 1):  # noqa
        query_params = {  # noqa
            "keywords": search_keyword.lower(),
            "order": "SCORE",
            "daysPublished": 7,
            "distance": 200,
            "page": page,
        }
        url = f"{base_url}?{urlencode(query_params)}"  # noqa

        try:
            # Make a GET request to the URL
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all job containers
            job_listings = soup.find_all(
                "div", class_="job-list-pagination-job-card-container"
            )

            # Extract data for each job listing
            for job in job_listings:
                title_tag = job.find("a", class_="clipped-text")
                title = title_tag.text.strip() if title_tag else "N/A"
                job_url = (
                    "https://www.theladders.com" + title_tag["href"]
                    if title_tag
                    else "N/A"
                )

                description_tag = job.find("p", class_="job-card-description")
                description = description_tag.text.strip() if description_tag else "N/A"

                location_tag = job.find("a", {"action": "job-card-location"})
                location = location_tag.text.strip() if location_tag else "N/A"

                remote_option_tag = job.find(
                    "span", {"data-testid": "remote-flag-badge"}
                )
                remote_option = (
                    remote_option_tag.text.strip() if remote_option_tag else "N/A"
                )

                salary_tag = job.find("p", class_="salary")
                salary = salary_tag.text.strip() if salary_tag else "N/A"

                # Append job data to the main list of dictionaries
                job_data.append(
                    {
                        "title": title,
                        "url": job_url,
                        "description": description,
                        "company": "N/A",
                        "salary": salary,
                        "location": location,
                        "remote_option": remote_option,
                        "schedule": "N/A",
                    }
                )

            print(f"Page {page} data has been added to the list.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        # Add a small delay to prevent overloading the server
        time.sleep(5)

    return job_data


def scrape_simply_hired(
    search_keyword: str = "", page: int = 2
) -> List[Dict[str, str]]:
    # Start URL and initial cursor
    base_url = "https://www.simplyhired.com/search"
    initial_url = f"{base_url}?q={search_keyword.lower()}&t=7"

    # Pagination using cursor
    next_cursor = None  # Initial cursor
    job_data = []

    # Iterate through pages using cursor
    for page in range(1, page + 1):  # noqa
        url = (
            f"{initial_url}&cursor={next_cursor}" if next_cursor else initial_url
        )  # noqa

        try:
            # Make a GET request to the URL
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all job containers
            job_listings = soup.find_all("li", class_="css-0")

            # Extract data for each job listing (similar to your existing logic)
            for job in job_listings:
                title_tag = job.find("a", class_="chakra-button css-1djbb1k")
                title = title_tag.text.strip() if title_tag else "N/A"
                job_url = (
                    "https://www.simplyhired.com" + title_tag["href"]
                    if title_tag
                    else "N/A"
                )

                company_tag = job.find("span", {"data-testid": "companyName"})
                company = company_tag.text.strip() if company_tag else "N/A"

                # Find location
                location_tag = job.find(
                    "span", {"data-testid": "searchSerpJobLocation"}
                )
                location = location_tag.text.strip() if location_tag else "N/A"

                remote_option = "N/A"
                if location == "Remote":
                    location = "N/A"
                    remote_option = "Remote"

                # Extract the description
                description_tag = job.find("p", {"data-testid": "searchSerpJobSnippet"})
                description = description_tag.text.strip() if description_tag else "N/A"

                salary_tag = job.find("p", class_="chakra-text css-1g1y608")
                salary = salary_tag.text.strip() if salary_tag else "N/A"

                schedule = "N/A"

                # Append job data to the main list of dictionaries
                job_data.append(
                    {
                        "title": title,
                        "url": job_url,
                        "description": description,
                        "company": company,
                        "salary": salary,
                        "location": location,
                        "remote_option": remote_option,
                        "schedule": schedule,
                    }
                )

            print(f"Page {page} data has been added to the list.")

            # Extract the next cursor from the pagination
            next_page_link = soup.find("a", {"aria-label": "Next page"})
            if next_page_link:
                next_cursor = next_page_link["href"].split("cursor=")[-1]
            else:
                print("No more pages available.")
                break

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        # Add a small delay to prevent overloading the server
        time.sleep(5)  # Adjust this delay as needed

    return job_data


def scrape_flex_jobs(search_keyword: str = "", page: int = 2) -> List[Dict[str, str]]:
    # Set the search parameters
    base_url = "https://www.flexjobs.com/search"
    job_data = []  # List to store job dictionaries

    # Iterate through pages
    for page in range(1, page + 1):  # noqa
        query_params = {  # noqa
            "searchkeyword": search_keyword.lower(),
            "page": page,
            "sortbyrelevance": "true",
        }

        url = f"{base_url}?{urlencode(query_params)}"  # noqa

        try:
            # Make a GET request to the URL
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all job containers
            job_listings = soup.find_all("div", class_="sc-14nyru2-2 fmkHkh")

            # Extract data for each job listing
            for job in job_listings:
                title_tag = job.find("a", class_="sc-jv5lm6-13 fQyPIb textWrap")
                title = title_tag.text.strip() if title_tag else "N/A"
                job_url = (
                    "https://www.flexjobs.com" + title_tag["href"]
                    if title_tag
                    else "N/A"
                )

                description_tag = job.find("p", class_="sc-jv5lm6-4 caAWyW")
                description = description_tag.text.strip() if description_tag else "N/A"

                remote_option_tag = job.find(
                    "li", id=lambda x: x and "remoteoption" in x
                )
                remote_option = (
                    remote_option_tag.text.strip() if remote_option_tag else "N/A"
                )

                schedule_tag = job.find("li", id=lambda x: x and "jobschedule" in x)
                schedule = schedule_tag.text.strip() if schedule_tag else "N/A"

                salary_tag = job.find("li", id=lambda x: x and "salartRange" in x)
                salary = salary_tag.text.strip() if salary_tag else "N/A"

                # Append job data to the main list of dictionaries
                job_data.append(
                    {
                        "title": title,
                        "url": job_url,
                        "description": description,
                        "company": "N/A",
                        "salary": salary,
                        "location": "N/A",
                        "remote_option": remote_option,
                        "schedule": schedule,
                    }
                )

            print(f"Page {page} data has been added to the list.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        # Add a small delay to prevent overloading the server
        time.sleep(5)

    return job_data
