# 3. scrapes gov.sg press releases for latest press releases on the following topics (parse http)
# https://www.sgpc.gov.sg/
# - MSE - They order businesses to close down when breaching measures, issue advisories on COVID
# - STB - Tourism Industry related news
# - MTI -


# 4. scrapes MOH Press Releases for current state (parse http)
# https://www.moh.gov.sg/covid-19-phase-advisory - Current Phase Updates summarised
# https://www.moh.gov.sg/covid-19 - Similar to the above

import requests
import os
import feedparser
import lxml.html as lh
from flask_apscheduler import APScheduler
from LocusDev import db
from models import db, Article, EventType
import time

scheduler = APScheduler()

# @scheduler.task("interval", id="wrapper", hours=4, misfire_grace_time=900)
@scheduler.task("cron", id="wrapper", hour='9', minute='09')
def wrapperTask():
    parseMOHFeed()
    time.sleep(5)
    gov_sg_api_scrape()
    time.sleep(5)
    checkTags()
    time.sleep(2)
    return

def parseMOHFeed():
    NewsFeed = feedparser.parse("https://www.moh.gov.sg/feeds/news-highlights")
    outputList = []
    for article in NewsFeed.entries:
        if article.title.lower().strip().startswith('update on local covid-19 situation'):
            # ddict = {}
            text = article.description[ article.description.lower().find('summary') : article.description.lower().find('<strong>', article.description.lower().find('summary')) ]
            text = lh.fromstring(text).text_content().replace('\xa0', ' ').replace('·', '')
            if text.startswith('Summary'):
                text = text[len("Summary of local situation"):].strip()

            checker = Article.query.filter_by(articleId=article.link).first()
            if checker is not None: break

            print(f'DatePublished gov_sg_aparseMOHFeedpi_scrape : {article.published}')

            article = Article(articleId=article.link, # link serves as the id of the article
                          title=article.title,
                          bodyText=text,
                          datePublished=article.published,
                          description="")
            db.session.add(article)
            db.session.commit()
    return outputList

# Tags:
# Health
# COVID-19
# Social and Community
# POFMA
# Environment
# Economy and Finance
# not to include : 'Others'
def gov_sg_api_scrape():
    NUM_ROWS_GOV_SG_API = str(50)
    GOV_SG_API = "https://www.gov.sg/api/v1/search?fq=contenttype_s:[*%20TO%20*]&fq=isfeatured_b:false&fq=primarytopic_s:[*%20TO%20*]%20OR%20secondarytopic_sm:[*%20TO%20*]&sort=publish_date_tdt%20desc&start=0&rows={}".format(NUM_ROWS_GOV_SG_API)

    headers = {"accept": "application/json, text/plain, */*",
               "accept-language": "en-US,en;q=0.9",
               "accept-encoding": "gzip, deflate, br",
               "connection": "keep-alive",
               # "cookie": "_gcl_au=1.1.1590965881.1629875587; _ga=GA1.1.1281913755.1629875588; BIGipServerPOOL_T01699AENW007_80=!RRaPXSVqcp7JPmK2y3uy1ZSmqkptIK1MPWyq0SlDFJIQgxRRsgqdf6XUEuxJVpeoYIp2kRG+2abm7Io=; BIGipServerPOOL_T01699AENW008_80=!85WJrW9y65os52y2y3uy1ZSmqkptIKl569Y42Q7comc/a5jhd+7kOhrbLjz3xjxZ5hl7ZybdZ7gLfO4j844sEmEC+NBEVdql/E0aGEI=; _gid=GA1.1.53318824.1630161450; AMCVS_DF38E5285913269B0A495E5A%40AdobeOrg=1; AMCV_DF38E5285913269B0A495E5A%40AdobeOrg=1075005958%7CMCIDTS%7C18868%7CMCMID%7C83649643605679938043731086567568432525%7CMCAAMLH-1630766250%7C3%7CMCAAMB-1630766250%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1630168650s%7CNONE%7CvVersion%7C4.4.1; ASP.NET_SessionId=l2kygwiqrlevugxelj04ksaa; ARRAffinity=0ac9bce649c45e7967e35a9af818b7ca2e33342c80af9690acae9cd95bdb1278; SC_ANALYTICS_GLOBAL_COOKIE=755da20b05e5457f9b691533252f129b|True; _sp_ses.8ca1=*; _sp_id.8ca1=f419c00c-fe3b-45ed-b984-2f9eee3085b0.1629875589.3.1630166281.1630162507.db92c051-f2b0-4977-ba94-b6bf7bccbc29",
               "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
               "sec-ch-ua-mobile": "?0",
               "sec-fetch-dest": "empty",
               "sec-fetch-mode": "cors",
               "sec-fetch-site": "same-origin",
               "referer": "https://www/gov.sg/health",
               "host": "www.gov.sg",
               "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', }
    try:
        response = requests.get(GOV_SG_API, headers=headers, timeout=15)
    except requests.exceptions.Timeout:
        return
    if response.status_code != 200:
        print(response.status_code)
        return
    try:
        data = response.json()
    except ValueError:
        print('ValueError')
        return
    try:
        testRun = data['response']
    except:
        print('Json Issue')
        return
    print("Total Num responses:", data['response']['docs'])
    outputList = []
    for article in data['response']['docs']:
        ddict = {}
        imgUrl = "www.gov.sg/" + article['imageurl_s']
        minutesToRead = article['minuteread_s']
        articleUrl = "www.gov.sg/" + article['pageurl_s']
        articleTitle = article['title_t']
        try: articleDescription = article['short_description_t']
        except: articleDescription = ""
        articleID = article['itemid_s']
        articleMainText = article['bodytext_t']

        print(f'DatePublished gov_sg_api_scrape : {datePublished}')

        # nCount = find_nth(articleMainText, '. ', articleMainText.count('. ') * 0.3)
        # articleSummarized = meaningCloudSummarizer(articleMainText)

        datePublished = article['publishdate_s']

        checker = Article.query.filter_by(articleId=articleUrl).first()
        if checker is not None: break

        article = Article(articleId= articleUrl,
                          title=articleTitle,
                          bodyText=articleMainText,
                          datePublished=datePublished,
                          description=articleDescription)
        db.session.add(article)
        db.session.commit()

        # ddict['imgUrl'] = imgUrl
        # ddict['minutesToRead'] = minutesToRead
        # ddict['articleSummarized'] = articleSummarized
        # ddict['articleSummarized'] = articleMainText[:nCount]
    return outputList

def checkTags():
    # Attractions: Accordion 3
    # Country and Recreational Clubs: Accordion 6
    # Enterprises in Finance Sector: Accordion 13
    # Funeral Events: Accordion 15
    # F&B: Accordion 16
    # Hotels: Accordion 20
    # Solemnisation and Reception: Accordion 22
    # MICE Events : Accordion 26
    # Nightlife: Accordion 27
    # Property Show Galleries: Accordion 31
    # Public Entertainment: Accordion 32
    # Religious organisations : Accordion 33
    # Sports Sector Enterprises: Accordion 36
    # Tours: Accordion 38
    try:
        response = requests.get('https://www.gobusiness.gov.sg/safemanagement/sector/', timeout=15)
    except requests.exceptions.Timeout:
        return
    if response.status_code != 200:
        print(response.status_code)
        return
    root = lh.fromstring(response.text)
    # TODO: find len 'jekyllcodex_accordion', replace with 42
    SectorList = ['Attractions', 'Country and recreation clubs', 'Finance', 'Funeral events', 'F&B', 'Hotels',
                  'Marriage solemnisations and wedding receptions', 'MICE events', 'Nightlife Establishments (Pivoted)',
                  'Property show galleries', 'Public entertainment', 'Religious organisations',
                  'Sports sector enterprises, sports education, and premises with sports facilities', 'Tours']
    for num in range(1, 42):
        sectorContent = root.xpath(f'//*[@id="main-content"]/section[3]/div/div/div[2]/div/div/div/ul/li[{num}]')
        text = sectorContent[0].text_content()
        sectorName = text[:text.find('\n')]
        if sectorName in SectorList:
            # print(sectorName.strip())
            text = text[len(sectorName):]
            check = 0
            lastUpdatedStr = ""
            while check != -1:
                lastUpdatedStr += text[text.find('[', check): text.find(']', check) + 1]
                text = text[text.find(']', check):]
                check = text.find('[')
            checker = EventType.query.filter_by(eventTypeName=sectorName.strip()).first()
            if checker is not None and checker.currString != lastUpdatedStr.strip():
                checker.currString = lastUpdatedStr.strip()
                # Append to a Post request list

                db.session.commit()
            if checker is None:
                newEventType = EventType(sectorName, lastUpdatedStr.strip())
                db.session.add(newEventType)
                db.session.commit()
    # Make the post request
    req = requests.post("")

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start

# limited to 20000 requests a month, $0.01 aft that
def meaningCloudSummarizer(text):
    # print(f'Original text: {text}.')
    numSentences = text.count('.')
    print(f'Number of Sentences initially: {numSentences}')
    url = "https://meaningcloud-summarization-v1.p.rapidapi.com/summarization-1.0"
    querystring = {"sentences": "10", "txt": text}
    smmrizeHeaders = {
        'accept': "application/json",
        'x-rapidapi-host': "meaningcloud-summarization-v1.p.rapidapi.com",
        'x-rapidapi-key': os.environ.get('SMMRIZE_API_KEY')
    }
    try:
        response = requests.request("GET", url, headers=smmrizeHeaders, params=querystring, timeout=15)
    except requests.exceptions.Timeout:
        return
    if response.status_code != 200:
        print(response.status_code)
        return
    try:
        summaryJSON = response.json()
    except ValueError:
        print(response.text)
        return
    try:
        summarizedText = summaryJSON["summary"]
    except:
        if response.text.find('"summary"') == -1: return
        summarizedText = response.text[response.text.find('"summary"') + len("summary"): -2]
        pass
    # print(response.text)
    return summarizedText.replace('[...] ', '')

