import requests
from bs4 import BeautifulSoup
import MySQLdb

def get_event_url(url, n, connection, cursor):

    page= requests.get(url)
    if(page.status_code != 200):
        return
    #page
    soup = BeautifulSoup(page.content, 'html.parser')
    #all events in page
    allevents = soup.select('tr')
    #every event
    for tr in allevents:

        title = ''
        venue = ''
        date = ''
        tags = []
        overview = ''
        price = ''

        tds = tr.findAll('td')
        #get URL link to event
        if len(tds) <2:
           continue
        eventlink = tds[1].find('a').get('href')

        #get tags have no link
        if tds[4].findAll('span'):
            for tag in tds[4].findAll('span'):
                tags.append('#'+tag.get_text().encode('ascii','ignore'))
        #get tags have link
        if tds[4].findAll('a'):
            for tag in tds[4].findAll('a'):
                tags.append('#'+tag.get_text().encode('ascii','ignore'))
        #detail event page
        eventpage = requests.get(eventlink)
        newsoup = BeautifulSoup(eventpage.content, 'html.parser')
        cont = newsoup.find('section')

        #get title
        title = cont.find('h1').get_text().encode('ascii','ignore')
        #get date
        date = cont.find('ul').find('span').get_text().encode('ascii','ignore')
        #get venue
        venuetemp = cont.findAll('li')
        if len(venuetemp)>2:
            venue = venuetemp[2].get_text().encode('ascii','ignore')
        else:
            venue = venuetemp[1].get_text().encode('ascii','ignore')
        #get overview
        overview = newsoup.find('div', {'id': 'content'}).find('section', {'class': 'box'}).find('p').get_text().encode('ascii','ignore')
        print title,venue,date,overview,tags
        #save them in db
        query = "INSERT INTO edure_event (title,venue,date,price,events_overview,tags) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title.strip(),venue.strip(),date.strip(),price,overview.strip(), ''.join(tags)))
        connection.commit()
    return


def get_event_all():

    #create connection with MySQLdb
    connection = MySQLdb.connect(host= "localhost",
                  user="edure",
                  passwd="edure",
                  db="edure")
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE edure_event")
    connection.commit()
    #pages
    pages = range(1, 7)
    original_url = 'https://10times.com/ajax?for=scroll&path=/education-training&ajax=1'
    #every page
    for page in pages:
        url = original_url+'&page=%s&popular=1&offSet=40' % page
        get_event_url(url,page,connection,cursor)
    connection.close()
    return True

get_event_all()
