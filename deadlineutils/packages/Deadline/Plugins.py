from ConnectionProperty import ConnectionProperty

class Plugins:
    """
        Class used by DeadlineCon to send Plugin requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetPluginNames(self):
        """ Gets the plugin names.
            Returns: The list of plugin names.
        """
        return self.connectionProperties.__get__("/api/plugins")

    def GetEventPluginNames(self):
        """ Gets the event plugin names.
            Returns: The list of event plugin names.
        """
        return self.connectionProperties.__get__("/api/plugins?EventNames=true")