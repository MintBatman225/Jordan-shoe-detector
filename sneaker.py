import requests
import os
import random
from PIL import Image
from io import BytesIO

# Directory path for Black Cement sneakers
save_directory = 'University Blue 4s '

# Create the directory if it doesn't exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Set up API URL and headers
url = "https://the-sneaker-database.p.rapidapi.com/sneakers"
querystring = {"limit": "100", "brand": "Jordan", "name": "Jordan 4 University Blue"}

headers = {
    "x-rapidapi-key": "65123a43e9msh63d8132dc1a0b69p104ac6jsn8d95e9b33fa9",
    "x-rapidapi-host": "the-sneaker-database.p.rapidapi.com"
}

# API Call
try:
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()  # Raise an exception for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the API request: {e}")
    exit()

# Parse API response
response_json = response.json()

# Check if 'results' key is in the response
if 'results' not in response_json:
    print("No 'results' key in API response.")
    print(f"API Response: {response_json}")
    exit()

sneaker_data = response_json['results']

# Filter only Jordan sneakers (already in query, but just in case)
jordan_sneakers = [sneaker for sneaker in sneaker_data if sneaker.get('brand') == 'Jordan']

# Check if any Jordan sneakers were found
if not jordan_sneakers:
    print("No Jordan sneakers found in the API response.")
    exit()
else:
    print(f"Number of Jordan sneakers retrieved: {len(jordan_sneakers)}")

# Helper function to download and save images locally
def download_image(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(path)
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        raise  # Re-raise the exception to be handled upstream

# Process all retrieved images
for i, sneaker in enumerate(jordan_sneakers):
    # Check if image URL exists and is valid
    if ('image' in sneaker and sneaker['image'] and
        'original' in sneaker['image'] and sneaker['image']['original']):
        img_url = sneaker['image']['original']
    else:
        print(f"No image URL found for sneaker: {sneaker.get('name', 'Unknown')}")
        continue  # Skip this sneaker

    img_name = f"black_cement_3_{i+1}.jpg"
    local_img_path = os.path.join(save_directory, img_name)

    # Download and save image locally
    try:
        download_image(img_url, local_img_path)
        print(f"Downloaded: {img_name}")
    except Exception as e:
        print(f"Failed to download image {img_url}: {e}")
        continue  # Skip this sneaker

print(f"All images saved in '{save_directory}' directory.")
