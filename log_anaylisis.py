#!/usr/bin/env python
import re
import sys
import csv
import operator
from typing import NamedTuple
from concurrent.futures import ProcessPoolExecutor
class Users(NamedTuple):
	action: str
	message: str
	user: str
def informacion():
	filename = sys.argv[1]
	with open(filename,mode = 'r', encoding ='UTF-8') as file:
		lines = file.readlines()
		for line in lines:
			result = re.search(r'ticky: (INFO|ERROR) (.*)(\[.*\]|\s)+\((\w.*)+\)+$',line)
			if result == None:
				pass
			action = result.groups()[0]
			message = result.groups()[1]
			user = result.groups()[3]
			yield Users(action, message, user)


def diccionarios():
	per_user ={}
	errors ={}
	for token in informacion():
		if token.user not in per_user.keys():
			per_user[token.user] = {}
			per_user[token.user]['INFO'] = 0
			per_user[token.user]['ERROR']= 0
		if token.action == 'ERROR':
			errors[token.message] = errors.get(token.message, 0) +1
			per_user[token.user]['ERROR'] +=1
		elif token.action == 'INFO':
			per_user[token.user]['INFO'] +=1
	errors= sorted(errors.items(), key= operator.itemgetter(1), reverse= True)
	per_user = sorted(per_user.items())
	return per_user, errors
per_user, errors = diccionarios()

def csv_generated(per_user, errors):
    with open('error_message.csv', 'w') as file:
            file_1 = csv.writer(file)
            file_1.writerow(['ERROR','COUNT'])
            for error, message in errors:
                file_1.writerow([error,message])
    with open('user_statistics.csv', 'w') as file:
            file_1=csv.writer(file)
            file_1.writerow(['USERNAME', 'INFO', 'ERROR'])
            for pair in per_user:
                    user, message = pair
                    file_1.writerow([user, message['INFO'], message['ERROR']])

csv_generated(per_user, errors)
