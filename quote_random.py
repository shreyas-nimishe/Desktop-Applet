from notifier import *

def get_quotes():
	base_url = 'http://www.keepinspiring.me/famous-quotes-about-success/'
	response = requests.get(base_url)

	tree = html.fromstring(response.text) 
	quote_text = tree.xpath('//div[@class="author-quotes"]//text()')

	quotes_list = []
	for i in range(0, len(quote_text), 2 ):
		quotes_list.append(quote_text[i+1][2:], quote_text[i])
		message(quote_text[i+1][2:] , quote_text[i], os.path.abspath('./testing_area/img/wisdom6.png'))


