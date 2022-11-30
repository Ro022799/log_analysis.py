import re
import sys
import csv
import operator
per_user= {}
errors = {}
def dictados():
    filename = sys.argv[1]
    with open(filename,mode = 'r', encoding= 'UTF-8') as file:
        for line in file:
            result = re.search(r'ticky: (INFO|ERROR) (.*)(\[.*\]|\s)+\((\w.*)+\)+$',line)
            if result == None:
                continue
            action = result.groups()[0]
            message = result.groups()[1]
            user = result.groups()[3]
            if user not in per_user.keys():
                per_user[user] = {}
                per_user[user]['INFO'] = 0
                per_user[user]['ERROR']= 0
            if action == 'ERROR':
                errors[message] = errors.get(message, 0) +1
                per_user[user]['ERROR'] +=1
            if action == 'INFO':
                per_user[user]['INFO'] +=1
        dict_error = sorted(errors.items(), key= operator.itemgetter(1), reverse= True)
        dict_user = sorted(per_user.items())
        return dict_error, dict_user

def csv_generated():
    dict_error, dict_user = dictados()
    with open('error_message.csv', 'w') as files:
            file_1 = csv.writer(files)
            file_1.writerow(['ERROR','Count'])
            for error, mess in dict_error:
                file_1.writerow([error,mess])
    with open('user_statistics.csv', 'w') as file:
            file_1=csv.writer(file)
            file_1.writerow(['Username', 'INFO', 'ERROR'])
            for i in range(len(dict_user)):
                    user, mess = dict_user[i]
                    file_1.writerow([user, mess['INFO'], mess['ERROR']])
if __name__ == '__main__':
    csv_generated()
