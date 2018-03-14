from ConnectionProperty import ConnectionProperty
from DeadlineUtility import ArrayToCommaSeparatedString
import json

class Groups:
    """
        Class used by DeadlineCon to send Group requests. Additional
        Group requests related to Slaves can be found in the Slaves.py file.
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetGroupNames(self):
        """ Gets the group names.
            Returns: The list of group names.
        """
        return self.connectionProperties.__get__("/api/groups")

    def AddGroup(self, name):
        """ Adds a Group to the repository.
            Params: name = The group name
            Returns: Success message
        """
        body = '{"Group":"'+name+'"}'
        
        return self.connectionProperties.__post__("/api/groups", body)

    def AddGroups(self, names):
        """ Adds some groups to the repository
            Params: names: list of group names to add
            Returns: Success message
        """
        
        body = '{"Group":'+json.dumps(names)+'}'
        
        return self.connectionProperties.__post__("/api/groups", body)
        
    def PurgeGroups(self, replacementGroup="none", groups=[], overwrite=False):
        """ Purges obsolete groups from repository using the provided replacementGroup. 
        If Overwrite is set, the groups provided will overwrite the old groups and the 
        replacementGroup must be a group in the provided groups list. If Overwrite is 
        not set, the groups provided will be added to the repository and obsolete groups
        will be purged using the replacement group. If Overwrite is not set, then no groups
        are required.
        
            Params: replacementGroup:  the group to replace obsolete groups on purge
                    groups: the list of groups to set or add
                    overwrite: boolean flag that determines whether we are setting or adding groups
            Returns: Success message if successful.
        """

        body = '{"ReplacementGroup":"'+replacementGroup+'", "Group":'+json.dumps(groups)+', "OverWrite":'+json.dumps(overwrite)+'}'
        
        return self.connectionProperties.__put__("/api/groups", body)

    def DeleteGroup(self, name):
        """ Removes a Group to the repository.
            Params: name = The group name
            Returns: Success message
        """
        return self.connectionProperties.__delete__("/api/groups?Group="+name.replace(' ', '+'))
    
    def DeleteGroups(self, names):
        """ Removes some groups from the repository
            Params: names: list of group names to remove
            Returns: Success message
        """
        
        return self.connectionProperties.__delete__("/api/groups?Group="+ArrayToCommaSeparatedString(names).replace(' ','+'))