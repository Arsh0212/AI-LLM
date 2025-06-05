import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from stocks import Database_Management





class Fetch_Data:

    def __init__(self):
        self.dm = Database_Management()
        self.path = "https://www.moneycontrol.com/news/"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})

    def get_article_from_link(self,link):
        print("Searching")
        try:
            news_articles_page = self.session.get(link, timeout=8)
            news_articles_page_html = BeautifulSoup(news_articles_page.text, 'html.parser')
            wrapper = news_articles_page_html.find("div", class_="page_wrapper")
            if not wrapper:
                return None

            title = wrapper.find("h1", class_="article_title").get_text(strip=True)
            paragraphs = wrapper.find("div", class_="content_wrapper").find_all("p")
            content = " ".join(p.get_text(strip=True) for p in paragraphs if p)
            try:
                self.dm.insert_data(title, content)
                print("Inserted", title)
            except:
                return
        except Exception as e:
            print(e)
        

    def extract_article_links(self,subcategory_url):

        """Scrapes links to news articles from a subcategory page."""
        article_links = []
        try:
            category_page = self.session.get(subcategory_url, timeout=8)
            category_page_html = BeautifulSoup(category_page.text, 'html.parser')
            li_items = category_page_html.find("ul", id="cagetory").find_all("li", class_="clearfix")
            for li in li_items:
                try:
                    href = li.find("h2").find("a")["href"]
                    article_links.append(href)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        return article_links

    def has_exact_class(self,tag):
        return tag.name == 'li' and tag.get('class') == ['menu_l2']

    def get_all_articles(self):

        # Step 1: Fetch main categories
        main_page = self.session.get(self.path, timeout=10)
        main_page_html = BeautifulSoup(main_page.text, 'html.parser')
        category_items = main_page_html.find('ul', class_='clearfix navlist_sub').find_all(self.has_exact_class)

        # Storing all the category links from the main page
        category_links = [item.find('a')['href'] for item in category_items]

        # Step 2: Extract all article links from all subcategories
        all_article_links = []
        for category_url in category_links:
            print(f"Getting article links from: {category_url}")
            all_article_links.extend(self.extract_article_links(category_url))

        print(f"Total article links collected: {len(all_article_links)}")

        # Step 3: Use threading to fetch articles in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            try:
                [executor.submit(self.get_article_from_link, url) for url in all_article_links]
            except Exception as e:
                print(e)
                    
data = Fetch_Data()
data.get_all_articles()
