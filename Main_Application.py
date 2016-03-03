#!/usr/bin/python
from notifier import *
from inp_dialog import *

def quit(item):
	gtk.main_quit()	

def sort_downloads(item):
	print 'Check' 
	print os.getcwd()
	downloads_check()

def create_user(item):
	get_credentials()

def get_random_quotes(item):
	try:
		from quote_random import *
		get_quotes()
	except:
		no_internet()

def imp_notify(item):
	message(title = 'IMPORTANT NOTIFICATION', 
		msg = 'This is to notify that shreyas is awesome!!!!',
		icon = os.path.abspath('./machinity/img/shr.jpg')
	)

def about_developers(item):
	message(title = 'SHREYAS NIMISHE', 
		msg = 'DESIGNATION: LEAD DEVELOPER\nBRANCH: Mathematics & Computing\nCOLLEGE: ISM, DHANBAD\n\nA problem solver by nature, Shreyas loves to think, discuss and create algorithms for almost every interesting problem. He also has a passion for machine learning and played a key role in creating predictive features of this app.',
		icon = os.path.abspath('./machinity/img/shr.jpg')
	)
	
	
def about_the_app(item):
	message(title = 'About Machinity Desktop-Applet',
		msg = 'This app is created mainly to get important online content/notifications on your local machine without explicitly going through the trouble of downloading it yourself.', 
		icon = os.path.abspath('./machinity/img/bot1.png')
	)	

def no_internet():
	message(title = 'No Internet Connection', 
		msg = 'Please try and connect to the internet to get new notifications.',
		icon =  os.path.abspath('./machinity/img/red_cross.png')
	)

def ism_notification(item):
	try:
		from ism_scraper import *
		extract_imp_notifications()
	except:
		no_internet()	

# All created features must be added in main() of machinity.py
def main():
	# The Main Applet Interface
	print '\n\n\tMachinity App has started..\n\t\t-Created by Shreyas Nimishe\n\n'

	a = appindicator.Indicator('machinity_applet', os.path.abspath('./img/icon2.png'), appindicator.CATEGORY_APPLICATION_STATUS)
	a.set_status( appindicator.STATUS_ACTIVE )
	menu = gtk.Menu()
	
	#print os.path.abspath('./img/tick_green.png')

	os.chdir('../')			# directory changed to home directory for easily accessing files, images etc

	opt1 = gtk.MenuItem( 'Downloads' )
	opt2 = gtk.MenuItem( 'Important Notification')
	opt3 = gtk.MenuItem( 'Create New User')
	opt4 = gtk.MenuItem( 'ISM Notification' )
	random_quotes = gtk.MenuItem( 'Random Quotes')
	opt5 = gtk.MenuItem( 'Developers' )	
	opt6 = gtk.MenuItem( 'About/Help' )
	Quit = gtk.MenuItem( 'Quit' )


	# Find a better way to initialize menu 
	menu.append(opt1)
	menu.append(opt2)
	menu.append(opt3)
	menu.append(opt4)
	menu.append(random_quotes)
	menu.append(opt5)
	menu.append(opt6)
	menu.append(Quit)
	

	a.set_menu(menu)


	opt1.show()
	opt2.show()
	opt3.show()	
	opt4.show()
	random_quotes.show()
	opt5.show()
	opt6.show()
	Quit.show()	


	opt1.connect('activate', sort_downloads)	
	opt2.connect('activate', imp_notify)
	opt3.connect('activate', create_user)
	opt4.connect('activate', ism_notification)
	random_quotes.connect('activate', get_random_quotes)	
	opt5.connect('activate', about_developers)
	opt6.connect('activate', about_the_app)
	Quit.connect('activate', quit)	


	gtk.main()

if __name__ == '__main__': main()
