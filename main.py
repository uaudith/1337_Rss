import requests
from bs4 import BeautifulSoup as bs


def get_new_results(uploader: str):
    """
    ex: if url is 'https://1337x.to/user/goki/' then uploader field is 'goki'
    use the generator with next() untill  the func is_already_exist() returns True
    :param uploader: uploader name in the 1337x.to
    :return: A generator object.
    """
    url = f'https://1337x.to/user/{uploader}/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    resultset = soup.find_all('tr')[1:]
    for item in resultset:
        data = [i for i in item.children]
        url = 'https://1337x.to'
        url += data[1].contents[1].get('href')
        seeds = data[3].contents[0]
        leeches = data[5].contents[0]
        size = data[7].contents[0]
        age = data[9].contents[0]
        yield {'url': url,
               'seeds': seeds,
               'leeches': leeches,
               'size': size,
               'age': age
               }


def keep_a_record(uploader: str, record):
    """
    :param uploader: uploader name mentioned in the url to the profile of the uploader
    :param record: this is used to pevent posting same torrent again and again.
     It is adviced to use the url property as the record
    :return: None
    """
    with open(uploader, 'w') as file:
        file.write(record)


def is_already_exist(uploader: str, record) -> bool:
    """
    :param uploader: uploader name mentioned in the url to the profile of the uploader
    :param record: this is used to pevent posting same torrent again and again.
     It is adviced to use the url property as the record
    :return: True when the last kept record is equal to the current record.
     False if doesnt match. False means search result is new.
    :raise: if the file not found
    """
    with open(uploader, 'r') as file:
        try:
            if file.readline() == record:
                return True
            else:
                return False
        except FileNotFoundError:
            return False
