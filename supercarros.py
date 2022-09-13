import requests
from bs4 import BeautifulSoup

url = 'https://www.supercarros.com'
path = '/carros/sedan/'

response = requests.get(url + path)

cars = []


def parse_table(row_data):
    new_list = []
    for row in row_data:
        cols = row.find_all('td')
        cols = [ele.text.strip().lower() for ele in cols]
        new_list.append([ele for ele in cols if ele])
    return new_list


if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    cars_list = soup.find('div', id="bigsearch-results-inner-results").find_all('li')

    for car in cars_list:
        title = car.find('div', class_="title1").get_text()
        year = car.find('div', class_="year").get_text()
        image = car.find('img', class_="real")['src']
        link = url + car.find('a')['href']

        data = {
            'title': title.strip(),
            'year': year.strip(),
            'thumbnail': image,
            'url': link,
            'specifications': [],
            'accessories': [],
            'images': [],
        }

        content = requests.get(link)
        if content.status_code == 200:
            full = BeautifulSoup(content.content, "html.parser")
            specs = full.find_all('div', class_="detail-ad-info-specs-block")
            transmission = specs[0].find_all('strong')[0].get_text()
            fuelType = specs[0].find_all('strong')[2].get_text()
            drivetrain = specs[0].find_all('strong')[1].get_text()
            exterior_color = specs[0].find_all('strong')[3].get_text()

            # images
            images = full.find('div', id="detail-ad-info-photos").find_all('a')
            for img in images:
                if img.has_key('href'):
                    data['images'].append(img['href'])

            # accessories
            if specs[5].find('ul'):
                accessories = specs[5].find('ul').find_all('li')
                accessories.pop()
                accessories.pop()
                for acc in accessories:
                    data['accessories'].append(acc.get_text())

            table_body = specs[4].find('table')
            rows = table_body.find_all('tr')
            table = parse_table(rows)
            # specifications
            for spec in table:
                data['specifications'].append({spec[0]: spec[1]})

                if len(spec) > 2:
                    data['specifications'].append({spec[2]: spec[3]})

        cars.append(data)

print(cars)
