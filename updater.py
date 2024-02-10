import requests
import os
import sys
import zipfile
import tempfile
import shutil


def check_for_updates(current_version, repo_owner, repo_name):
    releases_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    print(releases_url)
    try:
        response = requests.get(releases_url)
        release_info = response.json()
        latest_version = release_info["tag_name"]
        return latest_version
    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
        return None

def is_update_available(current_version, latest_version):
    return current_version < latest_version

def download_update(repo_owner, repo_name):
    releases_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    try:
        response = requests.get(releases_url)
        release_info = response.json()
        assets = release_info["assets"]

        # Assuming the first asset is a zip file
        update_url = assets[0]["browser_download_url"]
        print(update_url)
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "file1.zip")
            with open(zip_path, "wb") as zip_file:
                zip_file.write(requests.get(update_url).content)

            extract_path = os.path.join(temp_dir, "extracted_update")
            print("Extract Path: ", extract_path)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)

            # Replace old files with the updated ones
            update_files(extract_path)
            

    except requests.RequestException as e:
        print(f"Error downloading update: {e}")


def update_files(extract_path):
    # Replace old files with the updated ones
    app_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    print(app_dir)
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            src_path = os.path.join(root, file)
            relative_path = os.path.relpath(src_path, extract_path)
            dest_path = os.path.join(app_dir, relative_path)

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Copy the file to the destination
            shutil.copy2(src_path, dest_path)

def main():
    
    current_version = "v0.1.0"
    latest_version = check_for_updates(current_version, "panoschatzileontiadis", "Updating")

    if latest_version and is_update_available(current_version, latest_version):
        print("Update available. Downloading...")
        download_update("panoschatzileontiadis", "Updating")
        print("Update complete. Please restart the application.")
    else:
        print("Your application is up to date.")

if __name__ == "__main__":
    main()
