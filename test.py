import requests
from flask import json
from nested_lookup import nested_lookup

# user_names = ['Danielo814','yangxiyucs']
# new_language = []
# git_language = {}
# for user in range(0, len(user_names)):
#     link = requests.get("https://api.github.com/users/" + user_names[user] + "/repos",
#                         auth=('yangxiyucs', 'ab112113'))
#     json_data = json.loads(link.text)
#     results = nested_lookup(key='full_name', document=json_data)
#
#     language_data = json.loads(link.text)
# # print(type(language_data))
# # print(type(link))
#
#     for i in range(0, len(results)):
#         link = requests.get("https://api.github.com/repos/" + results[i] + "/languages",
#                             auth=('yangxiyucs', 'ab112113'))
#         language_data = json.loads(link.text)
#         for l in range(0, len(language_data)):
#             # print(l)
#             new_language.append(list(language_data)[l])
#             # print(new_language)
#             # erase repeat language by set()
#     listnew = list(set(new_language))
#     git_language[user_names[user]] = listnew
#
#     print(len(listnew))
#     # print("git_language..." + json.dumps({user_names[user]:git_language}))
# final = json.dumps({'Language Used': git_language})
# print(final)
# --------------
# link = requests.get("https://api.github.com/repos/yangxiyucs/NewRepo/stats/commit_activity",
#                                 auth=('yangxiyucs', 'ab112113'))
# data = json.loads(link.text)
# for i in data:
#     print(type(i))

# ----------
# result = subprocess.check_output(["curl", "-H", "Accept: application/vnd.github.cloak-preview",
#                                   "https://api.github.com/search/commits?q=author:" + git.user_names[
#                                       i] + "&per_page=1000"], shell = False)
# url = "https://api.github.com/search/commits?q=author:yangxiyucs&per_page=1000"
# headers = {'Accept': 'application/vnd.github.cloak-preview'}
# result = requests.get(url, headers=headers, auth=('yangxiyucs', 'ab112113'))
# results = json.loads(result.text)
# print(results)

#-------------------t6
link = requests.get("https://api.github.com/users/yangxiyucs/repos?per_page=1000",
                    auth=('yangxiyucs', 'ab112113'))
json_data = json.loads(link.text)
results = nested_lookup(key='full_name', document=json_data)
print(results)
date = nested_lookup(key='updated_at', document=json_data)
print(date)

counter = 0
for r in results:
    if (str(date).find('2018') != -1):
        contributor = requests.get("https://api.github.com/repos/yangxiyucs/NewRepo/contributors",
                                   auth=('yangxiyucs', 'ab112113'))
        data = json.loads(contributor.text)
        counter += len(data)
print(counter)
