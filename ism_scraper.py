from notifier import *

def extract_imp_notifications():
	url = 'http://www.ismdhanbad.ac.in/'
	response = requests.get(url)
	
	tree = html.fromstring(response.text) 
	text = tree.xpath('//p[@style="text-align: justify;"]//text()')

	viewer = ''
	notice_board = []
	for notif in text:
		if not 'Click' in notif :
			viewer += notif 
		else :
			message('ISM Notification', viewer, os.path.abspath('./testing_area/img/ism.jpg'))
			notice_board.append(viewer)
			viewer = ''
				
	return notice_board
def main():
	extract_imp_notifications()

if __name__ == "__main__": main()