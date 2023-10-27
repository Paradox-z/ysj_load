# -*- coding:utf-8 -*-
from ssl import _create_unverified_context
from json import loads
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter.messagebox
import urllib.request
import urllib.parse

moviedata = ' [' \
            '{"title":"纪录片", "type":"1", "interval_id":"100:90"}, ' \
            ' {"title":"传记", "type":"2", "interval_id":"100:90"}, ' \
            ' {"title":"犯罪", "type":"3", "interval_id":"100:90"}, ' \
            ' {"title":"历史", "type":"4", "interval_id":"100:90"}, ' \
            ' {"title":"动作", "type":"5", "interval_id":"100:90"}, ' \
            ' {"title":"情色", "type":"6", "interval_id":"100:90"}, ' \
            ' {"title":"歌舞", "type":"7", "interval_id":"100:90"}, ' \
            ' {"title":"儿童", "type":"8", "interval_id":"100:90"}, ' \
            ' {"title":"悬疑", "type":"10", "interval_id":"100:90"}, ' \
            ' {"title":"剧情", "type":"11", "interval_id":"100:90"}, ' \
            ' {"title":"灾难", "type":"12", "interval_id":"100:90"}, ' \
            ' {"title":"爱情", "type":"13", "interval_id":"100:90"}, ' \
            ' {"title":"音乐", "type":"14", "interval_id":"100:90"}, ' \
            ' {"title":"冒险", "type":"15", "interval_id":"100:90"}, ' \
            ' {"title":"奇幻", "type":"16", "interval_id":"100:90"}, ' \
            ' {"title":"科幻", "type":"17", "interval_id":"100:90"}, ' \
            ' {"title":"运动", "type":"18", "interval_id":"100:90"}, ' \
            ' {"title":"惊悚", "type":"19", "interval_id":"100:90"}, ' \
            ' {"title":"恐怖", "type":"20", "interval_id":"100:90"}, ' \
            ' {"title":"战争", "type":"22", "interval_id":"100:90"}, ' \
            ' {"title":"短片", "type":"23", "interval_id":"100:90"}, ' \
            ' {"title":"喜剧", "type":"24", "interval_id":"100:90"}, ' \
            ' {"title":"动画", "type":"25", "interval_id":"100:90"}, ' \
            ' {"title":"同性", "type":"26", "interval_id":"100:90"}, ' \
            ' {"title":"西部", "type":"27", "interval_id":"100:90"}, ' \
            ' {"title":"家庭", "type":"28", "interval_id":"100:90"}, ' \
            ' {"title":"武侠", "type":"29", "interval_id":"100:90"}, ' \
            ' {"title":"古装", "type":"30", "interval_id":"100:90"}, ' \
            ' {"title":"黑色电影", "type":"31", "interval_id":"100:90"}' \
            ']'

def get_url_data_in_ranking_list(typeId, movie_count, rating, vote_count):
    """
    :param typeId:
    :param movie_count:
    :param rating:
    :param vote_count:
    :return:
    """

    try:
        context = _create_unverified_context()  # blocking SSL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        url = 'https://movie.douban.com/j/chart/top_list?type=' + str(typeId) + '&interval_id=100:90&action=unwatched&start=0&limit=' + str(movie_count)
        req = urllib.request.Request(url=url, headers=headers)
        f = urllib.request.urlopen(req, context=context)
        response = f.read()
        jsondata = loads(response)  # transforming json to Python objects

        res_list = []
        for subdata in jsondata:  # operating on each film in turn
            if (float(subdata['rating'][0]) >= float(rating)) and (float(subdata['vote_count']) >= float(vote_count)):
                sub_list= []
                sub_list.append(subdata['title'])
                sub_list.append(subdata['rating'][0])
                sub_list.append(subdata['rank'])
                sub_list.append(subdata['vote_count'])
                res_list.append(sub_list)

        for data in res_list:
            print(data)

        return [res_list, jsondata]

    except Exception as ex:
        err_str = "出现未知异常：{}".format(ex)
        return [err_str]

def get_url_data_in_keyword(key_word):
    """
    :param key_word:
    :return:
    """

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Setting the headless mode
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"')  # set user=agent
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # Setting up Developer Mode
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # do not load images

    load_driver_success = False  # Loading ChromeDriver
    browser = None
    wait = None
    try:
        browser = webdriver.Chrome(executable_path='D:/Program Files (x86)/chromedriver.exe', chrome_options=chrome_options)  # set ChromeDriver path
        browser.set_page_load_timeout(10)  # webpage loading timeout duration sets 10s
        browser.set_script_timeout(10)  # webpage js loading timeout duration sets 10s

        wait = WebDriverWait(browser, 10)  # waiting timeout duration sets 10s
        load_driver_success = True
    except Exception as ex:
        load_driver_success = False
        err_str = "加载chromedriver驱动失败，请下载chromedriver驱动并填写正确的路径。\n\n异常信息：{}".format(ex)
        return [err_str]


    # ChromeDriver running well
    if load_driver_success:

        try:
            # browsing papes
            browser.get('https://movie.douban.com/subject_search?search_text=' + urllib.parse.quote(key_word) + '&cat=1002')  # get methon, to capture return data
            # js dynamically rendered web pages
            # waiting class=root element in div
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.root')))

            dr = browser.find_elements(by=By.XPATH, value="//div[@class='item-root']") # Cause there are multiple results, get div with class item-root
            jsondata = []
            res_list = []
            for son in dr:
                moviedata = {'rating': ['', 'null'], 'cover_url': '', 'types': '', 'title': '', 'url': '', 'release_date': '', 'vote_count': '', 'actors': ''}
                sub_list = ['', '', '', '']

                url_element = son.find_elements(by=By.XPATH, value=".//a")  # Cause there are multiple results, get the url of the first 'a' tag
                if url_element:
                    moviedata['url'] = (url_element[0].get_attribute("href"))

                img_url_element = url_element[0].find_elements(by=By.XPATH, value=".//img")  # get the film poster image address
                if img_url_element:
                    moviedata['cover_url'] = (img_url_element[0].get_attribute("src"))

                title_element = son.find_elements(by=By.XPATH, value=".//div[@class='title']")  # get title element
                if title_element:
                    temp_title = title_element[0].text
                    moviedata['title'] = (temp_title.split('('))[0]
                    moviedata['release_date'] = temp_title[temp_title.find('(') + 1:temp_title.find(')')]
                    sub_list[0] = moviedata['title']

                rating_element = son.find_elements(by=By.XPATH, value=".//span[@class='rating_nums']")  # get ranking
                if rating_element:
                    moviedata['rating'][0] = rating_element[0].text
                    sub_list[1] = moviedata['rating'][0]

                vote_element = son.find_elements(by=By.XPATH, value=".//span[@class='pl']")  # get amount
                if vote_element:
                    moviedata['vote_count'] = vote_element[0].text.replace('(', '').replace(')', '').replace('人评价', '')
                    sub_list[3] = moviedata['vote_count']

                type_element = son.find_elements(by=By.XPATH, value=".//div[@class='meta abstract']")  # get type element
                if type_element:
                    moviedata['types'] = type_element[0].text
                    sub_list[2] = moviedata['types']

                actors_element = son.find_elements(by=By.XPATH, value=".//div[@class='meta abstract_2']")  # get actor element
                if actors_element:
                    moviedata['actors'] = actors_element[0].text

                jsondata.append(moviedata)
                res_list.append(sub_list)

            for data in res_list:
                print(data)

            browser.quit()
            return [res_list, jsondata]

        except Exception as ex:
            browser.quit()  # browser closed
            err_str = "chromedriver驱动加载成功，但是出现其他未知异常：{}".format(ex)
            return [err_str]
