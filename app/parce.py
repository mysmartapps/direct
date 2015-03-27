#!/usr/bin/python
#coding=utf-8

import math, sys, time, os, re, logging
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

LOGIN_URL = 'https://passport.yandex.ru/'
DIRECT_URL = 'https://direct.yandex.ru/'

def readLogin(n):
    file = open('data.txt')
    readlines = file.readlines()
    lenth = len(readlines)
    acs = math.ceil(lenth / 3) + 1
    print 'lines %d and users %d' % (lenth, acs)
    a = n * 2 - 2
    b = n * 2 - 1

    login = re.sub("^\s+|\n|\r|\s+$", '', readlines[a]) #clear str
    pswd = re.sub("^\s+|\n|\r|\s+$", '', readlines[b])  #clear str

    uloginandpassword = {'login' : login,
                         'password' : pswd}

    return uloginandpassword

def yaLogin(usernum):

    #get users param
    param = readLogin(usernum)
    username = param['login']
    password = param['password']

    print(username)
    print(password)

    result_no = 0
    # Browser
    br = Browser()

    # Cookie Jar
    #cj = cookielib.LWPCookieJar()
    #br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Little cheating...
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    br.open(LOGIN_URL)
    br.select_form(nr = 0)
    br['dbname'] = username
    br['passwd'] = password
    resp = br.submit()

    #TO DO test if login
    #if 'title name' in br.title():

    br.open(DIRECT_URL)
    html = br.response().read()

    #c_status = br.s

    soup = BeautifulSoup(''.join(html))

    #bb = soup.findAll("div", { "class" : "b-campaigns-list-item__state" })

    bb = soup.findAll("div", { "class" : "b-campaigns-list-item__state" })

    if not bb:
        aa = soup.find('p', 'p-common-error__message')
        if aa:
            print(aa.text)
        else:
            print('С вашим акком приключилась неведома хуйня')

    else:
        for allstatus in bb:
            print(allstatus.text)

        cc = soup.find('div', 'b-wallet-rest__total')
        print(cc.text)



def main():
    yaLogin(1)


if __name__ == '__main__':
    main()