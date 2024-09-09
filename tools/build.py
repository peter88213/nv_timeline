"""Build the nv_timeline novelibre plugin package.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the novxlib package.

The novxlib project (see see https://github.com/peter88213/novxlib)
must be located on the same directory level as the nv_timeline project. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

sys.path.insert(0, f'{os.getcwd()}/../../novelibre/tools')
from package_builder import PackageBuilder

VERSION = '4.3.3'


class PluginBuilder(PackageBuilder):

    PRJ_NAME = 'nv_timeline'
    LOCAL_LIB = 'nvtimelinelib'
    GERMAN_TRANSLATION = True

    def __init__(self, version):
        super().__init__(version)
        self.sampleTarget = f'{self.buildDir}/{self.PRJ_NAME}_sample'

    def add_extras(self):
        self.add_sample()
        self.add_icons()


def main():
    pb = PluginBuilder(VERSION)
    pb.run()


if __name__ == '__main__':
    main()
