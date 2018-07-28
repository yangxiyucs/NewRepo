#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:17:14 2018

"""

from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests, json, subprocess, datetime
from nested_lookup import nested_lookup

app = Flask(__name__)
api = Api(app)


class main():
    def __init__(self):
        self.number_of_users = int(input('username/repos add : '))
        self.user_names = []
        self.repos = []

        while (self.number_of_users != 0):
            self.user_name = input('user name: ')
            self.user_names.append(self.user_name)
            self.repo_name = input('repository name: ')
            self.repos.append(self.repo_name)
            self.number_of_users = self.number_of_users - 1

        self.git_data = {}
        for n in range(0, len(self.user_names)):
            user = requests.get('https://api.github.com/repos/' + self.user_names[n] + '/' + self.repos[n] + '/commits')
            self.git_data['{0}'.format(self.user_names[n])] = json.loads(user.text)
            print(self.git_data)

        self.git_commit_count = {}
        for i in range(0, len(self.user_names)):
            git_user_data = {}
            temp = subprocess.check_output(["curl", "-H", "Accept: application/vnd.github.cloak-preview",
                                            "https://api.github.com/search/commits?q=author:" + self.user_names[
                                                i] + "&per_page=1000"], shell=False).decode('utf-8')
            git_user_data['{0}'.format(self.user_names[i])] = json.loads(temp)
            results = nested_lookup(key='date', document=git_user_data, wild=True, with_keys=False)
            results = list(set(results))
            results = [x for x in results if ("2018" in x)]
            self.git_commit_count['{0}'.format(self.user_names[i])] = len(results)
            #
            repos = requests.get('https://api.github.com/users/' + self.user_names[i] + '/repos?per_page=100',
                                 auth=('yangxiyucs', '<token>'))
            for repo in repos.json():
                if not (repo['name'].startswith('docker')):
                    print('---------------')
                    print(repo['name'])
                    commits = requests.get('https://api.github.com/repos/' + self.user_names[i] + + str(
                        repo['name']) + '/stats/participation?per_page=1000', auth=('jpwhitemn', '<token>'))
                    weeks = commits.json()['all']
                    for i in weeks:
                        print(i)

        print(self.git_commit_count)


############################################################################################
"""Total number of commit contributions as above, but restricted to projects that are members of the original submitted set."""


############################################################################################


def calculate():
    commit_list = []
    commit_count = 0
    page_number = 1
    pages = True
    while (pages):
        link = requests.get(
            "https://api.github.com/repos/yangxiyucs/NewRepo/commits?page={}&per_page=100".format(page_number),
            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(link.text)
        print(pages)

        if (len(json_data) == 0):
            break
        for i in json_data:
            commit_list.append(i['sha'])
            print("Commit Sha: {}".format(i['sha']))

        if (len(json_data) == 0):
            print("End")
            pages = False
            break
        else:
        # print(link.headers.get('link'))
        # print("new")
        page_number = page_number + 1

    # json_data[0]['committer']['login'] == self.user_names[0]


if __name__ == "__main__":
    # Git = main()
    main()

    app.run(host='127.0.0.1', debug=True)
