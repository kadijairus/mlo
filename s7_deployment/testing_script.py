import requests
response = requests.get('https://api.github.com')
print(response.status_code)

#response=requests.get("https://api.github.com/repos/SkafteNicki/dtu_mlops")
#print(response.json())

#response = requests.get(
#    'https://api.github.com/search/repositories',
#    params={'q': 'requests+language:python'},
#)

"""
response = requests.get('https://imgs.xkcd.com/comics/making_progress.png')
with open(r'img.png','wb') as f:
    f.write(response.content)
"""

pload = {'username':'Olivia','password':'123'}
response = requests.post('https://httpbin.org/post', data = pload)
print(response.json())