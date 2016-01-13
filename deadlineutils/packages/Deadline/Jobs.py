import json
import ast
from ConnectionProperty import ConnectionProperty

class Jobs:
    """
        Class used by DeadlineCon to send Job requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
    
    def GetJobIds(self):
        """    Gets all the job IDs.
            Returns: The list of IDs.
        """

        return self.connectionProperties.__get__("/api/jobs?IdOnly=true")

    def GetJobs(self, ids = None):
        """    Gets all specified jobs, or all jobs if none specified.
            Input: List of job Ids
            Returns: The list of Jobs
        """
        script = "/api/jobs"
        if ids != None:
            script = script +"?JobID=" + ArrayToCommaSeperatedString(ids)
        return self.connectionProperties.__get__(script)

    def GetJobsInState(self, state):
        """    Gets all jobs in the specified state.
            Input: The state. Valid states are Active, Suspended, Completed, Failed, and Pending. Note that Active covers both Queued and Rendering jobs.
            Returns: The list of Jobs in the specified state.
        """
        return self.connectionProperties.__get__("/api/jobs?States=" + state)
        
    def GetJobsInStates(self, states):
        """    Gets all jobs in the specified states.
            Input: The list of states. Valid states are Active, Suspended, Completed, Failed, and Pending. Note that Active covers both Queued and Rendering jobs.
            Returns: The list of Jobs in the specified states.
        """
        return self.connectionProperties.__get__("/api/jobs?States=" + ",".join(states))

    def GetJob(self, id):
        """Gets a job
            Input: id: The job id (may be a list)
            Returns: The job/s (list)
        """
        
        jobId = ArrayToCommaSeperatedString(id)
        
        result = self.connectionProperties.__get__("/api/jobs?JobID="+jobId)
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result

    def SaveJob(self, jobData):
        """    Updates a job's properties in the database.
            Input: jobData: The jobs information in json format
            Returns: Success message
        """
        jobData = json.dumps(jobData)
        body = '{"Command":"save", "Job":'+jobData+'}'

        return self.connectionProperties.__put__("/api/jobs", body)

    def SuspendJob(self, id):
        """    Suspend a queued, rendering, or pending job.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"suspend", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)
        
    def SuspendJobNonRenderingTasks(self, id):
        """ Suspends the tasks for a job that are not in the rendering state.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"suspendnonrendering", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ResumeJob(self, id):
        """    Resumes a job.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"resume", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ResumeFailedJob(self, id):
        """    Resumes a failed job.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"resumefailed", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def DeleteJob(self, id):
        """    Deletes a job.
            Input: id: The job id
            Returns: Success message
        """
        return self.connectionProperties.__delete__("/api/jobs?JobID="+id)

    def RequeueJob(self, id):
        """    Requeues a job. All rendering and completed tasks for the job will be requeued.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"requeue", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ArchiveJob(self, id):
        """    Archive a non-queued, non-rendering job.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"archive", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ImportJob(self,file):
        """    Imports an archived job and returns it.
            Input: file: file location for archived job
            Returns: Success message
        """
        body = '{"Command":"import", "File":"'+file+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def PendJob(self, id):
        """    Place a job with dependencies in the pending state.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"pend", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def ReleasePendingJob(self, id):
        """    Releases a pending job.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"releasepending", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def CompleteJob(self, id):
        """    Completes a job. All incomplete tasks for the job will be marked as complete.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"complete", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def FailJob(self, id):
        """    Fails a job. All incomplete tasks for the job will be marked as failed.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"fail", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def UpdateJobSubmissionDate(self, id):
        """    Sets the job's submission date to the current time.
            Input: id: The jobs ID
            Returns: Success message
        """
        body = '{"Command":"updatesubmissiondate", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)

    def SubmitJobFiles(self, info, plugin, aux = [], idOnly = False):
        """    Submit a new job using job info file and plugin info file.
            Input:  info: The location of the Job Info File
                    plugin: The location of the pluign info file
                    aux: array of any additional auxiliary submission files, defaults to empty
                    idOnly: If True, only the job's ID is returned, defaults to False
            Returns: the new job
        """
               
        return self.connectionProperties.__post__("/api/jobs", buildJobSubmission(info, plugin, aux, idOnly))
        
    def SubmitJob(self, info, plugin, aux = [], idOnly = False):
        """    Submit a new job.
            Input:  info: Dictionary of job information.
                    plugin: Dictionary of plugin information for the job.
                    aux: array of any additional auxiliary submission files, defaults to empty
                    idOnly: If True, only the job's ID is returned, defaults to False
            Returns: the new job
        """
        
        body = '{"JobInfo":'+json.dumps(info)+',"PluginInfo":'+json.dumps(plugin)+',"AuxFiles":'+json.dumps(aux)
        if idOnly:
            body += ',"IdOnly":true'
        body += '}'
        return self.connectionProperties.__post__("/api/jobs", body)

#Machine Limits    

    def SetJobMachineLimit(self, id, limit, slaveList, whiteListFlag):
        """    Sets a job's machine limit.
            Input:  id: The job ID.
                    limit: The maximum number of slaves that can work on this job at any one time
                    slaveList: A list of slaves whare are either not allowed to work on or are the only allowed slave for a job
                    whiteListFlag: if true the slaves in the slavelist are the only slaves allowed to work on the job else, the slaves are now allowed to work on the job
            Returns: Success message
        """
        body = json.dumps({"Command":"setjobmachinelimit","JobID":id, "Limit":limit, "SlaveList":slaveList,"WhiteListFlag":whiteListFlag})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def AddSlavesToJobMachineLimitList(self, id, slaveList):
        """    Add additional slaves to the jobs limit list
            Input:  id: The job ID.
                    slaveList: The slaves to be added to the jobs machine limit list
            Returns: Success message
        """
        body = json.dumps({"Command":"addslavestojobmachinelimitlist","JobID":id, "SlaveList":slaveList})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def RemoveSlavesFromJobMachineLimitList(self, id, slaveList):
        """    Remove chosen slaves from the jobs limit list
            Input:  id: The job ID.
                slaveList: The slaves to be removed from the jobs machine limit list
            Returns: Success message
        """
        body = json.dumps({"Command":"removeslavesfromjobmachinelimitlist","JobID":id,"SlaveList":slaveList})
    
        return self.connectionProperties.__put__("/api/jobs", body)
        
    def SetJobMachineLimitListedSlaves(self, id, slaveList):
        """    Sets a job's machine limit slave list.
            Input:  id: The job ID.
                    slaveList: A list of slaves whare are either not allowed to work on or are the only allowed slave for a job
            Returns: Success message
        """
        body = json.dumps({"Command":"setjobmachinelimitlistedslaves","JobID":id, "SlaveList":slaveList})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def SetJobMachineLimitWhiteListFlag(self, id, whiteListFlag):
        """    Sets a job's machine limit white list flag.
            Input:  id: The job ID.
                    whiteListFlag: if true the slaves in the slavelist are the only slaves allowed to work on the job else, the slaves are now allowed to work on the job
            Returns: Success message
        """
        
        body = json.dumps({"Command":"setjobmachinelimitwhitelistflag","JobID":id, "WhiteListFlag":whiteListFlag})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def SetJobMachineLimitMaximum(self, id, limit):
        """    Sets a job's machine limit maximum number of slaves.
            Input:  id: The job ID.
                    limit: The maximum number of slaves that can work on this job at any one time
            Returns: Success message
        """
        body = json.dumps({"Command":"setjobmachinelimitmaximum","JobID":id, "Limit":limit})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def AppendJobFrameRange(self, id, frameList):
        """    Appends to a job's frame range without affecting the existing tasks. The only exception is if the job's chunk size is greater than one, and the last task is having frames appended to it.
            Input: id; The Job ID.
                    frameList: The additional frames to append.
            Returns: Success message
        """
        body = json.dumps({"Command":"appendjobframerange","JobID":id, "FrameList":frameList})
    
        return self.connectionProperties.__put__("/api/jobs", body)

    def SetJobFrameRange(self, id, frameList, chunkSize):
        """    Modifies a job's frame range. If the job is currently being rendered, any rendering tasks will be requeued to perform this operation.
            Input: id; The Job ID.
                    frameList: The frame list.
                    chunkSize: The chunk size.
            Returns: Success message
        """
        body = json.dumps({"Command":"setjobframerange","JobID":id, "FrameList":frameList, "ChunkSize":chunkSize})
    
        return self.connectionProperties.__put__("/api/jobs", body)
        
    #Job Details
    def GetJobDetails(self, ids):
        """ Gets the job details for the provided Job IDs.
            Input: The Job ids (may be a list)
            Return: The Job Details for the valid Job IDs provided.
        """
        
        script = "/api/jobs"

        script = script +"?JobID=" + ArrayToCommaSeperatedString(ids)+"&Details=true"
        return self.connectionProperties.__get__(script)
        
    #Undelete/Purge Deleted
    def GetDeletedJobs(self, ids = None):
        """ Gets the undeleted jobs that correspond to the provided job ids. If no ids are provided, gets all the deleted jobs.
            Input: The Job ids (optional, may be a list)
            Return: The job/s (list)
        """
        
        script = "/api/jobs?Deleted=true"
        
        if ids != None:
            script = script +"&JobID=" + ArrayToCommaSeperatedString(ids)
        return self.connectionProperties.__get__(script)
            
    def GetDeletedJobIDs(self):
        """    Gets all the deleted job IDs.
            Returns: The list of deleted job IDs.
        """

        return self.connectionProperties.__get__("/api/jobs?IdOnly=true&Deleted=true")
        
    def PurgeDeletedJobs(self, ids):
        """ Purges the deleted jobs that correspond to the provided ids from the deleted job collection.
            Input: The Deleted Job ids (may be a list)
            Return: Success message
        """
        
        script = "/api/jobs?Purge=true"
        
        script = script +"&JobID=" + ArrayToCommaSeperatedString(ids)
        return self.connectionProperties.__delete__(script)
        
    def UndeleteJob(self, id):
        """    Undeletes deleted job.
            Input: id: The job id
            Returns: Success message
        """
        body = '{"Command":"undelete", "JobID":"'+id+'"}'
        
        return self.connectionProperties.__put__("/api/jobs", body)
        
    def UndeleteJobs(self, ids):
        """    Undeletes deleted jobs.
            Input: id: The job ids
            Returns: Success message
        """
        #body = '{"Command":"undelete", "JobIDs":"'+id+'"}'
        body = json.dumps({"Command":"undelete","JobIDs":ids})
        return self.connectionProperties.__put__("/api/jobs", body)

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
        #script+="\""
        return script
        
def buildJobSubmission(info, plugins, aux, idOnly):
    
    infoText = fileRead(info)
    
    pluginsText = fileRead(plugins)
    
    body = '{"JobInfo":'+infoText+',"PluginInfo":'+pluginsText+',"AuxFiles":'+json.dumps(aux)
    if idOnly:
        body += ',"IdOnly":true'
    body += '}'
    
    return body
    
def fileRead(filelocation):
    
    file = open(filelocation, 'r')
    
    obj = '{'
    
    for line in file:
        
        line = line.replace('\n', '')
        line = line.replace('\t', '')
        
        tokens = line.split("=",1)
        if len(tokens) == 2:
            obj = obj + '"'+tokens[0].strip()+'":"'+tokens[1].strip()+'",'
        
    obj = obj[:-1]
    
    obj = obj + '}'
    
    return obj
    
    