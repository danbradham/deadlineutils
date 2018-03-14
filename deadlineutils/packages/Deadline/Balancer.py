from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Balancer:
    """
        Class used by DeadlineCon to send Balancer requests. 
        Stores the address of the web service for use in sending requests.
    """    
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetBalancerNames(self):
        """ Gets all the balancer names.
        Returns: The list of balancer names
        """
        return self.connectionProperties.__get__("/api/balancer?NamesOnly=true")

    def GetBalancerInfo(self, name):
        """ Gets a balancer info.
            Input: name: The balancer name
            Returns: The balancer info.
        """
        return self.connectionProperties.__get__("/api/balancer?Name="+name.replace(' ','+')+"&Info=true")

    def GetBalancerInfos(self, names = None):
        """ Gets a list of balancer infos.
            Input: name: The balancer names to be retrieved. If None then gets all balancer infos
            Returns: The balancer infos.
        """
        script = "/api/balancer?Info=true"
        if names != None:
            script = script+"&Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def SaveBalancerInfo(self, info):
        """ Saves a balancer info to the database.
            Input:    info: JSon object of the Balancer info
            Returns: Success message
        """
        
        info = json.dumps(info)
        
        body = '{"Command":"saveinfo", "BalancerInfo":'+info+'}'
        
        return self.connectionProperties.__put__("/api/balancer", body)
        
    def GetBalancerSettings(self, name):
        """ Gets a balancer settings.
            Input: name: The balancer name
            Returns: The balancer settings.
        """
        return self.connectionProperties.__get__("/api/balancer?Name="+name.replace(' ','+')+"&Settings=true")

    def GetBalancerSettingsList(self, names = None):
        """ Gets a list of balancer settings.
            Input: name: The balancer names to be retrieved. If None then gets all balancer settings
            Returns: The balancer settings.
        """
        script = "/api/balancer?Settings=true"
        if names != None:
            script = script+"&Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        
        return self.connectionProperties.__get__(script)

    def SaveBalancerSettings(self, settings):
        """ Saves a balancer settings to the database.
            Input:    settings: JSon object of the Balancer settings
            Returns: Success message
        """
        
        settings = json.dumps(settings)
        
        body = '{"Command":"savesettings", "BalancerSettings":'+settings+'}'
        
        return self.connectionProperties.__put__("/api/balancer", body)
        
    def GetBalancerInfoSettings(self, name):
        """ Gets a balancer info settings.
            Input: name: The balancer name
            Returns: The balancer info settings.
        """
        return self.connectionProperties.__get__("/api/balancer?Name="+name.replace(' ','+')+"&Settings=true&Info=true")

    def GetBalancerInfoSettingsList(self, names = None):
        """ Gets a list of balancer info settings.
            Input: name: The balancer names to be retrieved. If None then gets all balancer info settings
            Returns: The balancer info settings.
        """
        script = "/api/balancer"
        if names != None:
            script = script+"?Names="+ArrayToCommaSeparatedString(names).replace(' ','+')
        
        return self.connectionProperties.__get__(script)
        
    def DeleteBalancer(self, name):
        """ Deletes the Balancer instance associated with the name provided.
            Input: name: The balancer name to delete.
            Returns: Success message
        """
        return self.connectionProperties.__delete__("/api/balancer?Name="+name)