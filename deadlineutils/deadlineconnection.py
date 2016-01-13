# -*- coding: utf-8 -*-
'''
deadlineutils.deadlineconnection
================================
'''

from __future__ import print_function
import os
import getpass
from collections import Counter

try:
    from Deadline import DeadlineConnect
except ImportError:
    from .packages.Deadline import DeadlineConnect
except ImportError:
    print('Failed to import Deadline Standalone API')
    raise


class DeadlineConnection(object):
    '''
    Wraps Deadline.DeadlineConnect.DeadlineCon providing additional
    functionality. Can be used as a ContextManager::

        with DeadlineConnection('localhost', 8080) as c:
            best_pool = c.get_best_pool(prefix='maya')

    Here we get the best possible pool for the next job submission with the
    prefix *maya*.

    see also::

        *Deadline Standalone Python API*

    '''

    def __init__(self, addr, port):
        self._connection = DeadlineConnect.DeadlineCon(addr, port)

    def __getattr__(self, attr):
        return getattr(self._connection, attr)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return False

    def get_active_jobs(self):
        '''
        Get a list of jobs that are currently rendering

        :param connection: DeadlineConnect.DeadlineCon instance
        '''

        job_ids = []

        slave_infos = self.Slaves.GetSlaveInfos()
        for info in slave_infos:
            if info['JobId']:
                job_ids.append(info['JobId'])

        return job_ids

    def get_jobs_with_status(self, *statuses):
        '''
        Get a list of jobs in the database with a specific status/es

        Available Statuses: queued, active, suspended, completed, failed

        :param statuses: Unpacked list of statuses
        '''

        status_to_stat = {
            'queued': 0,
            'active': 1,
            'suspended': 2,
            'completed': 3,
            'failed': 4,
        }

        stats = [status_to_stat[status] for status in statuses]
        all_jobs = self.Jobs.GetJobs()
        return [job for job in all_jobs if job['Stat'] in stats]

    def get_used_pools(self):
        '''
        Get a list of pools currently assigned to queued and active jobs
        '''

        used_pools = []

        jobs = self.get_jobs_with_status('queued', 'active')
        for job in jobs:
            used_pools.append(job['Props']['Pool'])

        return used_pools

    def get_pools(self):
        '''
        Get a list of all availabled pools
        '''

        return self.Pools.GetPoolNames()

    def get_pools_usage_count(self):
        '''
        Get a dictionary containing the number of active and queued jobs using
        each pool
        '''

        pools = Counter({pool: 0 for pool in self.get_pools()})
        pools.update(self.get_used_pools())
        return pools

    def get_best_pool(self, prefix=None):
        '''
        Get the best pool with a name prefixed by prefix. *Best* being, the
        pool used the least among queued and active jobs.
        '''

        pools = self.get_pools_usage_count()

        if prefix:  # find least common starting with prefix
            for pool, _ in pools.most_common()[::-1]:
                if pool.startswith(prefix) and pool != prefix:
                    return pool

        return pools.most_common()[-1][0]

    def submit_job(self, job_info, plugin_info, pool=None, second_pool=None):
        '''
        Submit a new job to deadline.

        see also::

            *Deadline.Jobs.SubmitJob*

        :param job_info: Job information Dictionary
        :param plugin_info: Plugin info dictionary
        '''

        if pool:
            job_info['Pool'] = pool
        if second_pool:
            job_info['SecondaryPool'] = second_pool
        self.Jobs.SubmitJob(job_info, plugin_info)

    def maya_submit_job(self, render_path, render_prefix, render_layers,
                        pool=None, second_pool=None):
        '''
        Submit a maya render job to deadline...

        :param render_path: output directory for the rendered images
        :param render_prefix: filename prefix for rendered images
        '''

        info_cache = {}

        for layer in render_layers:

            print('Submiting {} to Deadline...'.format(layer), end='')

            job_info, plugin_info = maya_info(
                render_path,
                render_prefix,
                layer,
                cache=info_cache,
            )

            try:
                self.submit_job(
                    job_info,
                    plugin_info,
                    pool,
                    second_pool
                )
            except Exception, e:
                print('Failed.')
                print(e)
                raise
            else:
                print('Success!')


def maya_info(render_path, render_prefix, render_layer, cache=None):
    '''
    Get job_info and plugin_info to use with DeadlineConnection.submit_job
    '''

    from maya import cmds

    if not cache:
        # We don't want to get this information for each render layer
        # so we store it in a cache dictionary
        if cache is None:
            cache = {}

        scene_path = os.path.abspath(cmds.file(query=True, sn=True))
        scene_name = os.path.basename(scene_path)
        start_frame = int(cmds.getAttr('defaultRenderGlobals.startFrame'))
        end_frame = int(cmds.getAttr('defaultRenderGlobals.endFrame'))
        image_width = cmds.getAttr('defaultResolution.width')
        image_height = cmds.getAttr('defaultResolution.height')
        version = cmds.about(version=True)
        renderer = cmds.getAttr('defaultRenderGlobals.ren')
        project_path = cmds.workspace(q=True, rootDirectory=True)

        cache.update({
            'job_info': {
                'BatchName': scene_name,
                'UserName': getpass.getuser(),
                'Frames': '-'.join([str(start_frame), str(end_frame)]),
                'Plugin': 'MayaCmd',
                'OutputDirectory0': render_path,
            },
            'plugin_info': {
                'Animation': 1,
                'Renderer': renderer,
                'UsingRenderLayers': 1,
                'RenderHalfFrames': 0,
                'FrameNumberOffset': 0,
                'LocalRendering': 0,
                'StrictErrorChecking': 0,
                'MaxProcessors': 0,
                'Version': version,
                'Build': '64bit',
                'ProjectPath': project_path,
                'CommandLineOptions': '',
                'ImageWidth': image_width,
                'ImageHeight': image_height,
                'OutputFilePath': render_path,
                'OutputFilePrefix': render_prefix,
                'IgnoreErrorCode211': 1,
                'SceneFile': scene_path,
            }
        })

    # General Scene/Deadline Info
    job_info = dict(cache['job_info'])
    plugin_info = dict(cache['plugin_info'])

    # Render Layer Specific Info
    job_info['Name'] = ' - '.join([job_info['BatchName'], render_layer])
    plugin_info['RenderLayer'] = render_layer

    # Renderer Specific Info
    try:
        renderer_info = {
            'arnold': {
                'ArnoldVerbose': 1,
            },
            'vray': {},
        }[plugin_info['renderer']]
    except KeyError:
        pass
    else:
        plugin_info.update(renderer_info)

    return job_info, plugin_info
