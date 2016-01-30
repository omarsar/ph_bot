__author__ = 'omarsar'

#libraries
import ph_keys
import requests
from urllib.request import urlopen
import os
import re
import json
from twython import Twython


#initializers
twitter = Twython(os.environ.get('APP_KEY'),os.environ.get('APP_SECRET'),os.environ.get('OAUTH_TOKEN'), \
	os.environ.get('OAUTH_TOKEN_SECRET'))
parameters = {'access_token': os.environ.get('PH_ACCESS_TOKEN')}

#function to check if the account exists so as to verify and mention this handle name on Twitter
def check_twitter_account_status(twitter_handle):
	t_parameters = {'username': twitter_handle}
	user_url = "https://twitter.com/users/username_available"
	r = requests.get(user_url, params = t_parameters)	
	result = json.loads(r.text)

	print ("Twitter handle: ", result['reason'])

#TODO(2.0): function to try to get the twitter handle of a product from their site. 
def scrape_twitter_handle(url):
	try:
		r = requests.get(url)
		print (r.url)
		request = urlopen(r.url)
		html_page = request.read()

		twitter_handle = re.findall(r'https://twitter.com/(\w+)',str(html_page),re.I)
		if twitter_handle:
			return twitter_handle[0]
		else:
			return False
	except Exception as e:
		print(e.__doc__)
		print(e.message)

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
						#print(scrape_twitter_handle(p['redirect_url']))
						twitter_handle  = scrape_twitter_handle(p['redirect_url'])
						if twitter_handle:
							print (twitter_handle)
							check_twitter_account_status(twitter_handle)

		print (len(result['posts']))

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