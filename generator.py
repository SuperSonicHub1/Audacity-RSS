from extensions import MediaContent, Webfeeds, MediaItem, WebfeedsCover, WebfeedsIcon
from datetime import datetime
from typing import List
from requests import Session
from rfeed import Item, Feed, Guid, Image
from selectolax.parser import HTMLParser

session = Session()
URL = "https://www.audacityteam.org/posts/"
ICON_IMAGE = "https://www.audacityteam.org/wp-content/themes/wp_audacity/img/logo.png"
COVER_IMAGE = "https://www.audacityteam.org/wp-content/themes/wp_audacity/img/header-inner-bg.jpg"

def generate_carcass() -> Feed: 
	"""Generate feed carcass."""
	image = Image(
		ICON_IMAGE,
		"Logo for Audacity®",
		"https://www.audacityteam.org/"
	)
	icon = WebfeedsIcon(ICON_IMAGE)
	cover = WebfeedsCover(COVER_IMAGE)
	
	feed = Feed(
		title="Audacity® Posts",
		link="https://www.audacityteam.org/posts/",
		description="""Audacity is an easy-to-use, multi-track audio editor and recorder for Windows, macOS, GNU/Linux and other operating systems.
Developed by a group of volunteers as open source.""",
		language="en-US",
		lastBuildDate = datetime.now(),
		image=image,
		extensions=[
			MediaContent(),
            Webfeeds(), 
            icon,
			cover 
		]
	)
	
	return feed

def generate_feed() -> Feed:
	res = session.get(URL)
	res.raise_for_status()
	text = res.text

	tree = HTMLParser(text)
	posts = tree.css("article")

	items: List[Item] = []

	for post in posts:
		item_info = {}

		title = post.css_first("h1 > a")
		item_info["title"] = title.attributes["title"] or title.text()

		post_url = title.attributes["href"]
		item_info["link"] = post_url
		item_info["guid"] = Guid(post_url)

		post_date = post.css_first("time.published")
		item_info["pubDate"] = datetime.fromisoformat(post_date.attributes["datetime"])

		author = post.css_first("span.author > a")
		item_info["author"] = author.text()

		post_content = post.css_first("div.entry-content")
		item_info["description"] = post_content.html

		image = post.css_first("img")
		if image:
			media_item = MediaItem(
				image.attributes["src"],
				'image/png',
				'image',
				True,
			)
			item_info["extensions"] = [media_item]

		item = Item(**item_info)
		items.append(item)

	feed = generate_carcass()
	feed.items = items

	return feed
