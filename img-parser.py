import requests
from bs4 import BeautifulSoup
import argparse
import re

# Define command line arguments
parser = argparse.ArgumentParser(description='Find broken images on a website.')
parser.add_argument('base_url', type=str, help='The base URL of the website to search.')
parser.add_argument('start_page', type=int, help='The number of the starting page.')
parser.add_argument('end_page', type=int, help='The number of the ending page.')
parser.add_argument('--output_file', type=str, default='broken_images.txt', help='The path to the output file.')
args = parser.parse_args()

num_links_found = 0

# Loop through each page
for i in range(args.start_page, args.end_page + 1):
    # Construct the URL of the current page
    url = args.base_url.format(i)

    # Send a GET request to the page and get the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all images on the page
    images = soup.find_all('img')

    # Check if any of the images are broken
    for image in images:
        src = image.get('src')
        if not src:
            continue
        if src.startswith('http'):
            image_url = src
        else:
            # Find the base URL for relative paths
            base_url = re.search("(https?://.*?)/", url).group(1)
            image_url = base_url + src if src.startswith("/") else args.base_url.format(i) + src
        try:
            response = requests.get(image_url)
        except requests.exceptions.RequestException:
            continue
        if response.status_code != 200:
            # Write the broken image URL to the output file
            matching_link = f"{url} >> {image_url}"
            with open(args.output_file, 'a') as f:
                f.write(matching_link + '\n')
            num_links_found += 1

    # Print the current page being processed
    print(f"Processing page {i}...")

# Print the number of broken images found
if num_links_found > 0:
    print(f"Found {num_links_found} broken images.")
else:
    print("No broken images found.")
