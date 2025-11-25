#!/usr/bin/python3
"""Synchronize novelibre project with Timeline

Version @release
Requires Python 3.7+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import argparse
import os
from pathlib import Path

from nvlib.configuration.configuration import Configuration
from nvlib.gui.set_icon_tk import set_icon
from nvlib.alternative_ui.ui import Ui
from nvlib.alternative_ui.ui_tk import UiTk
from nvtimeline.nvtimeline_locale import _
from standalone.tl_converter import TlConverter

SUFFIX = ''
APPNAME = 'nv_timeline'
SETTINGS = dict(
    section_label='Section',
    section_color='170,240,160',
    new_event_spacing='1'
)
OPTIONS = dict(
    lock_on_export=False,
)


def run(sourcePath, silentMode=True, installDir='.'):
    if silentMode:
        ui = Ui('')
    else:
        ui = UiTk(f'{_("Synchronize Timeline and novelibre")} @release')
        set_icon(ui.root, icon='tlview')

    #--- Try to get persistent configuration data
    sourceDir = os.path.dirname(sourcePath)
    if not sourceDir:
        sourceDir = '.'
    iniFileName = f'{APPNAME}.ini'
    iniFiles = [
        f'{installDir}/{iniFileName}',
        f'{sourceDir}/{iniFileName}'
    ]
    configuration = Configuration(SETTINGS, OPTIONS)
    for iniFile in iniFiles:
        configuration.read(iniFile)
    kwargs = {'suffix': SUFFIX}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)
    converter = TlConverter()
    converter.ui = ui
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Synchronize novelibre with Timeline',
        epilog='')
    parser.add_argument(
        'sourcePath',
        metavar='Sourcefile',
        help='The path of the novelibre/Timeline project file.'
    )
    parser.add_argument(
        '--silent',
        action="store_true",
        help='suppress error messages and the request to confirm overwriting'
    )
    args = parser.parse_args()
    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.novx/config'
    except:
        installDir = '.'
    run(args.sourcePath, args.silent, installDir)
