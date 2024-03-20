import csv
import os
import requests
from urllib.parse import urlparse
import mimetypes
import uuid
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

# Directory to store hashes of downloaded files
hashes_dir = 'downloaded_hashes'
os.makedirs(hashes_dir, exist_ok=True)
hashes_file_path = os.path.join(hashes_dir, 'downloaded_hashes.txt')


# Function to compute the hash of file content
def compute_hash(content):
    hasher = hashlib.sha256()
    hasher.update(content)
    return hasher.hexdigest()


# Function to check if the hash of the current file already exists
def is_duplicate(hash):
    with open(hashes_file_path, 'a+') as f:
        f.seek(0)
        existing_hashes = f.read().splitlines()
        if hash in existing_hashes:
            return True
        else:
            # Add the new hash to the file
            f.write(hash + '\n')
            return False


def download_file(url, base_folder):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_content = response.content
            file_hash = compute_hash(file_content)

            if is_duplicate(file_hash):
                return f"Skipped duplicate file: {url}"

            content_type = response.headers.get('content-type')
            type_folder = "videos" if 'video' in content_type else "images"

            downloads_folder = os.path.join(base_folder, 'downloads')
            target_folder = os.path.join(downloads_folder, type_folder)
            os.makedirs(target_folder, exist_ok=True)

            unique_filename = str(uuid.uuid4())
            extension = mimetypes.guess_extension(content_type) if content_type else os.path.splitext(urlparse(url).path)[1]
            filename = f"{unique_filename}{extension}"

            filepath = os.path.join(target_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(file_content)
            return f"Successfully downloaded {url} to {filepath}"
        else:
            return f"Failed to download {url}: Server responded with status code {response.status_code}"
    except Exception as e:
        return f"Exception occurred while trying to download {url}: {str(e)}"


def find_and_download_files(starting_directory):
    urls = []
    for root, dirs, files in os.walk(starting_directory):
        for file in files:
            if file == 'messages.csv':
                csv_path = os.path.join(root, file)
                with open(csv_path, mode='r', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        for column in row:
                            if column.startswith('https://cdn.discordapp.com/attachments/'):
                                urls.append((column, starting_directory))

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(download_file, url, base_folder): url for url, base_folder in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                print(data)
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")


# Replace 'your_starting_directory_here' with the path to your starting directory
starting_directory = 'messages'
find_and_download_files(starting_directory)
