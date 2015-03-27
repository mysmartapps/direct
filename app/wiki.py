# coding: utf-8

from bottle import run, route, debug, redirect, request
import sqlite3
import re

def template(name,content):
    return '<html><body><h1>%s</h1>%s</body></html>' % (name,content)

def wiki(content):
    content = content.replace('\n','<br/>\n')
    content = re.sub(r'\[(.+?)\]', r'<a href="\1">\1</a>', content)
    content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
    return content

def dbInit():
    conn = sqlite3.connect('wiki.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS pages(name TEXT, content TEXT)')
    conn.commit()

def dbGetPage(name):
    conn = sqlite3.connect('wiki.db')
    cur = conn.cursor()
    cur.execute('SELECT content FROM pages WHERE name=?', (name,))
    r = cur.fetchone()
    if r: return r[0]
    return ''

def dbSavePage(name,content):
    conn = sqlite3.connect('wiki.db')
    cur = conn.cursor()
    cur.execute('SELECT name FROM pages WHERE name=?', (name,))
    r = cur.fetchone()
    if r: # page exsist
        cur.execute('UPDATE pages SET content=? WHERE name=?', (content,name))
    else:
        cur.execute('INSERT INTO pages (name,content) VALUES(?,?)', (name,content))
    conn.commit()

@route('/')
@route('/:name')
def index(name='main'):
    content = dbGetPage(name)
    if not content: content = 'page not found. <a href="/edit/%s">create %s page?</a>' % (name,name)
    else: content = wiki(content) + '<hr/><a href="/edit/%s">edit</a>' % name
    return template(name, content)

@route('/edit/:name')
def edit(name):
    content = dbGetPage(name)
    content = '<form method=POST action="/save/%s"><textarea cols=60 rows=20 name=content>%s</textarea><input type=submit /></form>' % (name,content)
    return template(name, content)

@route('/save/:name', method='POST')
def save(name):
    content = request.POST.get('content','')
    dbSavePage(name, content)
    redirect('/%s' % name, 303)

dbInit()
debug(True)
run(port=8080,reloader=True)
