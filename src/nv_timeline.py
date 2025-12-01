"""Timeline sync plugin for novelibre.

Version @release
Requires Python 3.7+
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
import webbrowser

from nvtimeline.nvtimeline_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
from nvlib.gui.menus.nv_menu import NvMenu
from nvtimeline.tl_service import TlService


class Plugin(PluginBase):
    """Plugin class for synchronization with Timeline."""
    VERSION = '@release'
    API_VERSION = '5.44'
    DESCRIPTION = 'Synchronize with Timeline'
    URL = 'https://github.com/peter88213/nv_timeline'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_timeline/'

    FEATURE = 'Timeline'

    def create_novx(self):
        self.timelineService.create_novx()

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
        self.timelineService = TlService(
            model,
            view,
            controller,
            self.FEATURE,
        )
        self._icon = self._get_icon('tl.png')

        # Create a submenu in the Tools menu.
        self.pluginMenu = NvMenu()

        label = self.FEATURE
        self._ui.toolsMenu.add_cascade(
            label=label,
            image=self._icon,
            compound='left',
            menu=self.pluginMenu,
            state='disabled',
        )
        self._ui.toolsMenu.disableOnClose.append(label)

        label = _('Information')
        self.pluginMenu.add_command(
            label=label,
            command=self.info,
        )

        self.pluginMenu.add_separator()

        label = _('Create or update the timeline')
        self.pluginMenu.add_command(
            label=label,
            command=self.export_from_novx,
        )

        label = _('Update the project')
        self.pluginMenu.add_command(
            label=label,
            command=self.import_to_novx,
        )
        self.pluginMenu.disableOnLock.append(label)

        label = _('Open Timeline')
        self.pluginMenu.add_separator()
        self.pluginMenu.add_command(
            label=label,
            command=self.launch_application,
        )

        # Add an entry to the "File > New" menu.
        label = _('Create from Timeline...')
        self._ui.newMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self.create_novx,
        )

        # Add an entry to the Help menu.
        label = _('Timeline plugin Online help')
        self._ui.helpMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self.open_help,
        )

        #--- Configure the toolbar.
        self._ui.toolbar.add_separator(),

        # Put a button on the toolbar.
        self._ui.toolbar.new_button(
            text=_('Open Timeline'),
            image=self._icon,
            command=self.launch_application,
            disableOnLock=False,
        ).pack(side='left')

    def launch_application(self):
        self.timelineService.launch_application()

    def lock(self):
        self.pluginMenu.lock()

    def open_help(self):
        webbrowser.open(self.HELP_URL)

    def unlock(self):
        self.pluginMenu.unlock()

