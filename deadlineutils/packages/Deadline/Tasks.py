from ConnectionProperty import ConnectionProperty
import json

class Tasks:
    """
        Class used by DeadlineCon to send Task requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties

    def GetJobTaskIds(self, id):
        """ Gets the ids of the job's tasks.
            Input:  id: The job id
            Returns: The list of IDs.
        """
        return self.connectionProperties.__get__("/api/tasks?JobID="+id+"&IdOnly=true")

    def GetJobTasks(self, id):
        """    Gets the tasks for a job.
            Input:  id: The job ID
            Returns: The job's task collection.
        """
        return self.connectionProperties.__get__("/api/tasks?JobID="+id)

    def GetJobTask(self, jobId, taskId):
        """    Gets a specific job task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: The job's task.
        """
        
        result = self.connectionProperties.__get__("/api/tasks?JobID="+jobId+"&TaskID="+str(taskId))
        
        if type(result) == list and len(result) > 0:
            result = result[0]
        
        return result

    def RequeueJobTask(self, jobId, taskId):
        """ Requeues a task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: Success message
        """
        
        task = str(taskId)
        
        body = '{"Command":"requeue", "JobID":"'+jobId+'", "TaskList":'+task+'}'
        
        return self.connectionProperties.__put__("/api/tasks", body)

    def RequeueJobTasks(self, jobId, taskIds = None):
        """ Requeues multiple tasks for a single job.
            Input:  jobId: The job ID
                    taskIds: the list of task ID, if not supplied requeues all tasks for the job
            Returns: Success message
        """
        
        if taskIds is not None:
            
            body = json.dumps({"Command":"requeue", "JobID":jobId, "TaskList":taskIds})
            
        else:
            body = '{"Command":"requeue","JobID":"'+jobId+'"}'
            
        return self.connectionProperties.__put__("/api/tasks", body)
        
        
    def CompleteJobTask(self, jobId, taskId):
        """ Complete a task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: Success message
        """
        body = '{"Command":"complete", "JobID":"'+jobId+'", "TaskList":'+str(taskId)+'}'
        
        return self.connectionProperties.__put__("/api/tasks", body)       

    def CompleteJobTasks(self, jobId, taskIds = None):
        """ Complete multiple tasks for a single job.
            Input:  jobId: The job ID
                    taskIds: the list of task ID
            Returns: Success message
        """
        if taskIds is not None:
            
            body = json.dumps({"Command":"complete", "JobID":jobId, "TaskList":taskIds})
            
        else:
            body = '{"Command":"complete","JobID":"'+jobId+'"}'
            
        return self.connectionProperties.__put__("/api/tasks", body)    

    def ResumeJobTask(self, jobId, taskId):
        """ Resume a suspended task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: Success message
        """
        body = '{"Command":"resume", "JobID":"'+jobId+'", "TaskList":'+str(taskId)+'}'
        
        return self.connectionProperties.__put__("/api/tasks", body)             

    def ResumeJobTasks(self, jobId, taskIds = None):
        """ Resume multiple suspended tasks for a single job.
            Input:  jobId: The job ID
                    taskIds: the list of task ID
            Returns: Success message
        """
        if taskIds is not None:
            
            body = json.dumps({"Command":"resume", "JobID":jobId, "TaskList":taskIds})
            
        else:
            body = '{"Command":"resume","JobID":"'+jobId+'"}'
            
        return self.connectionProperties.__put__("/api/tasks", body)   

    def SuspendJobTask(self, jobId, taskId):
        """ Suspend a task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: Success message
        """
        body = '{"Command":"suspend", "JobID":"'+jobId+'", "TaskList":'+str(taskId)+'}'
        
        return self.connectionProperties.__put__("/api/tasks", body)             

    def SuspendJobTasks(self, jobId, taskIds = None):
        """ Suspend multiple tasks for a single job.
            Input:  jobId: The job ID
                    taskIds: the list of task ID
            Returns: Success message
        """
        if taskIds is not None:
            
            body = json.dumps({"Command":"suspend", "JobID":jobId, "TaskList":taskIds})
            
        else:
            body = '{"Command":"suspend","JobID":"'+jobId+'"}'
            
        return self.connectionProperties.__put__("/api/tasks", body)   

    def FailJobTask(self, jobId, taskId):
        """ Fail a task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: Success message
        """
        body = '{"Command":"fail", "JobID":"'+jobId+'", "TaskList":'+str(taskId)+'}'
        
        return self.connectionProperties.__put__("/api/tasks", body)             

    def FailJobTasks(self, jobId, taskIds = None):
        """ Fail multiple tasks for a single job.
            Input:  jobId: The job ID
                    taskIds: the list of task ID
            Returns: Success message
        """
        if taskIds is not None:
            
            body = json.dumps({"Command":"fail", "JobID":jobId, "TaskList":taskIds})
            
        else:
            body = '{"Command":"fail","JobID":"'+jobId+'"}'
            
        return self.connectionProperties.__put__("/api/tasks", body)   

    def ResumeFailedJobTask(self, jobId, taskId):
        """ Resume a failed task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: Success message
        """
        body = '{"Command":"resumefailed", "JobID":"'+jobId+'", "TaskList":'+str(taskId)+'}'
        
        return self.connectionProperties.__put__("/api/tasks", body)         

    def ResumeFailedJobTasks(self, jobId, taskIds):
        """ Resume multiple failed tasks for a single job.
            Input:  jobId: The job ID
                    taskIds: the list of task ID
            Returns: Success message
        """
        if taskIds is not None:
            
            body = json.dumps({"Command":"resumefailed", "JobID":jobId, "TaskList":taskIds})
            
        else:
            body = '{"Command":"resumefailed","JobID":"'+jobId+'"}'
            
        return self.connectionProperties.__put__("/api/tasks", body)       

    def PendJobTask(self, jobId, taskId):
        """ Pend a task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: Success message
        """
        body = '{"Command":"pend", "JobID":"'+jobId+'", "TaskList":'+str(taskId)+'}'
        
        return self.connectionProperties.__put__("/api/tasks", body)         

    def PendJobTasks(self, jobId, taskIds):
        """ Pend multiple tasks for a single job.
            Input:  jobId: The job ID
                    taskIds: the task ID
            Returns: Success message
        """
        if taskIds is not None:
            
            body = json.dumps({"Command":"pend", "JobID":jobId, "TaskList":taskIds})
            
        else:
            body = '{"Command":"pend","JobID":"'+jobId+'"}'
            
        return self.connectionProperties.__put__("/api/tasks", body)

    def ReleasePendingJobTask(self, jobId, taskId):
        """ Release a pending task.
            Input:  jobId: The job ID
                    taskId: the task ID
            Returns: Success message
        """
        body = '{"Command":"releasepending", "JobID":"'+jobId+'", "TaskList":'+str(taskId)+'}'
        
        return self.connectionProperties.__put__("/api/tasks", body)        

    def ReleasePendingJobTasks(self, jobId, taskIds):
        """ Release multiple pending tasks for a single job.
            Input:  jobId: The job ID
                    taskIds: the task ID
            Returns: Success message
        """
        if taskIds is not None:
            
            body = json.dumps({"Command":"releasepending", "JobID":jobId, "TaskList":taskIds})
            
        else:
            body = '{"Command":"releasepending","JobID":"'+jobId+'"}'
            
        return self.connectionProperties.__put__("/api/tasks", body)