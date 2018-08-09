#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:17:14 2018

"""
import subprocess

from flask import Flask, jsonify, render_template, flash
from flask_restful import Resource, Api
import requests, json, datetime
from nested_lookup import nested_lookup
from flask_mail import Mail, Message

app = Flask(__name__)
api = Api(app)
mail = Mail()
''''main'''
mail.init_app(app)
app.config.from_object('app.setting')


class main():
    def __init__(self):
        self.number_of_users = int(input('number of username/repos add : '))
        self.repos = []
        self.add = []
        self.user_names = []
        while (self.number_of_users != 0):
            self.user_name = input('user name: ')
            self.user_names.append(self.user_name)
            self.repo_name = input('repository name: ')
            self.repos.append(self.repo_name)
            self.number_of_users -= 1


"""1.Total number of commit contributions to any project to which a user has a contributed."""


@app.route('/t1', methods=['GET', 'POST'])
def total():
    git_commit_count = {}
    git_data = {}
    for u in range(0, len(git.user_names)):
        user = requests.get('https://api.github.com/repos/' + git.user_names[u] + '/' + git.repos[u] + '/commits')
        git_data[git.user_names[u]] = json.loads(user.text)

        for i in range(0, len(git.user_names)):
            git_user_data = {}
            url = "https://api.github.com/search/commits?q=author:" + git.user_names[i] + "&per_page=1000"
            headers = {'Accept': 'application/vnd.github.cloak-preview'}
            result = requests.get(url, headers=headers, auth=('yangxiyucs', 'ab112113'))
            git_user_data[git.user_names[i]] = json.loads(result.text)
            results = nested_lookup(key='date', document=git_user_data)
            results = list(set(results))
            results = [date for date in results if ("2018" in date)]
            git_commit_count[git.user_names[i]] = len(results)

    final = json.dumps({'Total Commit': git_commit_count})
    git.add.append(final)
    print(final)
    # print(jsonify({'count': git_commit_count}))
    # flash("success")
    return render_template('index.html', final=final)


"""2.Total number of commit contributions as above, but restricted to projects that are members of the original submitted set."""


@app.route('/t2', methods=['GET', 'POST'])
def origin():
    commit_list = {}
    for user in range(0, len(git.user_names)):
        result = requests.get(
            "https://api.github.com/repos/" + git.user_names[user] + "/" + git.repos[
                user] + "/commits?since=2018-01-01",
            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(result.text)
        commit_list[user] = len(json_data)

    final = json.dumps({'Original Commit': commit_list})
    git.add.append(final)
    print(final)
    return render_template('index.html', final=final)


'''
3.The number of known programming languages for each user (presuming that the languages of
             any repository committed to are known to the user)
'''


@app.route('/t3', methods=['GET', 'POST'])
def language():
    git_language = {}
    new_language = []
    for user in range(0, len(git.user_names)):
        link = requests.get("https://api.github.com/users/" + git.user_names[user] + "/repos",
                            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(link.text)
        results = nested_lookup(key='full_name', document=json_data)

        for i in range(0, len(results)):
            link = requests.get("https://api.github.com/repos/" + results[i] + "/languages",
                                auth=('yangxiyucs', 'ab112113'))
            language_data = json.loads(link.text)
            for l in range(0, len(language_data)):
                new_language.append(list(language_data)[l])
                # erase repeat language by set()
        listnew = list(set(new_language))
        git_language[git.user_names[user]] = listnew
        counter = len(listnew)
        print(counter)
    final = json.dumps({'Language Used': git_language})
    git.add.append(final)
    print(final)

    return render_template('index.html', final=final, counter=counter)


# 4.weekly commits in 2018
@app.route('/t4', methods=['GET', 'POST'])
def weekly():
    # for i in range(0, len(git.user_names)):
    #     repos = requests.get('https://api.github.com/users/' + git.user_names[i] + '/repos?per_page=1000',
    #                          auth=('yangxiyucs', 'ab112113'))
    cmt_rate = {}
    # for repo in repos.json():
    #     print(repo)
    #     results = requests.get('https://api.github.com/repos/' + git.user_names[i] + '/' + str(
    #         repo['name']) + '/stats/participation?per_page=1000', auth=('yangxiyucs', 'ab112113'))
    #     weeks = results.json()['all']
    #     for i in weeks:
    #         pass
    #
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
        cmt_rate[git.user_names[r]] = count
    final = json.dumps({'weekly commit': cmt_rate})
    git.add.append(final)
    print(final)
    return render_template('index.html', final=final)


"""  5. The average commit rate of each user to any project, for 2018."""


@app.route('/t5', methods=['GET', 'POST'])
def average():
    avg_cmt = {}
    for name in git.user_names:

        link = requests.get("https://api.github.com/users/" + name + "/repos?per_page=1000",
                            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(link.text)
        results = nested_lookup(key='full_name', document=json_data)
        count = 0

        for i in results:
            link = requests.get("https://api.github.com/repos/" + i + "/" + "stats/commit_activity",
                                auth=('yangxiyucs', 'ab112113'))
            if (len(link.text) != 0):
                data = json.loads(link.text)
            else:
                continue
            for d in data:
                if (d['total'] != 0 and (
                        '2018' in (datetime.datetime.fromtimestamp(int(d['week'])).strftime('%Y-%m-%d %H:%M:%S')))):
                    count = d['total'] + count

                else:
                    continue
        avg_cmt[name] = (count / (len(results)))
    git.add.append(json.dumps({'average commit rate(2018)': avg_cmt}))
    final = json.dumps({'average commit rate(2018)': avg_cmt})
    print(final)
    return render_template('index.html', final=final)


""" 6. The total number of collaborators in 2018 (ie. a count of other users who have
contributed to any project that the user has contributed to)."""


@app.route('/t6', methods=['GET', 'POST'])
def collaborators():
    contributors = {}
    for user in git.user_names:
        counter = 0
        count = 0
        link = requests.get("https://api.github.com/users/" + user + "/repos?per_page=1000",
                            auth=('yangxiyucs', 'ab112113'))
        json_data = json.loads(link.text)
        results = nested_lookup(key='full_name', document=json_data)
        # date = nested_lookup(key='updated_at', document=json_data)
        # print(date)
        # for r in results:
        #     if (str(date).find('2018') != -1):
        #         contributor = requests.get("https://api.github.com/repos/" + r + "/contributors",
        #                                    auth=('yangxiyucs', 'ab112113'))
        #         data = json.loads(contributor.text)
        #         counter += len(data)
        for r in results:
            result = requests.get("https://api.github.com/repos/" + r + "/commits?since=2018-01-01",
                                  auth=('yangxiyucs', 'ab112113'))
            getresul = json.loads(result.text)

            if (len(getresul) != 0):
                count += 1
                contributor = requests.get("https://api.github.com/repos/" + r + "/contributors",
                                           auth=('yangxiyucs', 'ab112113'))
                if (len(contributor.text) != 0):
                    data = json.loads(contributor.text)
                    counter = counter + len(data)
                else:
                    pass

            else:
                continue
        contributors['{0}'.format(user)] = (counter - count)
    final = json.dumps({'contributors (2018)': contributors})
    git.add.append(final)
    print(final)
    return render_template('index.html', final=final)


''''EMAIL'''


@app.route('/email', methods=['GET', 'POST'])
def send_mail():
    for user in git.user_names:
        msg = Message('github', sender='176098868@qq.com', subject='github API',
                      recipients=git.user_names[user] + '@github.com')
        msg.html = git.add
        mail.send(msg)


if __name__ == "__main__":
    git = main()
    app.run(host='0.0.0.0', port=8080)
