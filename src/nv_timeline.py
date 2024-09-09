"""Timeline sync plugin for novelibre.

Version @release
Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from datetime import datetime
import os
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

from nvtimelinelib.nvtimeline_globals import _
from novxlib.file.doc_open import open_document
from novxlib.novx_globals import Error
from novxlib.novx_globals import norm_path
from nvlib.plugin.plugin_base import PluginBase
from nvtimelinelib.tl_button import TlButton
from nvtimelinelib.tl_file import TlFile
import tkinter as tk

APPLICATION = 'Timeline'
PLUGIN = f'{APPLICATION} plugin v@release'
INI_FILENAME = 'nv_timeline.ini'
INI_FILEPATH = '.novx/config'


class Plugin(PluginBase):
    """Plugin class for synchronization with Timeline."""
    VERSION = '@release'
    API_VERSION = '4.3'
    DESCRIPTION = 'Synchronize with Timeline'
    URL = 'https://github.com/peter88213/nv_timeline'
    _HELP_URL = f'https://peter88213.github.io/{_("nvhelp-en")}/nv_timeline/'

    SETTINGS = dict(
        section_label='Section',
        section_color='170,240,160',
        new_event_spacing='1'
    )
    OPTIONS = dict(
        lock_on_export=False,
    )

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        self._timelineButton.disable()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')
        self._timelineButton.enable()

    def install(self, model, view, controller, prefs=None):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Overrides the superclass method.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        # Create a submenu in the Tools menu.
        self._pluginMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._ui.toolsMenu.add_cascade(label=APPLICATION, menu=self._pluginMenu)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')
        self._pluginMenu.add_command(label=_('Information'), command=self._info)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Create or update the timeline'), command=self._export_from_novx)
        self._pluginMenu.add_command(label=_('Update the project'), command=self._import_to_novx)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Open Timeline'), command=self._launch_application)

        # Add an entry to the "File > New" menu.
        self._ui.newMenu.add_command(label=_('Create from Timeline...'), command=self._create_novx)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Timeline plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

        #--- Configure the toolbar.

        # Get the icons.
        prefs = controller.get_preferences()
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            iconPath = f'{homeDir}/.novx/icons/{size}'
        except:
            iconPath = None
        try:
            tlIcon = tk.PhotoImage(file=f'{iconPath}/tl.png')
        except:
            tlIcon = None

        # Put a Separator on the toolbar.
        tk.Frame(view.toolbar.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # Initialize the operation.
        self._timelineButton = TlButton(view, _('Open Timeline'), tlIcon, self._launch_application)

    def lock(self):
        """Inhibit changes on the model.
        
        Overrides the superclass method.
        """
        self._pluginMenu.entryconfig(_('Update the project'), state='disabled')

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        self._pluginMenu.entryconfig(_('Update the project'), state='normal')

    def _create_novx(self):
        """Create a novelibre project from a timeline."""
        timelinePath = filedialog.askopenfilename(
            filetypes=[(TlFile.DESCRIPTION, TlFile.EXTENSION)],
            defaultextension=TlFile.EXTENSION,
            )
        if not timelinePath:
            return

        self._ctrl.close_project()
        root, __ = os.path.splitext(timelinePath)
        novxPath = f'{root}{self._mdl.nvService.get_novx_file_extension()}'
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = TlFile(timelinePath, **kwargs)
        target = self._mdl.nvService.make_novx_file(novxPath)

        if os.path.isfile(target.filePath):
            self._ui.set_status(f'!{_("File already exists")}: "{norm_path(target.filePath)}".')
            return

        message = ''
        try:
            source.novel = self._mdl.nvService.make_novel()
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=target.filePath, doNotSave=True)
        finally:
            self._ui.set_status(message)

    def _export_from_novx(self):
        """Update or create a timeline from the novelibre project."""
        if not self._mdl.prjFile:
            return

        self._ui.propertiesView.apply_changes()
        self._ui.restore_status()
        if not self._mdl.prjFile.filePath:
            if not self._ctrl.save_project():
                return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if os.path.isfile(timelinePath):
            action = _('update')
        else:
            action = _('create')
        if self._mdl.isModified:
            if not self._ui.ask_yes_no(_('Save the project and {} the timeline?').format(action)):
                return

            self._ctrl.save_project()
        elif action == _('update') and not self._ui.ask_yes_no(_('Update the timeline?')):
            return

        kwargs = self._get_configuration(self._mdl.prjFile.filePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = self._mdl.nvService.make_novx_file(self._mdl.prjFile.filePath)
        source.novel = self._mdl.nvService.make_novel()
        target = TlFile(timelinePath, **kwargs)
        target.novel = self._mdl.nvService.make_novel()
        try:
            source.read()
            if os.path.isfile(target.filePath):
                target.read()
            target.write(source.novel)
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
        except Error as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(message)

    def _get_configuration(self, sourcePath):
        """Return a dictionary with persistent configuration data."""
        sourceDir = os.path.dirname(sourcePath)
        if not sourceDir:
            sourceDir = '.'
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            pluginCnfDir = f'{homeDir}/{INI_FILEPATH}'
        except:
            pluginCnfDir = '.'
        iniFiles = [f'{pluginCnfDir}/{INI_FILENAME}', f'{sourceDir}/{INI_FILENAME}']
        configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        for iniFile in iniFiles:
            configuration.read(iniFile)
        configData = {}
        configData.update(configuration.settings)
        configData.update(configuration.options)
        return configData

    def _import_to_novx(self):
        """Update the novelibre project from a timeline."""
        if not self._mdl.prjFile:
            return

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if not os.path.isfile(timelinePath):
            self._ui.set_status(_('!No {} file available for this project.').format(APPLICATION))
            return

        if self._mdl.isModified and not self._ui.ask_yes_no(_('Save the project and update it?')):
            return

        self._ctrl.save_project()
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = TlFile(timelinePath, **kwargs)
        target = self._mdl.nvService.make_novx_file(self._mdl.prjFile.filePath, **kwargs)
        message = ''
        try:
            target.novel = self._mdl.nvService.make_novel()
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True)
        except Error as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(f'{message}')

    def _info(self):
        """Show information about the Timeline file."""
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if os.path.isfile(timelinePath):
            try:
                timestamp = os.path.getmtime(timelinePath)
                if timestamp > self._mdl.prjFile.timestamp:
                    cmp = _('newer')
                else:
                    cmp = _('older')
                fileDate = datetime.fromtimestamp(timestamp).strftime('%c')
                message = _('{0} file is {1} than the novelibre project.\n (last saved on {2})').format(APPLICATION, cmp, fileDate)
            except:
                message = _('Cannot determine file date.')
        else:
            message = _('No {} file available for this project.').format(APPLICATION)
        messagebox.showinfo(PLUGIN, message)

    def _launch_application(self):
        """Launch Timeline with the current project."""
        if self._mdl.prjFile:
            timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
            if os.path.isfile(timelinePath):
                if self.OPTIONS['lock_on_export']:
                    self._ctrl.lock()
                open_document(timelinePath)
            else:
                self._ui.set_status(_('!No {} file available for this project.').format(APPLICATION))

