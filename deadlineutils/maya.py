'''
deadlineutils.maya
==================
Provides two methods, submit_job and get_job_info
'''
from __future__ import absolute_import, print_function
import os
import getpass


def submit_job(connection, render_path, render_prefix, render_layers,
               pool=None, second_pool=None):
    '''
    Submit a maya render job to deadline...

    :param connection: deadlineutils.connection.Connection instance
    :param render_path: output directory for the rendered images
    :param render_prefix: filename prefix for rendered images
    :param render_layers: List of render layers to submit
    :param pool: Primary pool
    :param second_pool: Secondary pool
    '''

    info_cache = {}

    for layer in render_layers:

        print('Submiting {} to Deadline...'.format(layer), end='')

        job_info, plugin_info = get_job_info(
            render_path,
            render_prefix,
            layer,
            cache=info_cache,
        )

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


def get_job_info(render_path, render_prefix, render_layer, cache=None):
    '''
    Get job_info and plugin_info to use with Connection.submit_job

    :param render_path: output directory for the rendered images
    :param render_prefix: filename prefix for rendered images
    :param render_layer: Render layer
    :param cache: Job/plugin info defaults
    '''

    try:
        from maya import cmds
    except ImportError:
        msg = (
            '[deadline.maya.get_job_info] unable to retrieve job info:\n'
            '    maya.cmds module unavailable in current python context.\n'
        )
        raise Exception(msg)

    if not cache:
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
                'Plugin': 'MayaBatch',
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
