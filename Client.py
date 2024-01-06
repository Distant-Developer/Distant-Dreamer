'''
ClientSession is class that is saved in the user's Session.
'''

from flask import json, jsonify
from SQL.Organization import Organization
from SQL.User import User
from mySQL import database

class ClientSession():
    def __init__(self, token, username, id, acct_type) -> None:
        self.token = token 
        self.username = username
        self.id = id
        self.acct_type = acct_type #User or Businses

        self.userAct = self.userAccount()
        self.bussAccts = self.get_organizations()
    
    def userAccount(self):
        user_raw = database.use_database(
            "SELECT * from users where id = ?", (self.id,), easySelect=False
        )
        #print(user_raw)
        user = [User(*row).to_dict() for row in user_raw]

        return user[0]
    
    def get_organizations(self):
        raw = database.use_database(
            "SELECT * from organizations where owner_id = ?", (self.id,), easySelect=False
        )
        return [Organization(*row).to_dict() for row in raw]
    
    def serialize(self):
        return {"token":self.token, "username":self.username, "id":self.id, "acct_type":self.acct_type, "userAct":self.userAct, "bussAccts":self.bussAccts}