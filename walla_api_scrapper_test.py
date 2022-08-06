import requests
from time import sleep


USERS_FILE            = 'users.txt'
USERS_WITH_SOLD_ITEMS = 'users_with_sold_items.txt'
N_LOAD_PAGES = 250 #PAGE= approx 20 prods

def make_req(url):
    r = requests.get(url)
    return r.json()

def append_to_file(user_ids, file):
    
    for id in user_ids:
        with open(file, 'a+') as f:
            f.write(f'{id}\n')
            # f.write(id)

def get_ids_from_file(file):
    with open(file, 'r+') as lines:
        for line in lines:
            yield line

def get_users_with_sold_items():

    users_id = get_ids_from_file(USERS_FILE)

    for id in users_id:
        try:
            # url = f'https://api.wallapop.com/api/v3/users/{id}/stats'
            # r = make_req(url)

            id = id.replace('\n', '')

            r = requests.get(f'https://api.wallapop.com/api/v3/users/{id}/stats').json()
            sold_number = get_solds(r)

            print(f'{id}-{sold_number}')

            if sold_number > 2:
                yield f'{id}-{sold_number}'

        except Exception as e:
            print(e)
            print(f'https://api.wallapop.com/api/v3/users/{id}/stats')


def get_solds(r):
    
    for item in r['counters']:
        if item['type'] == 'sells':
            return item['value']

def get_users_from_home_serps():
    
    # variables used in url
    start       = 320
    items_count = 0

    # with open(USERS_FILE, 'r') as f:
    #     for l in f:
    #         print(l)

    for i in range(N_LOAD_PAGES):
        start       += 40
        items_count += 40
        url = f'https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.41956&start={start}&user_region=Comunidad de Madrid&user_city=Madrid&search_id=8ebdab8a-2710-43e9-8192-f2b44d573193&country_code=ES&items_count={items_count}&density_type=20&filters_source=search_box&order_by=closest&step=0&longitude=-3.69196'

        r = make_req(url)
        sleep(3)

        #append user id's to txt file
        user_ids= []
        r_objects_list= r['search_objects']
        for object in r_objects_list:
            user_id= object['user']['id']
            print(user_id)
            user_ids.append(user_id)

        append_to_file(set(user_ids), USERS_FILE)
        
        print(f'\nIteration {i} of {n}')


def run():

    # write to users.txt the users id from walla serps
    # get_users_from_home_serps()

    #from those users, check if they have sold products, if they do, append those ids to users_with_sells.txt
    ids = get_users_with_sold_items()
    append_to_file(ids, USERS_WITH_SOLD_ITEMS)


if __name__ == '__main__':
    run()