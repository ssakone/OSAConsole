import requests
import json

api_url = "http://localhost:8000"
authToken = ""
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


def auth(username, password):
	global authToken
	data = {
		"username": username,
		"password": password
	}
	result = requests.post("{}/api-token-auth/".format(api_url), data=data)
	if result.status_code == 200:
		authToken = json.loads(result.text)['token']
		return True
	return False

#if auth('enokas','sakone'):
#create_sondage("Test 2", "Pas grand chose comme description", 1, True)
#create_question("Comment aller vous", 2, 4)
create_question_response_proposal("NonNo", 3)