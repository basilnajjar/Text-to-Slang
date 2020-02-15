from bs4 import BeautifulSoup
from selenium import webdriver

import requests
import random
import os

article_url= "https://www.thecrimson.com/article/2020/2/13/doe-investigation-foreign-governments/"
text_to_slang_translator_url = "https://www.noslang.com/reverse/"



def get_article():
    src = requests.get(article_url)
    if src.status_code == 200:
        soup = BeautifulSoup(src.content, 'lxml')
        text_collection = soup.find_all('p')[11:-3]

        article = ""
        for text in text_collection:
            article += text.getText()

        return article


def slang_it(article):
    # set up the selenium driver
    chromedriver = os.path.abspath("chromedriver.exe")
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://www.noslang.com/reverse/")

    inputElement = driver.find_element_by_id("p")
    inputElement.clear()

    # insert innocent article into the text-area
    inputElement.send_keys(article)

    # convert to slang
    login_form = driver.find_element_by_name('TheForm')
    submit_button = login_form.find_element_by_name("submit")
    submit_button.click()

    # retrieve slang article
    slang_article = driver.find_element_by_class_name('translation-text').text

    # add some nice words
    words = slang_article.split()
    article = ''
    skip = i = 0


    while i < len(words) - 2:
        if words[i].lower() == 'a':
            article += words[i] + " fookin'"

        elif words[i].lower() == 'an':
            n = random.choice([0, 1])
            if n:
                article += "a goddamn'"
            else:
                article += "a stupid"


        elif words[i].lower() == 'president':
            article += 'Bo$$'

        elif words[i].lower() == 'united' and words[i+1].lower() == 'states':
            article += 'U.S. of A'
            skip = 2

        elif words[i].lower() == 'u.s.a':
            article += 'U.S. of A'

        elif words[i].lower() == 'united' and words[i + 1].lower() == 'states' and words[i + 2].lower() == 'of' and words[i + 3].lower() == 'america':
            article += 'U.S. of A'
            skip = 4

        elif words[i].lower() == 'yale':
            article += 'Yale Safety School'

        elif words[i].lower() == 'yale' and words[i+1] == 'university':
            article += 'Yale Safety School'
            skip = 2

        elif words[i].isdigit():
            n = random.choice([0, 1])
            if n:
                article += words[i] + " fookin'"
            else:
                article += words[i] + ' bloody'

        else:
            article += words[i]
            skip = 1

        # add space between each word
        article += ' '
        i += skip

        # 20 words per line
        if i % 20 == 0:
            article += '\n'


    return article


if __name__ == "__main__":
    # scrape article from the crimson
    article = get_article()

    # convert article to slang
    slang_article = slang_it(article)

    with open("output.txt", "w") as f:
        f.write(slang_article)