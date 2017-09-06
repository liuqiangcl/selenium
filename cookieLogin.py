#-*- coding:utf-8 -*-
import time
import requests
from selenium import webdriver

def get_system_cookies(url,account,password):
    '''通过request 登陆系统，获取cookie'''
    cookiesList = []
    data = {"username":account,"passwd":password}
    roomSession  = requests.Session()
    roomSession.post(url,data=data)
    loadCookies = requests.utils.dict_from_cookiejar(roomSession.cookies)
    for cookieName,cookieValue in loadCookies.items():
        cookies = {}
        cookies['name'] = cookieName
        cookies['value'] = cookieValue
        cookiesList.append(cookies)
    return cookiesList

def is_login_status_succeed(driver):
    '''判断是否登陆状态，非登陆状态,通过cookie登陆'''
    loginUrl = 'http://yingxiao.chewumi.com/login.php'  #登陆地址
    account = 'account'  #账号
    password = 'password'  #密码
    driver.get('http://yingxiao.chewumi.com/index.php') #测试是否为登陆状态
    if '请登录' in driver.page_source:  #判断是否登陆为登陆页面
        for cookie in get_system_cookies(loginUrl,account,password): #如果登陆界面获取cookie
            driver.add_cookie(cookie)  #添加cookie ，通过Cookie登陆
    return driver

def request_circle_details(driver,requestUrl):
    '''测试跳转圈子详情'''
    is_login_status_succeed(driver)
    driver.get(requestUrl)
    verifyField = driver.find_element_by_xpath('/html/body/div/div/div[2]/h1').text  #获取页面标题
    try:
        assert verifyField == '圈子详情'
        return '测试通过'
    except AssertionError as e:
        return '测试未通过'


'''测试下效果'''
requestUrl = 'http://yingxiao.chewumi.com/list.php?page=1'
driver = webdriver.Chrome()
driver.maximize_window()
print (request_circle_details(driver,requestUrl))
driver.get(requestUrl)
time.sleep(2)
driver.quit()
