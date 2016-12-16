=============
deadlineutils
=============
Deadline Standalone API utilities


Connection
==================
Wraps ``Deadline.DeadlineConnect.DeadlineCon`` providing additional
functionality. Can be used as a ContextManager::

    with Connection('localhost', 8080) as c:
        best_pool = c.get_best_pool(prefix='maya')

Here we get the best possible pool for the next job submission with the
prefix *maya*.

.. see also::

    `Deadline Standalone Python API<http://docs.thinkboxsoftware.com/products/deadline/7.2/3_Python%20Reference/class_deadline_connect_1_1_deadline_con.html>`_

