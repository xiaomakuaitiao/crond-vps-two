from Request import Request
from bs4 import BeautifulSoup
import time

request = Request()
list_url = []
post_api = 'https://www.vpsman.net/index.php/action/import_news'


def articleFormat(soup):
    if soup.find(id='cb_post_title_url'):
        title = soup.find(id='cb_post_title_url').contents[1].text
    else:
        title = soup.find(attrs={'class','postTitle'}).next.next.text.replace('\n','')
    
    if soup.find('span',id="post-date"):
        create_time = soup.find('span',id="post-date").text
    if soup.find('div',attrs={'class','custom-post-message-bottom'}):
        create_time = soup.find('div',attrs={'class','custom-post-message-bottom'}).contents[0].text
    
   
    body = soup.find('div',id="cnblogs_post_body")
    try:
        for item in body.find_all('img'):
            item.attrs['referrerpolicy'] = 'no-referrer'
    except:
        pass

    try:
        for item in body.find_all('a'):
            if item == '':
                continue

            item.attrs['rel'] = 'noopener noreferrer nofollow'
            item.attrs['target'] = '_blank'
            
    except:
        pass
    return {'title':title, 'content': str(body), 'date': create_time}

def article():
    global list_url, post_api
    for url in list_url:
        response = request.request(url)
        
        if response == False:
            continue
        
        soup = BeautifulSoup(response,'html.parser')
        try:
            data = articleFormat(soup)
            data['category'] = '编程语言'
            request.requestPost(wordpress_api=post_api,data=data)
            request.logger.info('POST SUCCESS,title:{}'.format(data['title']))
        except Exception as e:
            request.logger.error('article format error,{}'.format(e))
            continue
        finally:
            response = ''
            soup = ''


def articleList(url):
    global list_url
   
    response = request.request(url)
    if response == False:
        return False
    
    soup = BeautifulSoup(response,'html.parser')

    links = soup.find_all('a',attrs={'class','post-item-title'})
    list_url = [item.attrs['href'] for item in links]
    

def main():
    url = 'https://www.cnblogs.com/'
    articleList(url)
    article()

main()
request.logger.info('cnblogs Success all')

