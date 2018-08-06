#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:17:14 2018

"""

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import requests, json, subprocess, datetime
from nested_lookup import nested_lookup

app = Flask(__name__)
api = Api(app)

''''main'''


class main():
    def __init__(self):
        self.number_of_users = int(input('number of username/repos add : '))
        self.repos = []
        while (self.number_of_users != 0):
            self.user_name = input('user name: ')
            self.user_names.append(self.user_name)
            self.repo_name = input('repository name: ')
            self.repos.append(self.repo_name)
            self.number_of_users = self.number_of_users - 1


"""1.Total number of commit contributions to any project to which a user has a contributed."""


@app.route('', method=['GET'])
def total():
    git_commit_count = {}
    git_data = {}
    for u in range(0, len(git.user_names)):
        user = requests.get('https://api.github.com/repos/' + git.user_names[u] + '/' + git.repos[u] + '/commits')
        git_data['{0}'.format(git.user_names[u])] = json.loads(user.text)
        # print(self.git_data)

        for i in range(0, len(git.user_names)):
            git_user_data = {}
            result = result.get(["curl", "-H", "Accept: application/vnd.github.cloak-preview",
                                 "https://api.github.com/search/commits?q=author:" + git.user_names[
                                     i] + "&per_page=1000"], shell=False).decode('utf-8')
            git_user_data['{0}'.format(git.user_names[i])] = json.loads(result)
            results = nested_lookup(key='date', document=git_user_data, wild=True)
            results = list(set(results))
            results = [date for date in results if ("2018" in date)]
            git_commit_count['{0}'.format(git.user_names[i])] = len(results)
            #

        return (git_commit_count)


"""2.Total number of commit contributions as above, but restricted to projects that are members of the original submitted set."""


@app.route('/rate', method=['GET'])
def origin():
    commit_list = []
    # commit_count = 0
    page_number = 1
    pages = True
    for user in git.user_names:
        result = requests.get(
            "https://api.github.com/repos/" + git.user_name[user] + "/" + git.repos[
                user] + "/commits?since=2018-01-01",
            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(result.text)
        commit_list[user] = len(json_data)
    return commit_list


''' 
3.The number of known programming languages for each user (presuming that the languages of
             any repository committed to are known to the user) 
'''


@app.route('/language', method=['GET'])
def language():
    for j in range(0, len(git.user_names)):
        link = requests.get("https://api.github.com/users/" + git.user_names[j] + "/repos",
                            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(link.text)
        results = nested_lookup(key='full_name', document=json_data, wild=True)

        git_language = {}
        add_language = []
        for i in range(0, len(results)):
            link = requests.get("https://api.github.com/repos/" + results[i] + "/languages",
                                auth=('yangxiyucs', 'ab112113'))
            language_data = json.loads(link.text)
            for l in range(0, len(language_data)):
                add_language.append(list(language_data)[l])
            git_language[git.user_names[i]] = list(set(add_language))
    return (jsonify(git_language))


# 4.weekly commits in 2018
@app.route('/repo', method=['GET'])
def weekly():
    for i in range(0, len(git.user_names)):
        repos = requests.get('https://api.github.com/users/' + git.user_names[i] + '/repos?per_page=1000',
                             auth=('yangxiyucs', 'ab112113'))
    cmt_rate = {}
    # for repo in repos.json():
    #     print(repo)
    #     results = requests.get('https://api.github.com/repos/' + git.user_names[i] + '/' + str(
    #         repo['name']) + '/stats/participation?per_page=1000', auth=('yangxiyucs', 'ab112113'))
    #     weeks = results.json()['all']
    #     for i in weeks:
    #         pass
    for r in range(0, len(git.user_names)):
        link = requests.get(
            "https://api.github.com/repos/" + git.user_names[r] + "/" + git.repos[r] + "/stats/commit_activity",
            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(link.text)
        count = []
        for d in json_data:
            if (d['total'] != 0 and (
                    '2018' in (datetime.datetime.fromtimestamp(int(d['week'])).strftime('%Y-%m-%d %H:%M:%S')))):

                count.extend(
                    [datetime.datetime.fromtimestamp(int(d['week'])).strftime('%Y-%m-%d %H:%M:%S'), d['total']])
            else:
                continue
        cmt_rate[git.user_name[r]] = count
    return (cmt_rate)


"""  5. The average commit rate of each user to any project, for 2018."""


@app.route('/rate', method=['GET'])
def average():
    avg_cmt = {}
    for name in git.user_names:

        link = requests.get("https://api.github.com/users/" + name + "/repos?per_page=1000",
                            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(link.text)
        results = nested_lookup(key='name', document=json_data)
        count = 0
        counter = 0

        for i in results:
            link = requests.get("https://api.github.com/repos/" + name + "/" + i + "/" + "stats/commit_activity",
                                auth=('yangxiyucs', 'ab112113'))
            data = json.loads(link.text)

            for d in data:
                if (d['total'] != 0 and (
                        '2018' in (datetime.datetime.fromtimestamp(int(d['week'])).strftime('%Y-%m-%d %H:%M:%S')))):
                    count = d['total'] + count

                else:
                    pass
        avg_cmt[name] = (count / (len(results)))
    return jsonify(avg_cmt)


""" 6. The total number of collaborators in 2018 (ie. a count of other users who have 
contributed to any project that the user has contributed to)."""


def average():
    pass


if __name__ == "__main__":
    git = main()
    app.run(host='0.0.0.0', debug=True, port=8080)
