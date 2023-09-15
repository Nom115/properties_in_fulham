# Web Scraping Script for Rightmove.co.uk - Properties in Fulham London

This is a Python script for web scraping property data from [Rightmove.co.uk](https://www.rightmove.co.uk/). The script utilizes various Python libraries to scrape property data and then stores it in Google BigQuery for further analysis and visualization in Looker Studio.

## Prerequisites

Before running the script, make sure you have the following Python packages installed:

- `requests`: Used for making HTTP requests to the Rightmove website.
- `beautifulsoup4`: A library for parsing HTML and extracting data from web pages.
- `pandas`: Used for data manipulation and storage.
- `json`: Used for working with JSON data.
- `lxml`: A library for processing XML and HTML documents.
- `geopy`: Used for geocoding the property addresses.
- `os`: Used for setting environment variables.
- `pandas_gbq`: A library for uploading data to Google BigQuery.

You'll also need to set up your Google Cloud credentials and specify the BigQuery table and project where the scraped data will be stored. Make sure you replace the following placeholders in the script:

- `/google_auth.json`: Replace with the path to your Google Cloud authentication JSON file.
- `Bigquery_table_id`: Replace with the BigQuery table ID where you want to store the data.
- `Bigquery_project_id`: Replace with your Google Cloud project ID.

## Usage

1. Install the required Python packages:

   ```bash
   pip install requests beautifulsoup4 pandas json lxml geopy pandas-gbq
