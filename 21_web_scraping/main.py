import requests
from bs4 import BeautifulSoup

def build_github_url(user_input: str) -> str:
    user_input = user_input.strip().rstrip('/')
    if user_input.startswith("http"):
        return user_input
    return f"https://github.com/{user_input}"

def fetch_profile_image_url(github_url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    response = requests.get(github_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    profile_image = soup.find('img', class_='avatar-user')

    if not profile_image:
        raise ValueError("Profile image not found.")

    return profile_image.get('src')

def get_github_profile_image():
    user_input = input("Enter GitHub profile URL or username: ").strip()
    github_url = build_github_url(user_input)

    print(f"\n🔍 Scraping: {github_url}\n")

    try:
        image_url = fetch_profile_image_url(github_url)
        print(f"✅ Profile Image URL:\n{image_url}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Network error: {req_err}")
    except ValueError as ve:
        print(f"⚠️ {ve}")
    except Exception as e:
        print(f"❗ Unexpected error: {e}")

if __name__ == "__main__":
    print("🔎 GitHub Profile Image Scraper")
    print("-------------------------------")
    get_github_profile_image()
