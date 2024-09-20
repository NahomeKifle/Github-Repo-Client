#Name of programmer: Nahome Kifle

import requests
from dotenv import load_dotenv
import os
import time

load_dotenv() #getting the token from the secure .env file
API_TOKEN = os.getenv('API_TOKEN')

headers = {


    'Authetntication':f'token{API_TOKEN}'



}



def get_top_ten_repos(): #function that gets the top 10 repositories with the most stars
    url = 'https://api.github.com/search/repositories' #connecting to the github api of repos
    params = {
        'q':'stars:>1', #querring through the repos based on stars
        'sort': 'stars', #sorting
        'order': 'desc', # getting the top repos
        'per_page': 10 # getting 10 of those top repos
    }
    
    response = requests.get(url, headers=headers, params=params) #getting the data that qw just queried through and putting it into a repsonse variable

    if response.status_code == 200:
        return response.json()['items']
    elif response.status_code == 403:
        print("")
        time.sleep(600) #if it takes longer than 10 minutes 
        return get_top_ten_repos()
    else:
        print("")
        return[]
    
    
def get_bug_issue(owner, repo):#function to get the bugs
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    params = {
        'labels':'bug', #queries
        'state': 'open',
        'per_page': 1
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        issues = response.json()
        if issues:
            issue_title = issues[0]['title'] #gets the title of the bug
            issue_body = issues[0]['body'] or 'No description'
            return f"{issue_title}\n{issue_body}"
        else:
            return 'none'
    elif response.status_code == 403:
        print("")
        time.sleep(600) # if the time takes longer than 10 minutes
        return get_bug_issue(owner, repo)
    else:
        print("")
        return 'none'
    

def main():
    repos = get_top_ten_repos() #main function to run the two endpoints


    if repos:
        for repo in repos:
            repo_name = repo['full_name'] 
            stars = repo['stargazers_count']

            print(f"--------------------------------------------------")
            print(f"{repo_name}, {stars}")


            owner, repo_name = repo_name.split('/')


            bug_issue = get_bug_issue(owner, repo_name)


            print(f"Bug Issue:\n{bug_issue}")
            print(f"--------------------------------------------------")

if __name__ == '__main__':
    main()





