"""Provide a Timeline service class for novelibre.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os
from pathlib import Path
from tkinter import filedialog

from nvlib.controller.services.service_base import ServiceBase
from nvlib.model.file.doc_open import open_document
from nvlib.novx_globals import norm_path
from nvtimeline.nvtimeline_locale import _
from nvtimeline.tl_file import TlFile


class TlService(ServiceBase):
    INI_FILENAME = 'nv_timeline.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        section_label='Section',
        section_color='170,240,160',
        new_event_spacing='1'
    )
    OPTIONS = dict(
        lock_on_export=False,
    )

    def __init__(self, model, view, controller, windowTitle):
        super().__init__(model, view, controller)
        self.windowTitle = windowTitle

    def create_novx(self):
        """Create a novelibre project from a timeline."""
        self._ui.restore_status()
        timelinePath = filedialog.askopenfilename(
            filetypes=[(TlFile.DESCRIPTION, TlFile.EXTENSION)],
            defaultextension=TlFile.EXTENSION,
            )
        if not timelinePath:
            return

        if not self._ctrl.close_project():
            return

        root, __ = os.path.splitext(timelinePath)
        novxPath = f'{root}{self._mdl.nvService.get_novx_file_extension()}'
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = TlFile(timelinePath, **kwargs)
        target = self._mdl.nvService.new_novx_file(novxPath)

        if os.path.isfile(target.filePath):
            self._ui.set_status(
                f'!{_("File already exists")}: "{norm_path(target.filePath)}".'
            )
            return

        statusMsg = ''
        try:
            source.novel = self._mdl.nvService.new_novel()
            source.read()
            target.novel = source.novel
            target.write()
        except RuntimeError as ex:
            statusMsg = f'!{str(ex)}'
        else:
            self._ctrl.fileManager.copy_to_backup(target.filePath)
            statusMsg = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=target.filePath, doNotSave=True)
        finally:
            self._ui.set_status(statusMsg)

    def export_from_novx(self):
        """Update or create a timeline from the novelibre project."""
        self._ui.restore_status()
        if not self._mdl.prjFile:
            return

        self._ui.propertiesView.apply_changes()
        self._ui.restore_status()
        if not self._mdl.prjFile.filePath:
            if not self._ctrl.save_project():
                return

        timelinePath = (
            f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}'
            f'{TlFile.EXTENSION}'
        )
        if os.path.isfile(timelinePath):
            action = _('update')
        else:
            action = _('create')
        if self._mdl.isModified:
            if not self._ui.ask_yes_no(
                _('Save the project and {} the timeline?').format(action),
                detail=f"{_('There are unsaved changes')}.",
                title=self.windowTitle
                ):
                return

            self._ctrl.save_project()
        elif action == _('update') and not self._ui.ask_yes_no(
            _('Update the timeline?'),
            title=self.windowTitle
            ):
            return

        kwargs = self._get_configuration(self._mdl.prjFile.filePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = self._mdl.nvService.new_novx_file(self._mdl.prjFile.filePath)
        source.novel = self._mdl.nvService.new_novel()
        target = TlFile(timelinePath, **kwargs)
        target.novel = self._mdl.nvService.new_novel()
        try:
            source.read()
            if os.path.isfile(target.filePath):
                target.read()
            target.write(source.novel)
            self._ctrl.fileManager.copy_to_backup(target.filePath)
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
        except RuntimeError as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(message)

    def import_to_novx(self):
        """Update the novelibre project from a timeline."""
        self._ui.restore_status()
        if not self._mdl.prjFile:
            return

        timelinePath = (
            f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}'
            f'{TlFile.EXTENSION}'
        )
        if not os.path.isfile(timelinePath):
            self._ui.set_status(
                _('!No {} file available for this project.').format(
                    self.windowTitle))
            return

        if not self._ui.ask_yes_no(
            _('Save the project and update it?'),
            title=self.windowTitle
            ):
            return

        self._ctrl.save_project()
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = TlFile(timelinePath, **kwargs)
        target = self._mdl.nvService.new_novx_file(
            self._mdl.prjFile.filePath,
            **kwargs
        )
        message = ''
        try:
            target.novel = self._mdl.nvService.new_novel()
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
            self._ctrl.fileManager.copy_to_backup(target.filePath)
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(
                filePath=self._mdl.prjFile.filePath,
                doNotSave=True,
            )
        except RuntimeError as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(f'{message}')

    def info(self):
        """Show information about the Timeline file."""
        if not self._mdl.prjFile:
            return

        timelinePath = (
            f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}'
            f'{TlFile.EXTENSION}'
        )
        if os.path.isfile(timelinePath):
            try:
                timestamp = os.path.getmtime(timelinePath)
                if timestamp > self._mdl.prjFile.timestamp:
                    cmp = _('newer')
                else:
                    cmp = _('older')
                fileDate = datetime.fromtimestamp(timestamp).strftime('%c')
                tlInfo = _('{0} file is {1} than the novelibre project.\n (last saved on {2})').format(
                    self.windowTitle,
                    cmp,
                    fileDate
                )
            except:
                tlInfo = _('Cannot determine file date.')
        else:
            tlInfo = _('No {} file available for this project.').format(
                self.windowTitle
            )
        self._ui.show_info(
            message=self.windowTitle,
            detail=tlInfo,
            title=_('Information')
            )

    def launch_application(self):
        """Launch Timeline with the current project."""
        self._ui.restore_status()
        if not self._mdl.prjFile:
            return

        timelinePath = (
            f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}'
            f'{TlFile.EXTENSION}'
        )
        prefs = self._get_configuration(timelinePath)
        if os.path.isfile(timelinePath):
            if prefs['lock_on_export']:
                self._ctrl.lock()
            try:
                open_document(timelinePath)
            except Exception as ex:
                self._ui.set_status(f'!{str(ex)}')
        else:
            self._ui.set_status(
                _('!No {} file available for this project.').format(
                    self.windowTitle
                )
            )

    def _get_configuration(self, sourcePath):
        """Return a dictionary with persistent configuration data."""
        sourceDir = os.path.dirname(sourcePath)
        if not sourceDir:
            sourceDir = '.'
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            pluginCnfDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            pluginCnfDir = '.'
        iniFiles = [
            f'{pluginCnfDir}/{self.INI_FILENAME}',
            f'{sourceDir}/{self.INI_FILENAME}',
        ]
        configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        for iniFile in iniFiles:
            configuration.read(iniFile)
        configData = {}
        configData.update(configuration.settings)
        configData.update(configuration.options)
        return configData

