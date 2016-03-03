#usr/bin/python -tt
import time 
import math 
import sys
from datetime import datetime, date, time 
import os.path 
import csv 
import shutil 
import inspect 
import requests 
from urlparse import urljoin 
from  lxml import *
import xml.etree.ElementTree as ET 
from io import StringIO, BytesIO 
import grequests 
import gevent 
import requests
from bs4 import BeautifulSoup


class Response(object):
	def doc(self):
		if not hasattr(self, '_doc'):
			self._doc = html.fromstring(self.text)
		return self._doc

	def get_names_of_categories(self):

		raw_category_names = self.doc().xpath( '(//span[@itemprop="name"]')
		
		edited_categories = []		
		for name in raw_category_names:
			edited_categories.append(name[22:-16])

		return edited_categories

	def get_names_of_subcategories(self):
		names = self.doc().xpath( '(//h6/a/text())')
		
		edited_subcategories = []
		edited_subcategories.append("")
		for name in names:
			edited_subcategories.append(name[38:-32])
		
		return edited_subcategories

	def get_link_to_subcategories(self):
		return self.doc().xpath( '//p/a/@href')[:16]

	def is_page_a_leaf(self):	#important
		if self.url  == 'http://kiranprakashan.com/':
			return False
		else:
			return True

	def get_book_links(self):
		return self.doc().xpath('//h2[@class="product-name"]/a/@href')

	def get_category(self):
		return self.doc().xpath('//div[@class="breadcrumbs"]//text()')[-4]

	def get_book_details(self, cur_category = ''): # Extract the book content from the page and form the Book object
		book = Book() 
	
		book.publisher = ''         
		book.edition_pub_year = '' 
		book.weight = '' 
		book.price = ''
		book.synopsis = '' 
		book.pages = '' 
		book.publisher = '' 
		book.binding = ''
		book.ISBN13 = ''
		book.ISBN10 = '' 
		book.authors = ''
		book.title = ''

		try:
			book.subcategory = book.category = book.sub_subcategory = ''
			book.book_link = self.url
			book.title = unicode(self.doc().xpath('//div[@class="product-name"]/h1/text()')[0]).encode('ascii', 'ignore')
			
			book.category = unicode(self.doc().xpath('//div[@class="breadcrumbs"]//text()')[15]).encode('ascii', 'ignore')
			book.price = unicode(self.doc().xpath('//span[@class="regular-price"]/span[@class="price"]/text()')[0]).encode('ascii', 'ignore')

			book.weight = ''
			
			book.publisher = 'kiranprakashan'
			book.ISBN13 = ''
			
			book.authors = ''
			book.image_link = unicode(self.doc().xpath('//div[@class="product-img-box col-sm-5 col-md-5 col-sms-4 col-smb-12"]/img/@src')[0]).encode('ascii', 'ignore')
		
			book.edition_pub_year = ''
			synopsis = self.doc().xpath('//div[@class="std"]//text()')

			for para in synopsis:
				book.synopsis += unicode(para).encode('ascii', 'ignore') 
			
			book.ISBN10  = '' # failed = self.doc().xpath('(//li[@id="details"]/text())')
			book.binding = book.pages = ''

			
			
		except AttributeError as ex:
			print 'AttributeError msg:' + ex.message 
			print 'AttributeError reason:' + ex.reason 
			print 'AttributeError url:' + str(self.url) 
			pass 
		except UnicodeEncodeError as ex:
			print 'Unicode error msg:' + ex.message 
			print 'Unicode error reason:' + ex.reason 
			print 'Unicode error url:' + str(self.url) 
			pass 
		except:
			print 'book_url:' + self.url 
			print 'Error occurred serializing the object : ' + str(sys.exc_info()[0]) 

		return book 

	def get_category_name(self):
		cat_finder = self.doc().xpath('//span[@itemprop="name"]//li/strong//text()')
		if len(cat_finder) == 1 :
			book.category = 'others'
		elif len(cat_finder) == 2 :
			book.category = cat_finder[1]
		else:
			book.category = cat_finder[1]
			book.subcategory = cat_finder[2]
		return book.category

	def get_next_page_response(self, page_no, original_url):
		next_url = original_url + '?p=' + str(page_no + 1)
		response1 = requests.get(original_url + '?p=' + str(page_no), verify = False, timeout = 50)
		response2 = requests.get(original_url + '?p=' + str(page_no + 1), verify = False, timeout = 50)

		if(response1.get_book_links() == response2.get_book_links()):
			return None
		else:
			return response2 

#--- Response Class ends here ---#

def testing():
	print "Running tests\n"

	tocheck = "http://kiranprakashan.com/books/ssc-staff-selection-commission/ssc-10-2-level-stenographers-grade-c-d-pwb-hindi.html?___SID=U"
	respobj = requests.get(tocheck, verify=False, timeout=50)
	checker = respobj.get_book_details()
	print "\n\nInside Testing Area \n\n"
	print checker.ToList()
	print "\n\n TEST ENDS \n\n"	
	sys.exit()

#testing function ends here

def main():
	for method_name, method in inspect.getmembers(Response, inspect.ismethod):  
		setattr(requests.models.Response, method_name, method.im_func)

	client = requests.Session()			# requests session used after logging in to linkedin

	HOMEPAGE_URL = 'https://www.linkedin.com'
	LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'	

	html = client.get(HOMEPAGE_URL).content
	soup = BeautifulSoup(html)
	csrf = soup.find(id="loginCsrfParam-login")['value']	

	login_information = {
	    'session_key':'shnimishe@gmail.com',
	    'session_password':'password',
	    'loginCsrfParam': csrf,
	}

	client.post(LOGIN_URL, data=login_information)	

	client.get('enter url')

	# Register out custom methods on the Requests::Response object
	

	#testing()

	# Log the scrapped categories details for efficiency
	already_scrapped_data = {}
	log_data = ()
	log_scrapping_progress_file_name = "linkedin_log.tsv"
	if os.path.isfile(log_scrapping_progress_file_name):
	    log_data = tuple(open(log_scrapping_progress_file_name, 'r'))
	    
	scrape_log_file  = open(log_scrapping_progress_file_name, "ab")
	scrape_log_filewriter = csv.writer(scrape_log_file, delimiter='\t')

	# global varialbes
	output_file_name = "linkedin.tsv"
	books_outfile  = open(output_file_name, "ab")
	book_filewriter = csv.writer(books_outfile, delimiter='\t')

	for line in log_data:
		list_t = line.split("\t")
		cat_t = list_t[0]
		already_scrapped_data[cat_t] = 1

	queue = []	# list is taken as queue as it can pop from the front
	queue.append(home_page)
	
	# BFS used for traversing entire site
	while queue :
		cur_page = queue.pop(0)
		pageresponse = requests.get(cur_page, verify = False, timeout = 50)

		print cur_page
		if (pageresponse.is_page_a_leaf()):
			
			#visiting sub category pages and extracting book info
			cur_category =  pageresponse.get_category()
			print "\t", cur_category, "\n"
			page_no = 1
			url = cur_page
			pgresponse = requests.get(url, verify = False, timeout = 50) #initialize to first page

			if cur_category in already_scrapped_data:
				print "\tSkipping Category ==> Already Completed\n"
				continue

			books = []
			while True : #entered leaf node
				
				
				book_urls = pgresponse.get_book_links()

				print "\n\t Page : ", page_no 

				for book_link in book_urls:
					
					page = requests.get(book_link, verify = False, timeout = 50)
					cur_book = page.get_book_details(cur_category,)
					books.append(cur_book)

					print  cur_book.title , "\n\n"
					#extracted book info for this page

				pgresponse = pageresponse.get_next_page_response(page_no, url)	#change page from pg_no => pg_no + 1
				page_no = page_no + 1
				if pgresponse == None:	 # subcategory completed
					try:            
						# write books to a file
						for bk in books:
							lst_temp = bk.ToList()
							
							book_filewriter.writerow(lst_temp) 
							books_outfile.flush() 
						del books[:] 
				                       
						# Log the scrape progress details as Category name 
						already_scrapped_data[cur_category] = 1		#category completed
						scrape_log_filewriter.writerow([cur_category, 1]) 
						scrape_log_file.flush() 
					except IndexError as ex:
						print 'IndexError msg:' + str(ex.message)         
						pass 
					except AttributeError as ex:
						print 'AttributeError msg:' + str(ex.message) 
						print 'AttributeError reason:' + str(ex.reason) 
						pass 
					except UnicodeEncodeError as ex:
						print 'Unicode error msg:' + str(ex.message) 
						print 'Unicode error reason:' + str(ex.reason) 
						pass 
					except:
						print 'Error occurred serializing the object : ' + str(sys.exc_info()[0]) 
					#------------------------------------------------------------------------------	
					break
		else:
			links = pageresponse.get_link_to_subcategories()
			for link in links:
				queue.append(link)

			print "\tTotal Categories = " ,len(links), '\n\n'
	#--------------BFS ENDS HERE------------------------------------

	# Close the file handlers
	scrape_log_file.flush()
	scrape_log_file.close()

	books_outfile.flush()
	books_outfile.close()

if __name__ == "__main__" : main()