import requests
import json

def run_test():
    
    # test get
    _test_get = requests.get('http://127.0.0.1:5000/pred')
    
    # print our json
    print(_test_get.json())



    # test post
    payload = {
                'experience_level': 'EX',
                'employment_type' : 'FT',
                'company_size': 'L',
                'role' : 'Artificial Intelligence Engineer',
                'residence' : 'US',
               # 'remote%' : '100'
    }

    r = requests.post('http://127.0.0.1:5000/pred', json=payload)

    print(r.json())



if __name__ == '__main__':

    # example tests
    run_test()
