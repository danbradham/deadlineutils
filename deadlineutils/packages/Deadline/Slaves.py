from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Slaves:
    """
        Class used by DeadlineCon to send Slave requests, as well as a few Pool and Group requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetSlaveNames(self):
        """ Gets all the Slave names.
            Returns: The list of slave names
        """
        return self.connectionProperties.__get__("/api/slaves?NamesOnly=true")

    def GetSlavesInfoSettings(self, names = None):
        """Gets multiple slaveslaves
            Inputs: names: the names of the slaves to get. If None get all slaves
            Returns: The list of slaves' infos and settings
        """
        script = "/api/slaves?Data=infosettings"
        if names != None:
            script = script +"&Name="+ ArrayToCommaSeparatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def GetSlaveInfoSettings(self, name):
        """ Gets a slave.
            Input: name: The slave name.
            Returns: The slave info and settings
        """
        
        result = self.connectionProperties.__get__("/api/slaves?Data=infosettings&Name="+name.replace(' ','+'))
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result

    def GetSlaveInfo(self, name):
        """ Gets a slave info object.
            Input: name: The slave name.
            Returns: The slave info
        """
        result = self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=info")
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result
        
    def GetSlaveInfos(self, names = None):
        """ Gets multiple slave info objects.
            Input: name: The slave names. If None return all info for all slaves
            Returns: list of the slave infos
            """
        script = "/api/slaves?Data=info"
        if names != None:
            script = script + "&Name="+ArrayToCommaSeparatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def SaveSlaveInfo(self, info):
        """ Saves slave info to the database.
            Input:  info: JSon object of the slave info
            Returns: Success message
        """
        info = json.dumps(info)
        body = '{"Command":"saveinfo", "SlaveInfo":'+info+'}'
        return self.connectionProperties.__put__("/api/slaves", body)

    def GetSlaveSettings(self, name):
        """ Gets a slave settings object.
            Input: name: The slave name.
            Returns: The slave settings
        """
        
        return self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=settings")
    
    def GetSlavesSettings(self, names = None):
        """ Gets multiple slave settings objects.
            Input: name: The slave names. If None return all info for all slaves
            Returns: list of the slave settings's info
        """
        script = "/api/slaves?Data=settings"
        if names != None:
            script = script + "&Name="+ArrayToCommaSeparatedString(names).replace(' ','+')
            
        return self.connectionProperties.__get__(script)

    def SaveSlaveSettings(self, info):
        """ Saves slave Settings to the database.
            Input:  info: JSon object of the slave settings
            Returns: Success message
        """
        info = json.dumps(info)
        body = '{"Command":"savesettings", "SlaveSettings":'+info+'}'
        
        return self.connectionProperties.__put__("/api/slaves", body)

    def DeleteSlave(self, name):
        """ Removes a slave from the repository.
            Input:  name: The name of the slave to be removed
            Returns: Success message
        """
        return self.connectionProperties.__delete__("/api/slaves?Name="+name)

    def AddGroupToSlave(self, slave, group):
        """ Adds a group to a slave.
            Input:  slave: The name of the slave or slaves( may be a list )
                    group: The name of the group or groups( may be a list )
            Return: Success message
        """
        body = '{"Slave":'+json.dumps(slave)+', "Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/groups", body)

    def AddPoolToSlave(self, slave, pool):
        """ Adds a pool to a slave.
            Input:  slave: The name of the slave or slaves( may be a list )
                    pool: The name of the pool or pools( may be a list )
            Return: Success message
        """
        body = '{"Slave":'+json.dumps(slave)+', "Pool":'+json.dumps(pool)+'}'
        
        return self.connectionProperties.__put__("/api/pools", body)

    def RemovePoolFromSlave(self, slave,pool):
        """ Adds a pool from a slave.
            Input:  slave: The name of the slave or slaves( may be a list )
                    pool: The name of the pool or pools( may be a list )
            Return: Success message
        """
        return self.connectionProperties.__delete__("/api/pools?Slaves="+ArrayToCommaSeparatedString(slave)+"&Pool="+ArrayToCommaSeparatedString(pool))

    def RemoveGroupFromSlave(self, slave,group):
        """ Adds a group from a slave.
            Input:  slave: The name of the slave or slaves( may be a list )
                    group: The name of the group or group( may be a list )
            Return: Success message
        """
        return self.connectionProperties.__delete__("/api/groups?Slaves="+ArrayToCommaSeparatedString(slave)+"&Group="+ArrayToCommaSeparatedString(group))

    def GetSlaveNamesInPool(self, pool):
        """ Gets the names of all slaves in a specific pool.
            Input:  pool: The name of the pool to search in.( May be a list)
            Returns: a list of all slaves that are in the pool
        """
        return self.connectionProperties.__get__("/api/pools?Pool="+ArrayToCommaSeparatedString(pool).replace(' ','+'))

    def GetSlaveNamesInGroup(self, group):
        """ Gets the names of all slaves in a specific group.
            Input:  group: The name of the group to search in. ( May be a list )
            Returns: a list of all slaves that are in the groups
        """
        return self.connectionProperties.__get__("/api/groups?Group="+ArrayToCommaSeparatedString(group).replace(' ','+'))

    def SetPoolsForSlave(self, slave,pool = []):
        """ Sets all of the pools for one or more slaves overriding their old lists
            Input:  slave: Slaves to be modified (may be a list)
                    pool: list of pools to be used
            Returns: Success message
        """
        body = '{"OverWrite":true, "Slave":'+json.dumps(slave)+',"Pool":'+json.dumps(pool)+'}'
        
        return self.connectionProperties.__put__("/api/pools", body)

    def SetGroupsForSlave(self, slave,group = []):
        """ Sets all of the groups for one or more slaves overriding their old lists
            Input:  slave: Slaves to be modified (may be a list)
                    pool: list of groups to be used
            Returns: Success message
        """
        body = '{"OverWrite":true, "Slave":'+json.dumps(slave)+',"Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/groups", body)

    def GetSlaveReports(self, name):
        """ Gets the reports for a slave.
            Input:  name: The name of the slave
            Returns all reports for the slave
        """
        return self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=reports")
        
    def GetSlaveReportsContents(self, name):
        """ Gets the reports contents for a slave.
            Input:  name: The name of the slave
            Returns all reports contents for the slave
        """
        
        return self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=reportcontents")

    def GetSlaveHistoryEntries(self, name):
        """ Gets the historyEntries for a slave.
            Input:  name: The name of the slave
            Returns: all history entries for the slave
        """
        return self.connectionProperties.__get__("/api/slaves?Name="+name.replace(' ','+')+"&Data=history")
