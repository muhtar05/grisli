import os
import sys
import time
import datetime
import tornado.web
import tornado.ioloop
from tornado.ioloop import IOLoop
import tornado.wsgi
import tornado.websocket
from tornado.queues import Queue
from tornado import gen
from tornado.options import options,define,parse_command_line
from django.core.wsgi import get_wsgi_application

import sqlite3
import requests
from bs4 import BeautifulSoup


q = Queue()
clients = []
results = {}

DJANGO_APPS_DIR = os.path.dirname(os.path.abspath(__file__))

def _execute(query):
	
	dbPath = 'db.sqlite3'
	connection = sqlite3.connect(dbPath)
	cursorobj = connection.cursor()
	try:
		cursorobj.execute(query)
		result = cursorobj.fetchall()
		connection.commit()
	except Exception:
		raise
	connection.close()
	return result

class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		data_list = []
		self.render("service.html", links=data_list)

class Application(tornado.web.Application):
	def __init__(self,wsgi_app):
		self.wsgi_app = wsgi_app
		handlers = [
		     (r'/test-tornado',HelloHandler),
		     (r'/parser',ParserHandler),
		     (r'.*', tornado.web.FallbackHandler, dict(fallback=self.wsgi_app)),
		]
		settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #xsrf_cookies=True,

        )
		super(Application,self).__init__(handlers,**settings)




def get_url_info(url):
	try:
		req = requests.get(url)
		success = True
		soup = BeautifulSoup(req.text, 'html.parser')
		h1_markup = soup.select('h1')
		encoding = req.encoding
		status_code = req.status_code
		h1_title = h1_markup
		title = soup.title.string

	except requests.exceptions.RequestException as e:
		success = None
		title = ''
		encoding = ''

	return dict(
		title=title,
		success=success,
		encoding=encoding,
	)



class ParserHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("Web socket opened")
		clients.append(self)

	def on_close(self):
		print("Web socket close")

	def on_message(self, message):
		for url in results:			
			self.write_message(results[url])
			

	def check_origin(self, origin):
		return True
 


@gen.engine
def consumer():
	while True:
		item = yield q.get()
		time_url = item[2]
		times_url = datetime.datetime.strptime(time_url, "%Y-%m-%d %H:%M:%S")
		timeshift = times_url - datetime.datetime.utcnow()
		if (timeshift < datetime.timedelta(seconds=1)):
			seconds = 0
		else:
		    seconds = timeshift.seconds

		yield gen.Task(IOLoop.instance().add_timeout, time.time() + seconds)
		try:
			url_info = get_url_info(item[1])
			res = {
						"title": str(url_info["title"]),
						"encoding": str(url_info["encoding"]),
						"url": item[1],
						"success": url_info["success"],
						"time_url":str(time_url),
			}

			results[item[1]] = res

			for c in clients:
				c.write_message(res)
			
			q.task_done()
			
		except:
			pass
			break	

		

def main():
	parse_command_line()
	sys.path.insert(0, DJANGO_APPS_DIR)
	os.environ['DJANGO_SETTINGS_MODULE'] = 'grisli.settings'
	wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
	tornado_app = Application(wsgi_app)
	tornado_app.listen(8001)
	rows = _execute('SELECT * FROM links_link ORDER BY `when`')
	for row in rows:
		q.put(row)
	    
	IOLoop.instance().add_callback(consumer)
	IOLoop.instance().start()

if __name__ == '__main__':
	main()