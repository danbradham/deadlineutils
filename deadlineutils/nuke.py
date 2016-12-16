'''
deadlineutils.nuke
==================
Provides two methods, submit_job and get_job_info
'''
from __future__ import absolute_import, print_function
import os
import getpass
import re


def submit_job(connection, write_nodes, pool=None, second_pool=None, **kwargs):
    '''
    Submit a nuke render job to deadline...

    :param connection: deadlineutils.connection.Connection instance
    :param render_path: output directory for the rendered images
    :param render_prefix: filename prefix for rendered images
    :param write_nodes: List of write nodes to submit
    :param pool: Primary pool
    :param second_pool: Secondary pool
    :param kwargs: job_info/plugin_info key overrides
    '''

    for write_node in write_nodes:

        name = write_node.fullName()
        print('Submiting {} to Deadline...'.format(name), end='')

        job_info, plugin_info = get_job_info(write_node)

        try:
            connection.submit_job(
                job_info,
                plugin_info,
                pool,
                second_pool
            )
        except Exception, e:
            print('Failed.')
            raise e
        else:
            print('Success!')


def _get_frame_range(write_node):
    '''Get frame range from write node. Either nodes limit or input range...'''

    limit = write_node['use_limit'].getValue()
    if limit:
        first = write_node['first'].getValue()
        last = write_node['last'].getValue()
        return '{}-{}'.format(first, last)

    return str(write_node.frameRange())


def _replace_padding_with_hashes(basename):
    '''Replace printf frame padding formatter with hashes...'''

    if '%0' in basename:
        start, end = basename.split('%0')
        return start + ('#' * int(end[0])) + end[2:]
    return basename


def get_job_info(write_node, **kwargs):
    '''
    Get nuke job and plugin info for deadline submission...

    :param render_path: output directory for the rendered images
    :param render_prefix: filename prefix for rendered images
    :param write_node: Write node
    :param kwargs: job_info/plugin_info key overrides
    '''

    try:
        import nuke
    except ImportError:
        msg = (
            '[deadline.nuke.get_job_info] unable to retrieve job info:\n'
            '    nuke module unavailable in current python context.\n'
        )
        raise Exception(msg)

    if write_node['disable'].getValue():
        msg = (
            'deadline.nuke.get_job_info unable to submit write node:\n'
            '    {} is disabled\n'
        ).format(write_node.fullName())
        raise Exception(msg)

    script = os.path.basename(nuke.scriptName())
    frames = _get_frame_range(write_node)
    filepath = write_node['file'].getValue()
    filepath = nuke.callbacks.filenameFilter(filepath)
    dirname, basename = os.path.split(filepath)
    basename = _replace_padding_with_hashes(basename)

    job_info = {
        'BatchName': script,
        'Name': script + ' - ' + write_node.fullName(),
        'UserName': getpass.getuser(),
        'Plugin': kwargs.get('Plugin', 'Nuke'),
        'OutputDirectory0': dirname,
        'OutputFilename0': basename,
        'Frames': frames,
        'ChunkSize': kwargs.get('ChunkSize', 10),
    }

    plugin_info = {
        'Version': nuke.NUKE_VERSION_STRING.split('v')[0],
        'NukeX': kwargs.get('NukeX', False),
        'UseGpu': kwargs.get('UseGpu', False),
        'RenderMode': 'Use Scene Settings',
        'ContinueOnError': kwargs.get('ContinueOnError', True),
        'BatchMode': kwargs.get('BatchMode', True),
        'BatchModeIsMovie': kwargs.get('BatchModeIsMovie', False),
        'WriteNode': write_node.fullName(),
        'Threads': kwargs.get('Threads', 0),
        'RamUse': kwargs.get('RamUse', 0),
        'EnforceRenderOrder': kwargs.get('EnforceRenderOrder', False),
        'Views': kwargs.get('Views', ''),
        'StackSize': kwargs.get('StackSize', 0),
        'PerformanceProfiler': kwargs.get('PerformanceProfiler', False),
        'PerformanceProfilerDir': kwargs.get('PerformanceProfilerDir', '')
    }

    return job_info, plugin_info
