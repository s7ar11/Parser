import requests
from bs4 import BeautifulSoup
import os
import time

# The URL of the website to search
base_url = 'https://antijob.net/class_war/{}'

# The link to search for
search_link = 'https://meduza.io/'

# The path to the output file
output_file = 'matching_links.txt'

# Create the output file if it doesn't exist
if not os.path.exists(output_file):
    with open(output_file, 'w'):
        pass

# Loop through each page
num_links_found = 0
for i in range(1, 2001):
    # Construct the URL of the current page
    url = base_url.format(i)

    # Send a GET request to the page and get the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all links on the page
    links = []
    if soup is not None:
        links = soup.find_all('a')

    # Check if the search link is in any of the links on the page
    if links:
        for link in links:
            if link.get('href') and search_link in link.get('href'):
                # Combine the main link page and the searching link without a hyphen
                matching_link = f"{url}>>{link.get('href')}"
                # Write the matching link to the output file
                with open(output_file, 'a') as f:
                    f.write(matching_link + '\n')
                num_links_found += 1

    # Wait for 5 seconds before processing the next page
    time.sleep(5)

    # Print the current page being processed
    print(f"Processing page {i}...")

# Print the number of links found
if num_links_found > 0:
    print(f"Found {num_links_found} matching links.")
else:
    print("No matching links found.")