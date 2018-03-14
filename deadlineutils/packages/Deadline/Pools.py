from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Pools:
    """
        Class used by DeadlineCon to send Pool requests. Additional
        Pool requests related to Slaves can be found in the Slaves.py file. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties

    def GetPoolNames(self):
        """ Gets the pool names.
            Returns: The list of pool names.
        """
        return self.connectionProperties.__get__("/api/pools")

    def AddPool(self, name):
        """ Adds a pool to the repository.
            Params: name = The pool name
            Returns: Success message
        """
        body = '{"Pool":"'+name+'"}'
        
        return self.connectionProperties.__post__("/api/pools", body)
        
    def AddPools(self, names):
        """ Adds some pools to the repository
            Params: names: list of pool names to add
            Returns: Success message
        """
        
        body = '{"Pool":'+json.dumps(names)+'}'
        
        return self.connectionProperties.__post__("/api/pools", body)
        
    def PurgePools(self, replacementPool="none", pools=[], overwrite=False):
        """ Purges obsolete pools from repository using the provided replacementPool. 
        If Overwrite is set, the pools provided will overwrite the old pools and the 
        replacementPool must be a pool in the provided pools list. If Overwrite is 
        not set, the pools provided will be added to the repository and obsolete pools
        will be purged using the replacement pool. If Overwrite is not set, then no pools
        are required.
        
            Params: replacementPool:  the pool to replace obsolete pools on purge
                    pools: the list of pools to set or add
                    overwrite: boolean flag that determines whether we are setting or adding pools
            Returns: Success message
        """

        body = '{"ReplacementPool":"'+replacementPool+'", "Pool":'+json.dumps(pools)+', "OverWrite":'+json.dumps(overwrite)+'}'
        
        return self.connectionProperties.__put__("/api/pools", body)

    def DeletePool(self, name):
        """ Removes a pool from the repository.
            Params: name = The pool name
            Returns: Success message
        """
        return self.connectionProperties.__delete__("/api/pools?Pool="+name.replace(' ','+'))
        
    def DeletePools(self, names):
        """ Removes some pools from the repository
            Params: names: list of pool names to remove
            Returns: Success message
        """
        
        return self.connectionProperties.__delete__("/api/pools?Pool="+ArrayToCommaSeparatedString(names).replace(' ','+'))
        