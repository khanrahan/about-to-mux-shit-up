"""
Script Name: About to Mux Shit Up
Written By: Kieran Hanrahan

Script Version: 0.1.0
Flame Version: 2022

URL: http://github.com/khanrahan/about-to-mux-shit-up

Creation Date: 02.22.24
Update Date: 02.22.24

Description:

    Attach Mux nodes to the output sockets of the selected Clip nodes in Batch.

Menus:

    Right-click selected Clip nodes in the Batch schematic --> Create... -->
    About to Mux Shit Up

To Install:

    For all users, copy this file to:
    /opt/Autodesk/shared/python

    For a specific user, copy this file to:
    /opt/Autodesk/user/<user name>/python
"""

import flame

TITLE = 'About to Mux Shit Up'
VERSION_INFO = (0, 1, 0)
VERSION = '.'.join([str(num) for num in VERSION_INFO])
TITLE_VERSION = '{} v{}'.format(TITLE, VERSION)
MESSAGE_PREFIX = '[PYTHON]'

NODE_SPACING = (400, 140)


def message(string):
    """Print message to shell window and append global MESSAGE_PREFIX."""
    print(' '.join([MESSAGE_PREFIX, string]))



def mux_shit_up(selection):
    """Process all selected nodes."""
    message(TITLE_VERSION)
    message('Script called from {}'.format(__file__))

    for node in selection:
        node_position = (node.pos_x.get_value(), node.pos_y.get_value())
        sockets = node.output_sockets

        for number, socket in enumerate(sockets):
            if number > 0:
                if all((socket.startswith(sockets[number - 1]),
                        socket.endswith('_alpha'))):
                    flame.batch.connect_nodes(node, socket, mux, 'Matte_0')
                    continue

            mux = flame.batch.create_node('Mux')
            mux.name.set_value('_'.join((node.name.get_value(), socket)))
            mux.pos_x.set_value(node_position[0] + NODE_SPACING[0])
            mux.pos_y.set_value(node_position[1] - NODE_SPACING[1] * number)
            flame.batch.connect_nodes(node, socket, mux, 'Input_0')

    message('Done!')


def scope_clip_node(selection):
    """Filter for only PyClipNode objects."""
    return all(isinstance(item, flame.PyClipNode) for item in selection)


def get_batch_custom_ui_actions():
    """Python hook to add custom item to right click menu in Batch."""
    return [{'name': 'Create...',
             'actions': [{'name': 'About to Mux Shit Up',
                          'isVisible': scope_clip_node,
                          'execute': mux_shit_up,
                          'minimumVersion': '2022'}]
            }]
