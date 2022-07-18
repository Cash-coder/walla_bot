import requests
from time import sleep

# variables used in url
start       = 320
items_count = 0


def make_req(url):
    r = requests.get(url)
    return r.json()

for _ in range(2):
    start       += 40
    items_count += 40
    url = f'https://api.wallapop.com/api/v3/general/search?user_province=Madrid&latitude=40.41956&start={start}&user_region=Comunidad de Madrid&user_city=Madrid&search_id=8ebdab8a-2710-43e9-8192-f2b44d573193&country_code=ES&items_count={items_count}&density_type=20&filters_source=search_box&order_by=closest&step=0&longitude=-3.69196'

    r = make_req(url)
    sleep(3)

    #print titles
    r_objects_list = r['search_objects']
    for object in r_objects_list:
        title = object['title']
        print(title)