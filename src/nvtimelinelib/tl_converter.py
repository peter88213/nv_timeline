"""Provide a converter class for test_nv_timeline.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv-timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from novxlib.converter.converter import Converter
from novxlib.model.novel import Novel
from novxlib.model.nv_tree import NvTree
from novxlib.novx.novx_file import NovxFile
from novxlib.novx_globals import _
from novxlib.novx_globals import norm_path
from nvtimelinelib.tl_file import TlFile
from novxlib.novx_globals import Error


class TlConverter(Converter):
    """A converter class for noveltree and Timeline."""

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath: str -- the source file path.

        The direction of the conversion is determined by the source file type.
        Only noveltree project files and Timeline files are accepted.
        """
        self.newFile = None
        if not os.path.isfile(sourcePath):
            self.ui.set_status(f'!{_("File not found")}: "{norm_path(sourcePath)}".')
            return

        fileName, fileExtension = os.path.splitext(sourcePath)
        if fileExtension == TlFile.EXTENSION:
            # Source is a timeline
            sourceFile = TlFile(sourcePath, **kwargs)
            targetFile = NovxFile(f'{fileName}{NovxFile.EXTENSION}', **kwargs)
            if os.path.isfile(f'{fileName}{NovxFile.EXTENSION}'):
                # Update existing noveltree project from timeline
                self.import_to_novx(sourceFile, targetFile)
            else:
                # Create new noveltree project from timeline
                self.create_novx(sourceFile, targetFile)
        elif fileExtension == NovxFile.EXTENSION:
            # Update existing timeline from noveltree project
            sourceFile = NovxFile(sourcePath, **kwargs)
            targetFile = TlFile(f'{fileName}{TlFile.EXTENSION}', **kwargs)
            self.export_from_novx(sourceFile, targetFile)
        else:
            # Source file format is not supported
            self.ui.set_status(f'!{_("File type is not supported")}: "{norm_path(sourcePath)}".')

    def export_from_novx(self, source, target):
        """Convert from noveltree project to other file format.

        Positional arguments:
            source -- NovxFile subclass instance.
            target -- Any Novel subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the message to the UI.
        4. Save the new file pathname.

        Error handling:
        - If the conversion fails, newFile is set to None.
        
        Overrides the superclass method.
        """
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(source.DESCRIPTION, norm_path(source.filePath), target.DESCRIPTION, norm_path(target.filePath)))
        message = ''
        try:
            self.check(source, target)
            source.novel = Novel(tree=NvTree())
            target.novel = Novel(tree=NvTree())
            source.read()
            if os.path.isfile(target.filePath):
                target.read()
            target.write(source.novel)
        except Error as ex:
            message = f'!{str(ex)}'
            self.newFile = None
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
        finally:
            self.ui.set_status(message)

