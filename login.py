from simple_salesforce import Salesforce

def login():

    # TODO 設定ファイルを読み込むようにしたい
    userName = "xxx@xxx.com"
    password = "xxxxxxxxxxx"

    # Salesforceへログイン認証を実行する
    sf = Salesforce(userName, password, '')

    return sf
