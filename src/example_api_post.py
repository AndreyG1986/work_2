# import requests
#
# url_post = "https://httpbin.org/post" # используемый адрес для отправки запроса
#
# response = requests.post(url_post) # отправка POST-запроса
#
# print(response) # вывод объекта класса Response
# # Вывод:
# >> <Response [200]>
#
# print(response.status_code) # вывод статуса запроса, 200 означает, что всё хорошо
# # Вывод:
# >> 200
#
# print(response.text) # печать ответа в виде текста того, что вернул нам внешний сервис
# # Вывод:
# >> {
# >>   "args": {},
# >>   "data": "",
# >>   "files": {},
# >>   "form": {},
# >>   "headers": {
# >>     "Accept": "*/*",
# >>     "Accept-Encoding": "gzip, deflate",
# >>     "Content-Length": "0",
# >>     "Host": "httpbin.org",
# >>     "User-Agent": "python-requests/2.31.0",
# >>     "X-Amzn-Trace-Id": "Root=1-65893054-044490af734f11d751ff9f85"
# >>   },
# >>   "json": null,
# >>   "origin": "185.252.41.5",
# >>   "url": "https://httpbin.org/post"
# >> }
#
# print(response.json()) # печать ответа в виде json объекта того, что нам вернул внешний сервис
# # Вывод:
# >> {'args': {}, 'data': '', 'files': {}, 'form': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '0', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.31.0', 'X-Amzn-Trace-Id': 'Root=1-65893054-044490af734f11d751ff9f85'}, 'json': None, 'origin': '185.252.41.5', 'url': 'https://httpbin.org/post'}