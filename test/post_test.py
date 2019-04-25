# -*- coding: utf-8 -*-
import requests, json, os

# main
if __name__ == "__main__":
    url = 'http://127.0.0.1:5000'
    d_path = '../tmp/'

    f_list = [f for f in os.listdir(d_path)]
    for f_name in f_list:
        files = {'FILE': (f_name, open('%s%s'%(d_path, f_name), 'rb'))}
        print(files)
        response = requests.post(url+'/predict', files=files)
        print(response.status_code)
        print(json.loads(response.content))
