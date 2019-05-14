import requests
from bs4 import BeautifulSoup
import MySQLdb

def get_event_url():
    page = requests.get("https://www.britishcouncil.in/events")
    if(page.status_code != 200):
        return
    #create connection with MySQLdb
    connection = MySQLdb.connect(host= "localhost",
                  user="edure",
                   passwd="edure",
                  db="edure")
    cursor = connection.cursor()
    # cursor.execute("TRUNCATE TABLE edure_event")
    # connection.commit()
    #scrapping
    soup = BeautifulSoup(page.content, 'html.parser')
    allevents = soup.findAll('article')
    #get all events
    url = "https://www.britishcouncil.in"

    arc_n = 0
    for article in allevents:
        overview = ''
        title = ''
        venue = ''
        tags = []
        date = ''
        price = ''
        arc_n += 1
        #get tag
        if article.find('dd') != False:
            tag = article.find('dd').get_text()
            tags_text = tag.split(',')
            for tag in tags_text:
                tags.append('#'+tag.strip().encode())
        #get URL link
        eventlink = url + article.find('a').get('href')
        eventpage = requests.get(eventlink)
        newsoup = BeautifulSoup(eventpage.content, 'html.parser')
        #event 1
        if(arc_n == 1):
            overview = article.find('p').get_text().encode('ascii','ignore')
            venue = newsoup.findAll('dd')[1].get_text().encode('ascii','ignore')
            #event page
            events = newsoup.findAll('tr')
            ev_n = 0
            for event in events:
                ev_n += 1
                if(ev_n == 1):
                    continue
                title_field = event.findAll('td')

                if(len(title_field[0].findAll('p')) > 0 ):
                    title = title_field[0].find('p').get_text().encode('ascii','ignore')
                else:
                    title = title_field[0].get_text().encode('ascii','ignore')
                date = title_field[1].get_text().encode('ascii','ignore')
                price = title_field[3].get_text().encode('ascii','ignore')
                print title,venue,date,overview,tags,price
                save_data_to_db(connection,cursor,title,venue,date,overview,tags,price)
        #event 2
        if(arc_n == 2):
            overview = newsoup.find('p').get_text().encode('ascii','ignore')
            venue = newsoup.findAll('dd')[1].get_text().encode('ascii','ignore')
            #event page
            events = newsoup.findAll('tr')
            ev_n = 0
            for event in events:
                ev_n += 1
                if(ev_n == 1):
                    continue
                title_field = event.findAll('td')
                title = title_field[0].get_text().encode('ascii','ignore')
                date = title_field[1].get_text().encode('ascii','ignore')
                price = title_field[4].get_text().encode('ascii','ignore')
                if(price != 'Free'):
                    price = ''
                print title,venue,date,overview,tags,price
                save_data_to_db(connection,cursor,title,venue,date,overview,tags,price)
        #event 3
        if(arc_n == 3):
            overview = newsoup.find('p').get_text()
            venue = newsoup.findAll('p')[1].get_text()
            date = newsoup.find('strong').get_text()
            price = "INR 200"
            title = newsoup.find('h1').get_text()
            print title,venue,date,overview,tags,price
            save_data_to_db(connection,cursor,title,venue,date,overview,tags,price)
        # if(arc ==4):
        if(arc_n == 4):
            title = newsoup.find('h1').get_text().encode('ascii','ignore')
            section = newsoup.find('section')
            date_cont = section.findAll('dd')
            date = date_cont[0].get_text().encode('ascii','ignore')
            tempdate = date.split(',')
            date = tempdate[1]
            venue = newsoup.findAll('dd')[1].get_text().encode('ascii','ignore')
            body_text = section.find('div',{'class':'bc-body-text'})
            overview = body_text.findAll('p')[0].get_text().encode()
            print title,venue,date,overview,tags,price
            save_data_to_db(connection,cursor,title,venue,date,overview,tags,price)
        if(arc_n == 5):
            tags = []
            title = newsoup.find('h1').get_text().encode('ascii','ignore')
            section = newsoup.findAll('section')[0]
            date_cont = section.findAll('dd')
            date = date_cont[0].get_text().encode('ascii','ignore')
            tempdate = date.split(',')
            date = tempdate[1]
            venue = date_cont[1].get_text().encode('ascii','ignore')
            overview = section.find('div',{'class':'bc-body-text'}).get_text().encode('ascii','ignore')
            print title,venue,date,overview,tags,price
            save_data_to_db(connection,cursor,title,venue,date,overview,tags,price)
        if(arc_n == 6):
            title = newsoup.find('h1').get_text().encode('ascii','ignore')
            tag = article.find('dd').get_text()
            section = newsoup.findAll('section')[0]
            body_text = section.find('div',{'class':'bc-body-text'})
            overview = body_text.findAll('p')[0].get_text().encode('ascii','ignore')
            events = section.findAll('tr')

            ev_n = 0
            for event in events:
                ev_n += 1
                if(ev_n == 1):
                    continue
                title_field = event.findAll('td')
                date = title_field[0].get_text().encode('ascii','ignore')
                tempdate = date.split(',')
                date = tempdate[1]
                venue = title_field[1].get_text().encode('ascii','ignore')
                date = date + ' 2018 ' + title_field[2].get_text().encode('ascii','ignore')
                print title,venue,date,overview,tags,price
                save_data_to_db(connection,cursor,title,venue,date,overview,tags,price)

    connection.close()
    return
def save_data_to_db(connection,cursor,title,venue,date,overview,tags,price):
    query = "INSERT INTO edure_event (title,venue,date,events_overview,tags,price) VALUES (%s, %s, %s, %s, %s,%s)"
    cursor.execute(query, (title.strip(),venue.strip(),date.strip(),overview.strip(), ''.join(tags),price.strip()))
    connection.commit()
    return True
print (get_event_url())
