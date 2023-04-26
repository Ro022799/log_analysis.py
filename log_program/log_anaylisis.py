#!/usr/bin/env python
import re
import os
import sys
import csv
import operator
from tarfile import ExtractError
from typing import NamedTuple
class Users(NamedTuple):
	action: str
	message: str
	user: str

"""Checks the number of paramateres passed into the function"""
def parameters(number)->int:
	if len(sys.argv) !=2:
		raise ValueError('Program requires two parameters instead of {}\n'.format(number))
	else:
		return 1
"""Checks if the given filename have the correct paramaters"""
def file(filename:str)->str:
	if type(filename) not in [str]:
		raise TypeError ('File must be a string\n')
	if re.match(r'^[a-zA-z\d]+\.[l][o][g]+$', filename) == None:
		raise TypeError ('File must be a log file')
	if os.path.exists(filename) != True:
		raise FileNotFoundError('{} does not exists\n'.format(filename))
	else:
		return filename
"""Iterate over the log file to check the information"""
def information(filename:str):	
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
"""Creates the dictonaries in a sorted way"""
def diccionarios():
	per_user ={}
	errors ={}
	for token in information(filename):
		if token.user not in per_user.keys():
			per_user[token.user] = {}
			per_user[token.user]['INFO'] = 0
			per_user[token.user]['ERROR']= 0
		if token.action == 'ERROR':
			errors[token.message] = errors.get(token.message, 0) +1
			per_user[token.user]['ERROR'] +=1
		elif token.action == 'INFO':
			per_user[token.user]['INFO'] +=1
	"""If dictionaries does not have information raise ExtractError"""
	if len(per_user)== 0 and len(errors) ==0:
		raise ExtractError('Dictionaries without information')
	errors= sorted(errors.items(), key= operator.itemgetter(1), reverse= True)
	per_user = sorted(per_user.items())

	return per_user, errors
"""Creates the csv files"""
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
	

if __name__ == '__main__':
	number = parameters(len(sys.argv))
	filename = sys.argv[number]
	filename = file(filename)
	information(filename)
	user, error =diccionarios()
	csv_generated(user, error)
	sys.exit(0)
