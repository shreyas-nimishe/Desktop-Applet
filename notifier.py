#!/usr/bin/python
import sys, os, shutil, random, csv 
import appindicator, gtk, pynotify
import requests
from datetime import datetime
from lxml import html

class message():
        
    def __init__(self, item = '', title = '', msg = '', icon = '', notif_type = 'next/quit' ):  # add defaults
        self.item = item
        self.notif_type = notif_type
        pynotify.init("Shreyas_Nimishe")    # The Creator
         
        n = pynotify.Notification(title , msg, icon)
        n.set_urgency(pynotify.URGENCY_NORMAL)
        n.connect('closed', self.destroy)

        if(notif_type == 'Downloads'):
            #n.add_action("Video", "Video", self.movetoVideo)
            n.add_action("Music", "Music", self.movetoMusic)
            #n.add_action("Image", "Image", self.movetoPictures)
            n.add_action("Q", "Q", self.destroy)
            n.add_action("N", "N", self.Next)
        
        elif(notif_type == 'next/quit'):
            n.add_action('Next', 'Next', self.Next)
            n.add_action('Quit', 'Quit', self.destroy)

        
        n.show()
        gtk.main()
        
    def movetoMusic(self, n, item):
        move_to(self.item, 'Music')
        n.close()
        gtk.main_quit()

    def movetoPictures(self, n, item):
        move_to(self.item, 'Pictures')
        n.close()
        gtk.main_quit()

    def movetoVideo(self, n, item):
        move_to(self.item, 'Videos')
        n.close()
        gtk.main_quit()

    def Next(self, n, action=None):
        gtk.main_quit()

    def destroy(self, n, action=None):
        gtk.main_quit()
    
##--------------------------------------------------------------------------------------------##

def move_to(item, dest):
    # create function Auto Classify
    src_path = os.path.abspath('./Downloads') + '/' + item
    dest_path = os.path.abspath('./' + dest) + '/' + item
    shutil.move(src_path, dest_path)
    message('Transfer Completed!!', 'Status: Success')


def downloads_check():    
    for item in os.listdir('./Downloads'):
        if item[-3:] == 'mp4':
            message(item ,"Classify Downloaded items to folders", "Do you wish to move " + item + '?' + '\nQ] Quit \nN] Next'
, os.path.abspath('./machinity/img/dwn.png'), notif_type = 'Downloads' )

        print item

def main():
    downloads_check()

if __name__ == "__main__":  main()