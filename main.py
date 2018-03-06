from login import login

sf = login()

sf.CoffeeServerStatus__e.create({ 'DeviceName__c':'Sensor0001', 'isAvailable__c':'true'}) #insert
#sf.Device__c.update('a017F00000OWh7T',{'Name': 'updateDeviceName'})    #update
#sf.Device__c.delete('a017F00000OWh7T')                                 #delete

