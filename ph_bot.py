__author__ = 'omarsar'

#libraries
import ph_keys
import requests
from urllib.request import urlopen
import os
import json
from twython import Twython

#initializers
twitter = Twython(os.environ.get('APP_KEY'),os.environ.get('APP_SECRET'),os.environ.get('OAUTH_TOKEN'), \
	os.environ.get('OAUTH_TOKEN_SECRET'))
parameters = {'access_token': os.environ.get('PH_ACCESS_TOKEN')}


#function to try to get the twitter handle of a product from their site.
def get_twitter_handle(url):
	r = requests.get(url)
	print (r.url)
	print ("In getting twitter handle function")

#function to get the platforms of the products
def get_product_platforms(p):
	platforms = []
	for platform in p:
		platforms = platforms + [platform['name']]
	return platforms

#function to get top five products from product hunt
def pull_products():
	try:
		url = 'https://api.producthunt.com/v1/posts'
		r = requests.get(url, params = parameters)
		result = json.loads(r.text)

		if result['posts']:
			for p in result['posts']:
				
				if 'Web' in get_product_platforms(p['platforms']):
					print ("This product has a web version")

				print (p["name"])
				
				if p['redirect_url']:
					get_twitter_handle(p['redirect_url'])


		print (len(result['posts']))

		print ("In getting product function")
	except Exception as e:
		print (e.__doc__)
		print (e.message)



#post final tweet of trending products
def post_tweet():
	twitter.update_status(status='Product Index is a curated list of the most interesting tech products online')
	print ("Post tweet")


#main=========================================>
pull_products()
#post_tweet()