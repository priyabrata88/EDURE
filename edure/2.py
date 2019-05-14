import requests
from bs4 import BeautifulSoup
import MySQLdb

def get_event_url():
    page = requests.get("http://www.spe.org/events/calendar/")
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
    allevents = soup.select('table.events tbody tr')
    #get all events
    url = "http://www.spe.org"
    for tr in allevents:
        tds = tr.findAll('td')
        #get tag, date, venue,
        tag = tds[2].get_text()
        tags = tag.split()
        tag = '#'+tags[0]
        date = tr.find('span').get_text()
        venue =tds[4].find('span').get_text()
        #get overview, title
        overview  = ''
        title = ''
        price = ''
        #page has url
        if(tds[1].find('a')):
            title = tds[1].find('a').get_text()
            eventlink = tds[1].find('a').get('href')
            if(eventlink.startswith('http') == False):
                eventlink = url + eventlink
            #event detail page
            if(tag.startswith('#Symp') == False):
                eventpage = requests.get(eventlink)
                newsoup = BeautifulSoup(eventpage.content, 'html.parser')
                article = newsoup.find('article')
                if article:
                    if(article.find('p')):
                        overview = article.find('p').get_text()
                    # if(article.find('div', {'class':'spe-richtext-content'})):
                    #         overview = article.find('div', {'class':'spe-richtext-content'}).find('p').get_text()

        #page has not url
        else:
            title = tds[1].find('span').get_text()

        str = u'\u2014'
        tempvenue = venue.split(str)
        venue = tempvenue[0]
        print title,venue,date,overview,tag
        # #save them into db
        query = "INSERT INTO edure_event (title,venue,date,events_overview,tags,price) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title.strip().encode('ascii','ignore'),venue.strip().encode('ascii','ignore'),date.strip().encode('ascii','ignore'),overview.strip().encode('ascii','ignore'), tag.strip().encode('ascii','ignore'),price))
        connection.commit()

    connection.close()
    return

print (get_event_url())
