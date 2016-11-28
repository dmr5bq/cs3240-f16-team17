import requests
import getpass
from os.path import expanduser
import getpass
import mainGUI
from bs4 import BeautifulSoup

home = expanduser("~")

def download():
	### Login ###
	print("-----------------------------------------------------------------\n")
	print("Please log in.")
	username = input("Username: ")
	password = getpass.getpass("Password: ")

	URL = 'http://localhost:8000/users/login/'
	client = requests.session()
	cookie = client.get(URL)  # sets cookie
	soup = BeautifulSoup(cookie.text, "html.parser")
	csrf = soup.find('input', {'name':'csrfmiddlewaretoken'})['value']
	login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrf, next='/')
	client.post(URL, data=login_data)

	### Get Reports ###
	URL2 = 'http://localhost:8000/reports/my_reports/'
	req2 = client.get(URL2)

	### Parse Report String ###
	downloaded = False
	try:
		linkDict = {}
		recentLink = ''
		recentStrinpped = ''
		built = ''
		start = req2.text.find('<div class=\"list-group\">')
		#print('starting at:', start)
		temp = req2.text[start:req2.text.find('</div>', start, len(req2.text)-1)]
		parseStr = temp.splitlines()
		print('Select a Report or Folder:', end = '')
		for str in parseStr:
			stripped = str.lstrip().rstrip()
			if '<a href=\"' in stripped:
				end = stripped.find('class=\"') - 2
				recentLink = stripped[9:end]
			if('<' not in str and len(stripped) > 0):
				if(stripped == '&nbsp;'):
					pass
				elif('made on ' in stripped):
					print(stripped, end=' ')
				elif(stripped != 'Your Reports:'):
					print('\n\t' + stripped, end = ' ')
					linkDict.update({stripped : recentLink})
		print('\n')
		while(not downloaded):
			navigateTo = input()
			if(navigateTo in linkDict):
				if('/reports/folder/' in linkDict[navigateTo]):
					print('Now browsing folder: ', navigateTo)
					req2 = client.get('http://localhost:8000' + linkDict[navigateTo])
					start = req2.text.find('<li class=\"list-group-item list-group-item-info\">')
					temp = req2.text[start:req2.text.find('</div>', start, len(req2.text) - 1)]
					parseStr = temp.splitlines()
					print('Select a Report or Folder to Navigate:', end='')
					for str in parseStr:
						stripped = str.lstrip().rstrip()
						if '<a href=\"' in stripped:
							end = stripped.find('class=\"') - 2
							recentLink = stripped[9:end]
						if ('<' not in str and len(stripped) > 0):
							if (stripped == '&nbsp;'):
								pass
							elif ('made on ' in stripped):
								print(stripped, end=' ')
							elif (stripped != 'My Reports'):
								print('\n\t' + stripped, end=' ')
								linkDict.update({stripped: recentLink})
					print('\n')
				elif('/reports/report/' in linkDict[navigateTo]):
					print('Now browsing report: ', navigateTo)
					req2 = client.get('http://localhost:8000' + linkDict[navigateTo])
					start = req2.text.find('<li class=\"list-group-item list-group-item-info\">')
					temp = req2.text[start + 49:]
					start = temp.find('<li class=\"list-group-item list-group-item-info\">')
					temp = temp[start:temp.find('</div>', start, len(temp) - 1)]
					parseStr = temp.splitlines()
					print('Choose a File to Download:', end='')
					for str in parseStr:
						stripped = str.lstrip().rstrip()
						if '<a href=\"' in stripped and '/file/download/' in stripped:
							end = stripped.find('class=\"') - 2
							linkDict.update({recentStripped : stripped[9:end]})
						if ('<' not in str and len(stripped) > 0):
							if (stripped == '&nbsp;'):
								pass
							elif ('made on ' in stripped):
								print(stripped, end=' ')
							elif (stripped != 'Report content:'):
								print('\n\t' + stripped, end=' ')
								recentStripped = stripped
					print('\n')
				else:
					print('Downloading...')
					downLink = 'http://localhost:8000' + linkDict[navigateTo]
					req2 = client.get(downLink, stream=True)
					with open(navigateTo, 'wb') as file:
						for chunk in req2.iter_content(chunk_size=1024):
							if chunk:
								file.write(chunk)
					file.close()
					downloaded = True
					print('File successfully downloaded to current working directory')
			else:
				print('That file does not exist')
	except Exception:
		print("\nLogin failed.")
		download()
	menu()

def menu():
	print("-----------------------------------------------------------------\n")
	print("Welcome to SecureShare FDA.\n\nChoose an action:\n1. Download a file from a report\n2. Encrypt/decrypt an existing file\n3. Exit\n")
	response  = input("Menu Selection: ")
	r = 0
	try:
		r = int(response)
		if r > 4 or r < 1:
			print("The number you entered is invalid.")
			menu()
	except Exception:
		print("Please enter a valid integer.")
		menu()

	if r==1:
		download()
	elif r==2:
		mainGUI.main()
	elif r==3:
		print("Goodbye")
		print("-----------------------------------------------------------------")
		exit()

if __name__ == '__main__':
	menu()
