#!/usr/bin/python
import appindicator
import gtk
import sys
import pynotify
import os

def message(title = "Notification", text  = "This is to notify that shreyas is awesome...", icon  = os.path.abspath("./shr.jpg")):
    pynotify.init("Completion Message")
    notification = pynotify.Notification(title, text, icon) 
    notification.set_urgency(pynotify.URGENCY_NORMAL)
    notification.show()

def quit(item):
	gtk.main_quit()

def imp_notification(item):
	message('IMPORTANT NOTIFICATION', 'This is to notify that Shreyas Nimishe is awesome!!!!', os.path.abspath('./shr.jpg'))

def ism_notif(item):
	message('ISM NOTIFICATION', 'ISM has officially been declared an IIT!!!!\n\nJust Kidding:)\n', os.path.abspath('./ism.jpg'))

def main():
	print 'App has started..'

	a = appindicator.Indicator('testing', os.path.abspath('./myicon.png'), appindicator.CATEGORY_APPLICATION_STATUS)
	a.set_status( appindicator.STATUS_ACTIVE )
	menu = gtk.Menu()
	
	opt1 = gtk.MenuItem( 'Important Notification')	
	opt2 = gtk.MenuItem( 'ISM Notification' )
	Quit = gtk.MenuItem( 'Quit' )

	menu.append(opt1)
	menu.append(opt2)
	menu.append(Quit)	

	a.set_menu(menu)

	opt1.show()
	opt2.show()
	Quit.show()	

	opt1.connect('activate', imp_notification)
	opt2.connect('activate', ism_notif)		
	Quit.connect('activate', quit)	

	gtk.main()

if __name__ == '__main__': main()
