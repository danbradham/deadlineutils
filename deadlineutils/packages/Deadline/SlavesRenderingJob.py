from ConnectionProperty import ConnectionProperty

class SlavesRenderingJob:
    """
        Class used by DeadlineCon to send Slaves Rendering Job requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetSlavesRenderingJob(self, id, getIpAddress=False):
        """    Gets the list of slaves that are currently rendering a job.
            Input:  id: The job ID.
                getIpAddress: If True, the IP address of the slaves will be returned instead
            Returns: The list of slave names, or the list of slave IP addresses if getIpAddress is True
        """
        
        return self.connectionProperties.__get__("/api/slavesrenderingjob?JobID="+id+"&GetIpAddress="+str(getIpAddress))