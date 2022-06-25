import requests
import json
import argparse
import maskpass
import os
from colorama import init, Fore, Style
init()

def cls():
    os.system('cls')

api_url = "http://localhost:8000"
user = ""
authToken = ""


main_help = '''
1. Sondage
2. Resultat
0. Quitter
'''

sondage_help = '''
1. Liste des sondages
2. Ajouter un sondage
0. Retourner
'''

def getHeaders():
	global authToken
	heads = { "Authorization": "Token {}".format(authToken)}
	return heads

def create_sondage(libelle, description, verification, actif=False):
	data = {
		"libelle": libelle,
		"description": description,
		"verification": verification,
		"actif": actif
	}
	result = requests.post("{}/sondage/".format(api_url), data=data, headers=getHeaders())
	print(result.text, result.status_code)

def create_question(libelle, type_response, sondage):
	data = {
		"libelle": libelle,
		"type_response": type_response,
		"sondage": sondage
	}
	result = requests.post("{}/question/".format(api_url), data=data, headers=getHeaders())
	print(result.text, result.status_code)

def create_question_response_proposal(libelle, question):
	data = {
		"libelle": libelle,
		"question": question
	}
	result = requests.post("{}/response_proposal/".format(api_url), data=data, headers=getHeaders())
	print(result.text, result.status_code)


def interact():
	cls()
	print(main_help)
	while 1:
		try:
			choice = int(input(f'({Fore.GREEN}{api_url}{Style.RESET_ALL}) > '))
			if choice == 1:
				print(sondage_help)
				while 1:
					try:
						choice = int(input(f'({Fore.GREEN}{api_url}/sondage{Style.RESET_ALL}) > '))
						if choice == 1:
							print('sondage list')
						elif choice == 2:
							print('nouveau sondage')
						elif choice == 0:
							break
						else:
							print(f'({Fore.GREEN}{api_url}/sondage{Style.RESET_ALL}) unrecognized choice')
					except:
						print(f'({Fore.GREEN}{api_url}/sondage{Style.RESET_ALL}) unrecognized choice')
			elif choice == 2:
				print('Resultat')
			elif choice == 0:
				break
				exit()
			else:
				print(f'({Fore.GREEN}{api_url}{Style.RESET_ALL}) unrecognized choice')
		except:
			print(f'({Fore.GREEN}{api_url}{Style.RESET_ALL}) unrecognized choice')
			pass

def auth(username, password):
	global authToken, user
	data = {
		"username": username,
		"password": password
	}
	result = requests.post("{}/api-token-auth/".format(api_url), data=data)
	if result.status_code == 200:
		user = username
		authToken = json.loads(result.text)['token']
		return True
	return False


def checkHost(host):
	try: 
		ret = requests.get(host+"/question")
		if ret.status_code == 401:
			api_url = host
			return True
	except:
		return False
	return False

def authenticate(username=None):
	if username == None:
		username = input('Username: ')
	pwd = maskpass.askpass()
	return (username, pwd)
#if auth('enokas','sakone'):
#create_sondage("Test 2", "Pas grand chose comme description", 1, True)
#create_question("Comment aller vous", 2, 7)
# create_question_response_proposal("No", 11)
# create_question_response_proposal("Yes", 11)

parser = argparse.ArgumentParser(description="OpenSondage command line client")
parser.add_argument("host", help="Rest service server address")
parser.add_argument("-u","--username", help="votre nom d'utilisateur permet de vous authentifier")
parser.add_argument("-v","--verbose", help="Afficher plus de details", action="store_true")

args = parser.parse_args()

if args.host:
	if args.verbose:
		print('[...] Checking host')
	if checkHost(args.host) == False:
		print('[error] Invalid rest service host')
		exit(0)

	username, password = authenticate(args.username)
	if args.verbose:
		print('[auth] Authenticating...')

	if auth(username, password):
		print('[auth] Authenticated Successsfully')
		interact()
	else: 
		print('[auth] Authentication failed, credential incorrect')