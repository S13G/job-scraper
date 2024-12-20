from flask import jsonify, request

from scraper import create_app
from scraper.scrapers import scrape_flex_jobs, scrape_simply_hired, scrape_the_ladders

app = create_app()


@app.route("/scrape", methods=["POST"])
def scrape_jobs():
    try:
        # Parse the JSON payload
        data = request.json
        search_keyword = data.get("search_keyword", "")
        page_count = int(data.get("page_count", 1))

        if not search_keyword:
            return jsonify({"error": "search_keyword is required"}), 400

        # Collect job data
        all_job_data = []

        # Scraping
        print("Scraping The Ladders...")
        all_job_data.extend(scrape_the_ladders(search_keyword, page_count))

        print("Scraping SimplyHired...")
        all_job_data.extend(scrape_simply_hired(search_keyword, page_count))

        print("Scraping Flexjobs...")
        all_job_data.extend(scrape_flex_jobs(search_keyword, page_count))

        print(f"Length of all jobs: {len(all_job_data)}")

        # Return the results as JSON
        return jsonify({"jobs": all_job_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
