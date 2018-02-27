from login import login

# Salesforceへログイン認証を実行する
sf = login()

#TODO ボタン押下をトリガにしたい
#TODO レコード処理を別クラスに移したい
#TODO true/falseを処理したい
# デバイスレコードを作成する
sf.CoffeeServerStatus__e.create({ 'DeviceName__c':'Sensor0001', 'isAvailable__c':'true'}) #insert
#sf.Device__c.update('a017F00000OWh7T',{'Name': 'updateDeviceName'})    #update
#sf.Device__c.delete('a017F00000OWh7T')                                 #delete

#TODO 明確な終了条件が欲しい