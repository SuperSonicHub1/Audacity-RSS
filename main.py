from generator import generate_feed
from flask import Flask, redirect, make_response

FRONT_PAGE = """<h1>Audacity Posts Feed</h1>
Audacity posts some really neat stuff on their <a href='https://www.audacityteam.org/posts/'>site</a>, but it's hillariously unaccessable due to the lack of an RSS feed. So, I made one myself!
<br>
<a href='/feed'>Visit feed</a>"""

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
	return redirect("https://www.audacityteam.org/wp-content/uploads/2016/04/cropped-favicon-270x270.png")

@app.route("/")
def index():
	return FRONT_PAGE

@app.route("/feed")
def feed():
	audacity_feed = generate_feed()
	response = make_response(audacity_feed.rss())
	response.headers.set('Content-Type', 'application/rss+xml')
	return response

app.run(host='0.0.0.0',port=8080)
