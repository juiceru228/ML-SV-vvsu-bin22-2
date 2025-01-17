import requests
from bs4 import BeautifulSoup
api_url = 'https://habr.com/kek/v2/articles/?news=true&excludedIds%5B0%5D=874496&fl=ru&hl=ru&page=1&perPage=100'


def get_api_data(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при запросе API: {response.status_code}")
        return None

def get_article_ids(data):
    publication_refs = data.get("publicationRefs", {})
    return list(publication_refs.keys())

def get_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_element = soup.find('h1', class_='tm-title tm-title_h1')
        if title_element:
            title = title_element.find('span').get_text()
        else:
            title = "Заголовок не найден"
        
        content_element = soup.find('div', id='post-content-body')
        if content_element:
            text_content = content_element.get_text()
        else:
            text_content = "Текст статьи не найден"
        return f"Title: {title}\nContent: {text_content}\n\n"
    else:
        print(f"Ошибка при запросе статьи: {response.status_code}")
        return None

def main():
    data = get_api_data(api_url)
    if data:
        article_ids = get_article_ids(data)
        if article_ids:
            print("ID статей:")
            print(article_ids)
            with open("articles.txt", "w", encoding="utf-8") as file:
                 for idx, article_id in enumerate(article_ids, start=1):
                    article_url = f"https://habr.com/ru/news/{article_id}/"
                    content = get_article_content(article_url)
                    if content:
                        file.write(f"Статья {idx}\n")
                        file.write(f"URL: {article_url}\n")
                        file.write(content)
                        file.write("\n" + "-"*50 + "\n\n")  # Разделитель между статьями
            print("Статьи успешно записаны в файл articles.txt")
        else:
            print("Не удалось найти статьи.")
    else:
        print("Не удалось получить данные от API.")

if __name__ == "__main__":
    main()
