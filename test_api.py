import requests
import json

def run_test():
    
    # test get
    _test_get = requests.get('http://127.0.0.1:5000/pred')
    
    # print our json
    print(_test_get.json())


    print('\n\n\n\n')



    # test post
    payload = {
                'experience_level': 'EX',
                'employment_type' : 'FT',
                'company_size': 'L',
                'role' : 'Machine Learning Engineer',
                'residence' : 'US',
                'remote%' : '100'
    }

    r = requests.post('http://127.0.0.1:5000/pred', json=payload)

    print(r.json(), '\n\n\n')


if __name__ == '__main__':

    # example tests
    run_test()
