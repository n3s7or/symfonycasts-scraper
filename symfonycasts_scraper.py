import argparse
import requests
from bs4 import BeautifulSoup

class scrape_symfonycasts:

	def __init__(self, start, end, course):
		self.__session = None
		self.__token = None
		self.__user_email = ''
		self.__user_passw = ''
		self.__rango = [start != None if start else 1, end]
		self.__curse = '/screencast/' + course

		# Constants
		self.__BASE_URL = 'https://symfonycasts.com'
		self.__LOGIN_URL = '/login'
		self.__LOGIN_CHECK = '/login_check'
		self.__USER_AGENTS = {
			'mozilla':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
			'chrome':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'safari':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
		}
		self.__DOWNLOAD_SUFFIX = '/download/video'
	
	def get_direct_links(self):
		with requests.Session() as self.__session:
			self.__token = self.__get_token(self.__get_page_dom(self.__BASE_URL+self.__LOGIN_URL))
			self.__authenticate()

			dynamic_suffix_links = self.__get_links(self.__get_page_dom(self.__BASE_URL+self.__curse))			
			dynamic_download_links = list(self.__gen_dyn_down_link(dynamic_suffix_links))

			if self.__rango[1] == -1:
				self.__rango[1] = len(dynamic_download_links)

			for i in range(self.__rango[0]-1,self.__rango[1]):
				yield self.__session.head(self.__session.head(dynamic_download_links[i]).headers['location']).headers['location']

	def __gen_dyn_down_link(self,dsl):
		for i in dsl:
			yield self.__BASE_URL + i + self.__DOWNLOAD_SUFFIX

	def __get_links(self, html):
		chapter_list = html.find('div',class_='chapter-list')
		chapter_list_item = chapter_list.find_all('li')
		for item in chapter_list_item:
			if item.div.div.a['class'][0] != 'js-no-follow-link':
				yield item.div.div.a['href']	

	def __authenticate(self):
		data = {
			'_csrf_token'  : self.__token,
			'_email' 	   : self.__user_email,
			'_password'    : self.__user_passw,
			'_submit'      : '',
			'_target_path' : self.__BASE_URL
		}
		
		r = self.__session.post(self.__BASE_URL + self.__LOGIN_CHECK, data=data)
		
		if r.url == self.__BASE_URL + self.__LOGIN_URL:
			raise Exception('Invalid username or pass.')

	def __get_token(self, html):
		login_sub_btn = html.find(class_='login-submit-btn')
		return login_sub_btn.input['value']

	def __get_page_dom(self, url):
		headers = {
			'user-agent': self.__USER_AGENTS['mozilla']
		}
		r = self.__session.get(url=url,headers=headers)
		return BeautifulSoup(r.text, 'html.parser')

def prompt_user():
	#user_mail = input('Email: ')
	#user_pass = input('Password: ')
	course = '/screencast/' + input('Curso: /screencast/')
	
	rango = [1,0]
	inp = input('Rango [end, or start,end]: ').replace(' ','').split(',')

	if len(inp) > 2:
		raise Exception('Rango: No mas de dos argumentos')
	elif len(inp) == 2:			
		rango[0] = int(inp[0])
		rango[1] = int(inp[1])
	elif len(inp) == 1 and inp[0] != '':
		rango[1] = int(inp[0])

	#return [user_mail, user_pass, course, rango]
	return [course, rango]

def Main():

	# Prompt user disabled, user and pass must be wired in the constructor

	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=int, help='download from')
	parser.add_argument('--end', type=int, help='download to')
	parser.add_argument('--course', required=True, help='Course\'s name')
	args = parser.parse_args()
	
	symfonycasts = scrape_symfonycasts(
		start = args.start,
		end = args.end,
		course = args.course
	)

	with open('out.txt','w') as f:
		for direct_link in symfonycasts.get_direct_links():
			f.write(direct_link + '\n')

if __name__ == '__main__':
	Main()