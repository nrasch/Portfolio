#!/bin/python3

# This is a quick script I put together to automate the process of creating release candidate branches in multiple repositories
# at the end of each sprint. 
# 
# The script first prompts the user for the release candidate branch name, then processes each
# repository in the REPOS list. 
# 
# It then checks out the staging branch, pulls the latest changes, creates a new branch from
# staging, checks out the new branch, and pushes the new branch to the remote repository. After processing all repositories,
# the script sends a message to the org-engineering Slack channel to inform the team that the release candidate branch
# has been created. 
# 
# The script also reminds the release manager to execute the post-processing tasks, such as adding all the sprint tickets
# to the master release ticket and deploying the new release candidate to Acceptance and/or Beta.


# Imports
import subprocess
import requests
from requests.exceptions import RequestException

# Constants
REPO_DIR = "/home/nrasch/work"  # Base directory for all repositories
REPOS = [  # List of repository paths
    f"{REPO_DIR}/eVisitReop1", 
    f"{REPO_DIR}/eVisitReop2", 
    f"{REPO_DIR}/eVisitReop3", 
    f"{REPO_DIR}/eVisitReop4"
]
STAGING_BRANCH = "staging"  # Name of the staging branch

# Global variables
err = False  # Flag to indicate if an error occurred during execution

def send_slack_message(url, message):
    # URL for Slack webhook - org-engineering channel
    url = 'https://hooks.slack.com/services/123ABC'
    
    # Send message to Slack
    response = requests.post(url, json={'text': message})
    response.raise_for_status()  # Raises an exception for non-2xx status codes

def get_user_input():
    while True:
        # Prompt user for release candidate branch name
        rc_branch = input("\nEnter release candidate name: ")
        confirm = input(f"\nYou entered '{rc_branch}'. Is this correct? [y|n] ").lower()
        if confirm == 'y':
            return rc_branch
        elif confirm != 'n':
            print("Please enter 'y' for yes or 'n' for no.")

def git_command(*args, repo_dir=REPO_DIR):
    try:
        # Execute git command with given arguments
        result = subprocess.run(
            ["git"] + list(args),
            check=True, text=True, capture_output=True, cwd=repo_dir
        )
        print(f"Command output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        global err
        err = True
        print(f"An error occurred: {e}\nError output: {e.stderr}")

def process_repo(repo, rc_branch):
    # Prompt user before processing each repository
    input(f"\nProcessing repo '{repo}'. Press 'enter' to continue...")
    # Git operations: checkout staging, pull latest changes, create new branch, checkout to new branch, push new branch
    git_command("checkout", STAGING_BRANCH, repo_dir=repo)
    git_command("pull", "origin", repo_dir=repo)
    git_command("branch", rc_branch, repo_dir=repo)
    git_command("checkout", rc_branch, repo_dir=repo)
    git_command("push", "--set-upstream", "origin", rc_branch, repo_dir=repo)

def main():
    # Get release candidate branch name from user
    rc_branch = get_user_input()

    # Process each repository in REPOS
    for i, repo in enumerate(REPOS):
        process_repo(repo, rc_branch)
        if i < len(REPOS) - 1:
            input("\nPress 'enter' to process next repo...\n")
    
    # If no errors occurred during processing
    if not err:
        # URL for Slack webhook - org-engineering channel
        url = 'https://hooks.slack.com/services/123abc'
        
        # Inform user that repos have been processed
        input("\nAll repos have been processed. Press 'enter' to send Slack message...")
        message = ':blob_excited:  The release candidate `'+rc_branch+'` branch has been created from staging and is now available for `Repo1`, `Repo2`, `Repo3`, and `Repo4`.'
        send_slack_message(url, message)

        # Guide user through post-processing tasks
        input("\nPlease add all the sprint tickets to the master Release ticket. Press 'enter' when done...")
        input("\nPlease deploy the new RC to Acceptance and/or Beta. Press 'enter' when done...")

        # Send a message after deployment
        input("\nPress 'enter' to send a Slack message letting everyone know the RC has been deployed...")
        message = ':blob_excited:  The release candidate `'+rc_branch+'` has been deployed for `eVisit Core` and `Bluestream`.  Testing can now commence.'
        send_slack_message(url, message)

if __name__ == "__main__":
    main()