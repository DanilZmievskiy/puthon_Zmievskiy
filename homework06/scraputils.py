import requests
from bs4 import BeautifulSoup



def extract_news(soup):
    """ Extract news from a given web page """
    titles = soup.find_all("a", attrs={"class": "storylink"})
    titles_list = [title.text for title in titles]
    links_list = [BeautifulSoup(str(title), features='html5lib').a['href'] for title in titles]
    subtext = soup.find_all("td", attrs={"class": "subtext"})
    subtext = [info.text.splitlines()[1].split(' ') for info in subtext]
    authors_list = [author[3] for author in subtext]
    points_list = [point[0] for point in subtext]
    comments = [comment[15] for comment in subtext]
    comments_list = []
    for comment in comments:
        if comment == 'discuss':
            comments_list.append(0)
        else:
            num = comment.replace(u'\xa0', u' ')
            comments_list.append(num)
    news_list = []
    for num in range(30):
        news_list.append(dict.fromkeys(['author', 'comments', 'points', 'title', 'url']))
    y = 0
    for d in news_list:
        d['author'] = authors_list[y]
        d['comments'] = comments_list[y]
        d['points'] = points_list[y]
        d['title'] = titles_list[y]
        d['url'] = links_list[y]
        y += 1
    return news_list


def extract_next_page(soup):
    """ Extract next page URL """
    next_page = soup.find_all("a", attrs={"class": "morelink"})
    next_page = BeautifulSoup(str(next_page), features='html5lib').a['href']
    return next_page


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
