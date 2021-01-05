from Request import Request
from bs4 import BeautifulSoup
import time

request = Request()
list_url = []
cate = ''
post_api = 'https://www.vpsman.net/index.php/action/import_news'

def articleListUrl(get_url):
    global list_url, request
    response = request.request(url=get_url)
    if Request == False:
        exit()

    soup = BeautifulSoup(response,'html.parser')
    urls = soup.find_all('a',attrs={'class','tit'})
    list_url = [item.get('href') for item in urls]

def articleFormat(soup):
    title = soup.find('h1',attrs={'class','artical-title'}).string
    create_date = soup.find('a',attrs={'class','time fr'}).string
    body = soup.find('div',attrs={'class','editor-preview-side'})
    try:
        for item in body.find_all('img'):
            item.attrs['referrerpolicy'] = 'no-referrer'
    except:
        pass
    
    return {'title':title, 'content': str(body), 'date': create_date}


def article():
    global list_url, request, cate, post_api
    for url in list_url:
        response = request.request(url)
        if response == False:
            continue
        soup = BeautifulSoup(response,'html.parser')
        try:
            data = articleFormat(soup)
            data['category'] = cate
            request.requestPost(wordpress_api=post_api,data=data)
            request.logger.info('post Success,category:{},title:{}'.format(cate,data['title']))
        except Exception as e:
            request.logger.error('article format error,msg:{}'.format(e))
            continue
        finally:
            soup = ''
            response = ''
    
    list_url = []

def main():
    global cate, list_url, request
    cate = {
        '编程语言': 'https://blog.51cto.com/original/31',
        'Web技术': 'https://blog.51cto.com/original/30',
        '服务器': 'https://blog.51cto.com/original/27'
    }
    for key,item in cate.items():
        cate = key
        articleListUrl(item)
        if len(list_url) <= 0:
            request.logger.error('list url is empty!')
            continue
        article()
        request.logger.info('{} cate reptile Success!,sleep 5s'.format(key))
        time.sleep(5)

main()
request.logger.info('51cto Success')