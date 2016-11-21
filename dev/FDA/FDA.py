import urllib.request as ur
import requests
import getpass
import sys
import urllib
from os.path import expanduser
import wget
import getpass
import mainGUI
from simplecrypt import encrypt, decrypt
from bs4 import BeautifulSoup
from binascii import hexlify

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
	# print(csrf)
	login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrf, next='/')
	req = client.post(URL, data=login_data)
	# print(req)

	### Get Reports ###
	URL2 = 'http://localhost:8000/reports/my_reports/'
	client.get(URL)  # sets cookie
	soup2 = BeautifulSoup(client.get(URL2).text, "html.parser")
	csrf2 = soup2.find('input', {'name':'csrfmiddlewaretoken'})['value']
	login_data2 = dict(username=username, password=password, csrfmiddlewaretoken=csrf2, next='/')
	req2 = client.post(URL2, login_data2)

	### Parse Report String ###
	try:
		parseStr = req2.text
		reportList = parseStr.split(";")
		for x in reportList:
			if x=="":
				reportList.remove(x)
		reportNames = []
		for r in reportList:
			reportNames.append(r.split(",")[0])
		fileNames = []
		for f in reportList:
			if len(f)>=3:
				fileNames.append(f.split(",")[1])
		fileUrls = []
		for furl in reportList:
			if len(furl)>=3:
				fileUrls.append(furl.split(",")[2])
		print("\nWelcome User! Here are a list of your reports.\nPlease enter the report ID to view its file:\n")
		count = 0
		for name in reportNames:
			print(str(count) + ". " + name)
			count += 1
		number = input("\nReport Number: ")
		num = int(number)
		print("\nThe file in " + reportNames[num] + " is: ")
		print(fileNames[num])
		yn = input("\nDownload this file now? (y/n) ")
		url = "http://localhost:8000/reports/all_reports/detail/" + fileUrls[num]
	except Exception:
		print("\nLogin failed.")
		download()

	### Download File ###
	if yn is 'y':
		fi = wget.download(url)
		print("\n\nFile successfully downloaded to your current working directory.")
		menu()
	else:
		menu()

def menu():
	print("-----------------------------------------------------------------\n")
	print("Welcome to SecureShare FDA.\n\nChoose an action:\n1. Download a file from a report\n2. Encrypt/decrypt an existing file\n3. Exit\n")
	response  = input("Menu Selection: ")
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
