# 1. ALL IMPT Updates on COVID Related stuff (Updates to Measures) (Uses API)
    # done

# 2. scrapes MOH Press Releases for Differentiated measures etc, more impt/minute stuff (parse XML)
    # https://www.moh.gov.sg/feeds/news-highlights (parse XML) - ALL Press Updates in the past month, their titles and links


# 3. scrapes gov.sg press releases for latest press releases on the following topics (headless selenium)
    # https://www.sgpc.gov.sg/
    # - MSE - They order businesses to close down when breaching measures, issue advisories on COVID
    # - STB - Tourism Industry related news 
    # - MTI - 


# 4. scrapes MOH Press Releases for current state (headless selenium)
    # https://www.moh.gov.sg/covid-19-phase-advisory - Current Phase Updates summarised
    # https://www.moh.gov.sg/covid-19 - Similar to the above

import requests
import os
import pandas as pd
# import PyPDF2

# save CSV
directory = os.path.dirname(os.path.realpath(__file__))
DATA_FILEPATH = os.path.join(directory, 'GOV_SG_API_SCRAPED_L50Rows.csv')

def writeScrapedRow(rowDict):
    scrapeList.append(rowDict)
    pd.DataFrame(scrapeList).to_csv(DATA_FILEPATH, index=False)

TOPIC_GOV_SG_API = 'Health'
NUM_ROWS_GOV_SG_API = str(50)
GOV_SG_API = 'https://www.gov.sg/api/v1/search?fq=contenttype_s:[*%20TO%20*]&fq=isfeatured_b:false&fq=primarytopic_s:%22{}%22&q=*:*&sort=publish_date_tdt%20desc&start=0&rows={}'.format(TOPIC_GOV_SG_API, NUM_ROWS_GOV_SG_API)

headers = {"accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "connection": "keep-alive",
    #"cookie": "_gcl_au=1.1.1590965881.1629875587; _ga=GA1.1.1281913755.1629875588; BIGipServerPOOL_T01699AENW007_80=!RRaPXSVqcp7JPmK2y3uy1ZSmqkptIK1MPWyq0SlDFJIQgxRRsgqdf6XUEuxJVpeoYIp2kRG+2abm7Io=; BIGipServerPOOL_T01699AENW008_80=!85WJrW9y65os52y2y3uy1ZSmqkptIKl569Y42Q7comc/a5jhd+7kOhrbLjz3xjxZ5hl7ZybdZ7gLfO4j844sEmEC+NBEVdql/E0aGEI=; _gid=GA1.1.53318824.1630161450; AMCVS_DF38E5285913269B0A495E5A%40AdobeOrg=1; AMCV_DF38E5285913269B0A495E5A%40AdobeOrg=1075005958%7CMCIDTS%7C18868%7CMCMID%7C83649643605679938043731086567568432525%7CMCAAMLH-1630766250%7C3%7CMCAAMB-1630766250%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1630168650s%7CNONE%7CvVersion%7C4.4.1; ASP.NET_SessionId=l2kygwiqrlevugxelj04ksaa; ARRAffinity=0ac9bce649c45e7967e35a9af818b7ca2e33342c80af9690acae9cd95bdb1278; SC_ANALYTICS_GLOBAL_COOKIE=755da20b05e5457f9b691533252f129b|True; _sp_ses.8ca1=*; _sp_id.8ca1=f419c00c-fe3b-45ed-b984-2f9eee3085b0.1629875589.3.1630166281.1630162507.db92c051-f2b0-4977-ba94-b6bf7bccbc29", 
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "referer": "https://www/gov.sg/{}".format(TOPIC_GOV_SG_API.lower()),
    "host": "www.gov.sg",
    "User-Agent" :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',}

def gov_sg_api_scrape():
    print(GOV_SG_API)
    try: response = requests.get(GOV_SG_API, headers = headers, timeout = 15)
    except requests.exceptions.Timeout: return

    if response.status_code != 200:
        print(response.status_code)
        return
    # print(response.text)
    try :
        data = response.json()
    except ValueError:
        print('ValueError')
        return
    try: testRun = data['response']
    except: 
        print('json issue')
        return

    for article in data['response']['docs']:

        imgUrl = "www.gov.sg/" + article['imageurl_s']
        minutesToRead = article['minuteread_s']

        articleUrl =  "www.gov.sg/" + article['pageurl_s']
        articleTitle = article['title_t']
        articleDescription = article['short_description_t']
        articleID = article['itemid_s']
        articleMainText = article['bodytext_t']

        articleSummarized = meaningCloudSummarizer(articleMainText)

        datePublished = article['publishdate_s']

        print(f'Title : {articleTitle}')
        print(f'Description : {articleDescription}')
        print(f'Main Text: {articleMainText}')
        print(f'Time to read : {minutesToRead} mins')
        print(f'URL : {articleUrl}')
        print(f'Published on : {datePublished}')
        print()
        print(f'Summarized Text : {articleSummarized}')
        print()

        try: writeScrapedRow({'articleTitle' : articleTitle, 'articleDescription' : articleDescription, 'articleSummarized': articleSummarized, 'articleBodyText': articleMainText, 'articleUrl' : articleUrl, 'imgUrl' : imgUrl, 'articleID' : articleID, 'datePublished' : datePublished})
        except: pass

    print(f'Scraped from {datePublished} till today')

def pdfToText():
    FILE_PATH = 'cinemasadvisory2.pdf'

    with open(FILE_PATH, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        page = reader.getPage(0)
        print(page.extractText())

# def smmrize(text):
#     print(text)
#     smmrizeHeader = {"Expect" : ""}
#     data = {"SM_API_KEY" : "<apikey>", "SM_API_INPUT" : text, "SM_LENGTH" : 7}
#     try: response = requests.get('https://api.smmry.com', data = data, headers = smmrizeHeader, timeout = 15)
#     except: 
#         print('fail')
#         return
#     print(response.text)


# limited to 20000 requests a month, $0.01 aft that
def meaningCloudSummarizer(text):
    # print(f'Original text: {text}.')
    numSentences = text.count('.')
    print(f'Number of Sentences initially: {numSentences}')

    url = "https://meaningcloud-summarization-v1.p.rapidapi.com/summarization-1.0"
    querystring = {"sentences":"10","txt":text}
    smmrizeHeaders = {
        'accept': "application/json",
        'x-rapidapi-host': "meaningcloud-summarization-v1.p.rapidapi.com",
        'x-rapidapi-key': "e47d8fec9emsh8c42a8523023567p192d84jsn81b8bd5f5ec3"
        }

    try: response = requests.request("GET", url, headers=smmrizeHeaders, params=querystring)
    except requests.exceptions.Timeout: return

    if response.status_code != 200:
        print(response.status_code)
        return
    try: summaryJSON = response.json()
    except ValueError:
        print(response.text)
        return
    try: summarizedText = summaryJSON["summary"]
    except:
        if response.text.find('"summary"') == -1: return
        summarizedText = response.text[response.text.find('"summary"') + len("summary") : -2]
        pass
    print(response.text)
    return summarizedText.replace('[...] ', '')


if __name__ == '__main__':
    # scrapeList = []
    # gov_sg_api_scrape()
    # smmrize("Additional measures for travellers from higher risk countries Main Text: Over the past week, several countries continue to experience a resurgence of COVID-19 cases, while new virus variants have emerged in Singapore. The number of locally-transmitted case has also continued to increase. Additional border measures will be implemented to curb the COVID-19 infections in Singapore decisively. Extending consecutive travel history from 14 to 21 days From 7 May 2021, 11.59pm, prevailing border measures that apply to incoming travellers will be determined based on their recent travel history in the past consecutive 21 days. This is an extension of the existing assessed travel history period of 14 days. 1 Increasing SHN duration from 14 to 21 days The following changes to the SHN duration will come into effect from 7 May 2021, 11.59pm onwards: All travellers with recent travel history to higher risk countries/regions will be required to serve a 21-day Stay Home Notice (SHN) at dedicated facilities. Travellers who are currently serving a 14-day SHN and have yet to complete their SHN by 7 May 2021, 11.59pm will be required to serve an additional 7 days at their current SHN location. All travellers serving their 21-day SHN will undergo the COVID-19 Polymerase Chain Reaction (PCR) tests on-arrival, on Day 14 of their SHN, and another test before the end of their 21-day SHN period. Travellers who have stayed in Fiji and Vietnam in the past consecutive 21 days will be subjected to a 21-day SHN at dedicated facilities, with the option to serve the last 7 days at their place of residence. Those who have yet to complete their current 14-day SHN by 7 May 2021, 11.59pm will be allowed to complete it at their current SHN location, and request to serve their additional 7 days at their place of residence. Travellers from the UK, South Africa, Bangladesh, India, Nepal, Pakistan, and Sri Lanka who are currently required to serve a 21-day SHN will be required to serve the full duration of the SHN at dedicated facilities. Travellers who have yet to complete their 21-day SHN by 7 May 2021, 11.59pm, will have to complete their 21-day SHN at their current SHN location. For more information, click here for MOH's press release. This excludes bilaterally negotiated travel lanes (e.g. Air Travel Bubble, Reciprocal Green Lane).")
    # meaningCloudSummarizer("Over the past week, several countries continue to experience a resurgence of COVID-19 cases, while new virus variants have emerged in Singapore. The number of locally-transmitted case has also continued to increase. Additional border measures will be implemented to curb the COVID-19 infections in Singapore decisively. Extending consecutive travel history from 14 to 21 days From 7 May 2021, 11.59pm, prevailing border measures that apply to incoming travellers will be determined based on their recent travel history in the past consecutive 21 days. This is an extension of the existing assessed travel history period of 14 days. 1 Increasing SHN duration from 14 to 21 days The following changes to the SHN duration will come into effect from 7 May 2021, 11.59pm onwards: All travellers with recent travel history to higher risk countries/regions will be required to serve a 21-day Stay Home Notice (SHN) at dedicated facilities. Travellers who are currently serving a 14-day SHN and have yet to complete their SHN by 7 May 2021, 11.59pm will be required to serve an additional 7 days at their current SHN location. All travellers serving their 21-day SHN will undergo the COVID-19 Polymerase Chain Reaction (PCR) tests on-arrival, on Day 14 of their SHN, and another test before the end of their 21-day SHN period. Travellers who have stayed in Fiji and Vietnam in the past consecutive 21 days will be subjected to a 21-day SHN at dedicated facilities, with the option to serve the last 7 days at their place of residence. Those who have yet to complete their current 14-day SHN by 7 May 2021, 11.59pm will be allowed to complete it at their current SHN location, and request to serve their additional 7 days at their place of residence. Travellers from the UK, South Africa, Bangladesh, India, Nepal, Pakistan, and Sri Lanka who are currently required to serve a 21-day SHN will be required to serve the full duration of the SHN at dedicated facilities. Travellers who have yet to complete their 21-day SHN by 7 May 2021, 11.59pm, will have to complete their 21-day SHN at their current SHN location. For more information, click here for MOH's press release. This excludes bilaterally negotiated travel lanes (e.g. Air Travel Bubble, Reciprocal Green Lane).")

    #response = requests.get("https://www.sgpc.gov.sg/?agency=MOM")
    response = requests.get("https://www.sgpc.gov.sg/media_releases/mom/press_release/P-20210607-1")
    print(response.text)







    
