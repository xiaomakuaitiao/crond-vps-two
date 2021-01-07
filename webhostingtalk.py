from Request import Request
from bs4 import BeautifulSoup
import time

request = Request()
whtk_host = 'https://www.webhostingtalk.com/'
list_utl = []
post_api = 'https://www.vps136.com/index.php/action/import_news'
cate = ''

def articleList(url):
    global request, whtk_host, list_utl
    response = request.request(url)
    if response == False:
        exit()

    soup = BeautifulSoup(response,'html.parser')
    urls = soup.find_all('a',attrs={'class','title'})
    list_utl = [whtk_host + item.get('href') for item in urls]

def articleFormat(soup):
    title = soup.find('span',attrs={'class','threadtitle'}).next.text
    create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    content = soup.find('blockquote',attrs={'class','postcontent'})
    try:
        for item in content.find_all('a'):
            item.attrs['target'] = '_blank'
            item.attrs['rel'] = 'noopener noreferrer nofollow'
    except:
        pass

    try:
        for item in content.find_all('img'):
            item.attrs['referrerpolicy'] = 'no-referrer'
    except:
        pass
    return {'title':title, 'content': str(content), 'date': create_date}


def article():
    global list_utl, request, cate, post_api
    for url in list_utl:
        response = request.request(url)

        if response == False:
            continue
        
        soup = BeautifulSoup(response,'html.parser')
        try:
            data = articleFormat(soup)
            data['category'] = cate
            if data['title'] == '':
                request.logger.info('title is empty')
                continue

            request.requestPost(wordpress_api=post_api,data=data)
            request.logger.info('Post Success!,title:{}'.format(data['title']))
        except Exception as e:
            request.logger.error('article fromat error,msg:{}'.format(e))
            continue
        finally:
            soup = ''
            response = ''
    
    list_utl = []

def main():
    global list_utl, request, cate
    pages = {
        'VPS': 'https://www.webhostingtalk.com/forumdisplay.php?f=104',
        'Server': 'https://www.webhostingtalk.com/forumdisplay.php?f=36',
        'web-hosting': 'https://www.webhostingtalk.com/forumdisplay.php?f=4'
    }
    for key,item in pages.items():
        articleList(item)
        cate = key
        if len(list_utl) <= 0:
            request.logger.info('list url empty')
            exit()
        list_utl = list_utl[2:]
        article()
        request.logger.info('cate:{} is Success,time sleep 5s'.format(key))
        time.sleep(5)

    request.logger.info('webhostingtalk reptile Success!')

if __name__ == "__main__":
    try:
        main()
    except:
        pass