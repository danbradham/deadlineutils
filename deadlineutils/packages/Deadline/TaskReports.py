from ConnectionProperty import ConnectionProperty

class TaskReports:
    """
        Class used by DeadlineCon to send Task Reports requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties

    def GetAllTaskReports(self, jobId, taskId):
        """ Gets all types of reports for a single task within a job
            Input:  jobId: The job id
                    taskId: The task id
            Returns: The task reports
        """
        return self.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(taskId)+"&Data=all")

    def GetTaskErrorReports(self, jobId, taskId):
        """ Gets all error reports for a single task within a job
            Input:  jobId: The job id
                    taskId: The task id
            Returns: The task error reports
        """    
        return self.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(taskId)+"&Data=error")

    def GetTaskLogReports(self, jobId, taskId):
        """ Gets all log reports for a single task within a job
            Input:  jobId: The job id
                    taskId: The task id
            Returns: The log reports
        """    
        return self.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(taskId)+"&Data=log")

    def GetTaskRequeueReports(self, jobId, taskId):
        """ Gets all requeue reports for a single task within a job
            Input:  jobId: The job id
                    taskId: The task id
            Returns: The requeue reports
        """        
        return self.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(taskId)+"&Data=requeue")
        
    def GetAllTaskReportsContents(self, jobId, taskId):
        """ Gets the contents for all types of reports for a single task within a job
            Input:  jobId: The job id
                    taskId: The task id
            Returns: The task reports contents
        """
        return self.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(taskId)+"&Data=allcontents")

    def GetAllTaskErrorReportsContents(self, jobId, taskId):
        """ Gets all error reports contents for a single task within a job
            Input:  jobId: The job id
                    taskId: The task id
            Returns: The task error reports contents
        """    
        return self.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(taskId)+"&Data=allerrorcontents")

    def GetAllTaskLogReportsContents(self, jobId, taskId):
        """ Gets all log reports contents for a single task within a job
            Input:  jobId: The job id
                    taskId: The task id
            Returns: The log reports contents
        """    
        return self.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(taskId)+"&Data=alllogcontents")

    def GetAllTaskRequeueReportsContents(self, jobId, taskId):
        """ Gets all requeue reports contents for a single task within a job
            Input:  jobId: The job id
                    taskId: The task id
            Returns: The requeue reports contents
        """        
        return self.connectionProperties.__get__("/api/taskreports?JobID="+jobId+"&TaskID="+str(taskId)+"&Data=allrequeuecontents")
    