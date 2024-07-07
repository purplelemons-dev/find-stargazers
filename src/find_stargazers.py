import requests
import dotenv
from os import environ
from os.path import exists


def get_repos_and_stargazers(username, token):
    base_url = "https://api.github.com"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    repos_url = f"{base_url}/users/{username}/repos"
    repos_response = requests.get(repos_url, headers=headers)

    if repos_response.status_code != 200:
        print(
            f"Failed to fetch repositories. Status code: {repos_response.status_code}"
        )
        print(f"Response: {repos_response.json()}")
        return

    repos = repos_response.json()

    for repo in repos:
        repo_name = repo["name"]
        stargazers_url = f"{base_url}/repos/{username}/{repo_name}/stargazers"
        stargazers_response = requests.get(stargazers_url, headers=headers)

        if stargazers_response.status_code != 200:
            print(
                f"Failed to fetch stargazers for {repo_name}. Status code: {stargazers_response.status_code}"
            )
            continue

        stargazers = stargazers_response.json()

        if stargazers:
            print(f"\nRepository: {repo_name}")
            print("Stargazers:")
            for stargazer in stargazers:
                print(f"- {stargazer['login']}")


username = input("Enter the GitHub username: ")
if exists(".env"):
    dotenv.load_dotenv()
token = environ.get("GITHUB_TOKEN")

get_repos_and_stargazers(username, token)
