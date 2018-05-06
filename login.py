import sys
from simple_salesforce import Salesforce

def login():
    print ('start logging')

    userName = "caffe.look@gmail.com"
    password = "bY5fuBPu"

    sf = Salesforce(userName, password, '')
    
    print('complete logging')

    return sf
