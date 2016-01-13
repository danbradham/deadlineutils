from ConnectionProperty import ConnectionProperty
import json

class Pulse:
    """
        Class used by DeadlineCon to send Pulse requests. 
        Stores the address of the web service for use in sending requests.
    """    
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetPulseNames(self):
        """ Gets all the pulse names.
        Returns: The list of pulse names
        """
        return self.connectionProperties.__get__("/api/pulse?NamesOnly=true")

    def GetPulseInfo(self, name):
        """ Gets a pulse info.
            Input: name: The pulse name
            Returns: The pulse info.
        """
        return self.connectionProperties.__get__("/api/pulse?Name="+name.replace(' ','+')+"&Info=true")

    def GetPulseInfos(self, names = None):
        """ Gets a list of pulse infos.
            Input: name: The pulse names to be retrieved. If None then gets all pulse infos
            Returns: The pulse infos.
        """
        script = "/api/pulse?Info=true"
        if names != None:
            script = script+"&Names="+ArrayToCommaSeperatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def SavePulseInfo(self, info):
        """ Saves a pulse info to the database.
            Input:    info: JSon object of the Pulse info
            Returns: Success message
        """
        
        info = json.dumps(info)
        
        body = '{"Command":"saveinfo", "PulseInfo":'+info+'}'
        
        return self.connectionProperties.__put__("/api/pulse", body)
        
    def GetPulseSettings(self, name):
        """ Gets a pulse settings.
            Input: name: The pulse name
            Returns: The pulse settings.
        """
        return self.connectionProperties.__get__("/api/pulse?Name="+name.replace(' ','+')+"&Settings=true")

    def GetPulseSettingsList(self, names = None):
        """ Gets a list of pulse settings.
            Input: name: The pulse names to be retrieved. If None then gets all pulse settings
            Returns: The pulse settings.
        """
        script = "/api/pulse?Settings=true"
        if names != None:
            script = script+"&Names="+ArrayToCommaSeperatedString(names).replace(' ','+')
        
        return self.connectionProperties.__get__(script)

    def SavePulseSettings(self, settings):
        """ Saves a pulse settings to the database.
            Input:    settings: JSon object of the Pulse settings
            Returns: Success message
        """
        
        settings = json.dumps(settings)
        
        body = '{"Command":"savesettings", "PulseSettings":'+settings+'}'
        
        return self.connectionProperties.__put__("/api/pulse", body)
        
    def GetPulseInfoSettings(self, name):
        """ Gets a pulse info settings.
            Input: name: The pulse name
            Returns: The pulse info settings.
        """
        return self.connectionProperties.__get__("/api/pulse?Name="+name.replace(' ','+')+"&Settings=true&Info=true")

    def GetPulseInfoSettingsList(self, names = None):
        """ Gets a list of pulse info settings.
            Input: name: The pulse names to be retrieved. If None then gets all pulse info settings
            Returns: The pulse info settings.
        """
        script = "/api/pulse"
        if names != None:
            script = script+"?Names="+ArrayToCommaSeperatedString(names).replace(' ','+')
        
        return self.connectionProperties.__get__(script) 
        
    def DeletePulse(self, name):
        """ Deletes the Pulse instance associated with the name provided.
            Input: name: The pulse name to delete.
            Returns: Success message
        """
        return self.connectionProperties.__delete__("/api/pulse?Name="+name)

#Helper function to seperate arrays into strings
def ArrayToCommaSeperatedString(array):
    if isinstance(array, basestring):
        return array
    else:
        i=0
        script=""
        for i in range(0,len(array)):
            if(i!=0):
                script+=","
            script += str(array[i]);
        return script