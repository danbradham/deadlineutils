from ConnectionProperty import ConnectionProperty

class JobTaskLimit:
    """
        Class used by DeadlineCon to send Job task limit requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetJobTaskLimit(self):
        """ Gets the job task limit
            Returns: The job task limit
        """
        return self.connectionProperties.__get__("/api/jobtasklimit")