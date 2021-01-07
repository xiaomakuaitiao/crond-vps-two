from Request import Request
from bs4 import BeautifulSoup
import time

url = 'https://www.lowendtalk.com/categories/offers'
request = Request()
list_url = []
post_api = 'https://www.vps136.com/index.php/action/import_news'


def articleList():
    global request, list_url, url
    response = request.request(url)
    if response == False:
        exit()
    
    soup = BeautifulSoup(response,'html.parser')
    urls = soup.find_all('div',attrs={'class','Title'})
    list_url = [item.find('a').get('href') for item in urls]
    

def articleFormat(soup):
    title = soup.find('h1').text
    create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    body = soup.find('div',attrs={'class','Message userContent'})
    try:
        for item in body.find_all('a'):
            if item == '':
                continue

            item.attrs['rel'] = 'noopener noreferrer nofollow'
            if item.has_key('data-cfemail') == True :
                item.extract()
    except:
        pass
    
    try:
        for item in body.find_all('img'):
            if item == '':
                continue
            item.attrs['referrerpolicy'] = 'no-referrer'
    except:
        pass

    return {'title':title, 'content': str(body), 'date': create_date}

def article():
    global request, list_url, post_api
    for url in list_url:
        response = request.request(url)
        if response == False:
            continue

        soup = BeautifulSoup(response,'html.parser')

        try:
            data = articleFormat(soup)
            data['category'] = 'VPS'
            request.requestPost(wordpress_api=post_api,data=data)
            request.logger.info('Post Success!,title:{}'.format(data['title']))
        except Exception as e:
            request.logger.error('article format is error,msg:{}'.format(e))
            continue
        finally:
            soup = ''
            response = ''
    
    list_url = []

def main():
    global list_url,request
    articleList()
    if len(list_url) <= 0:
        request.logger.error('list is empty')
        exit()
    article()
    request.logger.info('Reptile lowendtakl Success')

if __name__ == "__main__":
    try:
        main()
    except:
        pass