from ConnectionProperty import ConnectionProperty
import json

class Users:
    """
        Class used by DeadlineCon to send User and UserGroup requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetUserNames(self):
        """ Gets all the user names.
            Return: The list of user names.
        """

        return (self.connectionProperties.__get__("/api/users?NamesOnly=true"))

    def GetUser(self, name):
        """ Gets a user's info.
            Input:  name: The user's name
            Return: The user info
        """
        result = (self.connectionProperties.__get__("/api/users?Name="+name.replace(' ','+')))
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result
    
    def GetUsers(self, names = None):
        """ Gets all the user infos.
            Input: names: The names of the users you want info for. If None get all users infos
            Return: The list of user infos.
        """
        script = "/api/users"
        if names != None:
            script =script +"?Name=" + ArrayToCommaSeperatedString(names).replace(' ','+')
            
        return (self.connectionProperties.__get__(script))

    def SaveUser(self, info):
        """ Saves a users info to the database.
            Input:  info: The Json object holding the users info
            Returns: Success message, or user name and ID if the user info is for a new user.
        """
        
        info = json.dumps(info)
            
        return self.connectionProperties.__put__("/api/users", info)
        

    def DeleteUser(self, name):
        """ Deletes a user.
            Input: name: The users name ( may be a list )
            Return: Success message
        """
            
        return self.connectionProperties.__delete__("/api/users?Name=" + ArrayToCommaSeperatedString(name).replace(' ','+'))
        
    def AddUserToUserGroup(self, user,group):
        """ Adds all of the users given to one or more user groups
            Input:  user: The users to be for the user group ( may be a list )
                    group: The user group ( may be a list )
            Returns: Success message
        """ 
        body = '{"Command":"add","User":'+json.dumps(user)+',"Group":'+json.dumps(group)+'}'
            
        return self.connectionProperties.__put__("/api/usergroups", body)

    def RemoveUserFromUserGroup(self, user,group):
        """ Removes all of the users given for one or more user groups
            Input:  user: The users to be for the user group ( may be a list )
                    group: The user group ( may be a list )
            Returns: Success message
        """
        body = '{"Command":"remove", "User":'+json.dumps(user)+',"Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/usergroups", body)

    def SetUsersForUserGroups(self, user,group):
        """  Sets all of the users for one or more user groups overriding their old lists
            Input:  user: The users to be for the user group ( may be a list )
                    group: The user group ( may be a list )
            Returns: Success message
        """ 
        body = '{"Command":"set", "User":'+json.dumps(user)+',"Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/usergroups", body)
        
    def GetUserGroupNames(self):
        """  Gets all the user group names.
            Returns: the user group names
        """
            
        return (self.connectionProperties.__get__("/api/usergroups"))
        
    def GetUserGroupsForUser(self, user):
        """ Gets all the user group names for a user
                Input: the user name
            Returns: a list of all the names of the user groups for the user
        """
        
        result = (self.connectionProperties.__get__("/api/usergroups?User="+user.replace(' ','+')))
            
        return result
    
    def GetUserGroup(self, name):
        """ Gets the users for the user group with the given name.
                Input: the user group name
            Returns: the users for the user group
        """
        result = (self.connectionProperties.__get__("/api/usergroups?Name="+name.replace(' ','+')))
            
        return result
        
    def NewUserGroups(self, names):
        """ Creates and saves new user groups with the given names. If no valid names are given an error will be returned.
            Input: the names for the new user group names. Any names that match existing user
            group names will be ignored.
            Returns: Success message.
        """
        
        body = '{"Group":'+json.dumps(names)+'}'
        
        return self.connectionProperties.__post__("/api/usergroups", body)
        
    def DeleteUserGroup(self, name):
        """ Deletes the user group with the given name.
            Input: the name of the group to delete.
            Returns: Success message.
        """
        
        result = (self.connectionProperties.__delete__("/api/usergroups?Name="+name.replace(' ','+')))
        
        return result

#Helper function to seperate arrays into strings
def ArrayToCommaSeperatedString(array):
    if isinstance(array, basestring):
        return array
    else:
        i=0
        script = ""
        for i in range(0,len(array)):
            if(i!=0):
                script+=","
            script += array[i];
        return script