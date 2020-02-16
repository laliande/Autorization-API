from dotenv import load_dotenv
from os import path, getenv
from pymongo import MongoClient
from datetime import datetime

dotenv_path = path.join('process.env')
if path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token = getenv("MONGO")
client = MongoClient(token)
db = client['db']
collection = db.logins


class Login:
    def __init__(self, name, surname, email, login, password, date=datetime.now()):
        self.name = name
        self.surname = surname
        self.email = email
        self.login = login
        self.password = password
        self.date = date

    def __repr__(self):
        return 'Login: {}, password: {}'.format(self.login, self.password)

    def createRecord(self):
        record = {}
        for key, value in self.__dict__.items():
            record.update({key: value})
        return record

    def addRecordToBD(self):
        record = self.createRecord()
        collection.insert_one(record)


user = Login('Daniella', 'flask', 'flask', 'flask', 'flask', 'flask')
user.addRecordToBD()
