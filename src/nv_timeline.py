"""Timeline sync plugin for novelibre.

Version @release
Requires Python 3.6+
Copyright (c) 2025 Peter Triesberger
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
from pathlib import Path
from tkinter import ttk
import webbrowser

from nvtimeline.nvtimeline_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
import tkinter as tk
from nvtimeline.tl_service import TlService


class Plugin(PluginBase):
    """Plugin class for synchronization with Timeline."""
    VERSION = '@release'
    API_VERSION = '5.18'
    DESCRIPTION = 'Synchronize with Timeline'
    URL = 'https://github.com/peter88213/nv_timeline'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_timeline/'

    FEATURE = 'Timeline'

    def create_novx(self):
        self.timelineService.create_novx()

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')
        self._timelineButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')
        self._timelineButton.config(state='normal')

    def export_from_novx(self):
        self.timelineService.export_from_novx()

    def import_to_novx(self):
        self.timelineService.import_to_novx()

    def info(self):
        self.timelineService.info()

    def install(self, model, view, controller):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)

        # Create a submenu in the Tools menu.
        self.pluginMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._ui.toolsMenu.add_cascade(
            label=self.FEATURE,
            menu=self.pluginMenu,
        )
        self._ui.toolsMenu.entryconfig(
            self.FEATURE,
            state='disabled',
        )
        self.pluginMenu.add_command(
            label=_('Information'),
            command=self.info,
        )
        self.pluginMenu.add_separator()
        self.pluginMenu.add_command(
            label=_('Create or update the timeline'),
            command=self.export_from_novx,
        )
        self.pluginMenu.add_command(
            label=_('Update the project'),
            command=self.import_to_novx,
        )
        self.pluginMenu.add_separator()
        self.pluginMenu.add_command(
            label=_('Open Timeline'),
            command=self.launch_application,
        )

        # Add an entry to the "File > New" menu.
        self._ui.newMenu.add_command(
            label=_('Create from Timeline...'),
            command=self.create_novx,
        )

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(
            label=_('Timeline plugin Online help'),
            command=self.open_help,
        )

        #--- Configure the toolbar.
        self._configure_toolbar()

        self.timelineService = TlService(
            model,
            view,
            controller,
            self.FEATURE,
        )

    def launch_application(self):
        self.timelineService.launch_application()

    def lock(self):
        """Inhibit changes on the model.
        
        Overrides the superclass method.
        """
        self.pluginMenu.entryconfig(
            _('Update the project'),
            state='disabled',
        )

    def open_help(self):
        webbrowser.open(self.HELP_URL)

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        self.pluginMenu.entryconfig(
            _('Update the project'),
            state='normal',
        )

    def _configure_toolbar(self):

        # Get the icons.
        prefs = self._ctrl.get_preferences()
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
        tk.Frame(
            self._ui.toolbar.buttonBar,
            bg='light gray',
            width=1,
        ).pack(side='left', fill='y', padx=4)

        # Put a button on the toolbar.
        self._timelineButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=_('Open Timeline'),
            image=tlIcon,
            command=self.launch_application
        )
        self._timelineButton.pack(side='left')
        self._timelineButton.image = tlIcon

        # Initialize tooltip.
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self._timelineButton, self._timelineButton['text'])

