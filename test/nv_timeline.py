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
import gettext
import locale
import os
from pathlib import Path
import sys
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

from calendar import day_name, month_name

ROOT_PREFIX = 'rt'
CHAPTER_PREFIX = 'ch'
PLOT_LINE_PREFIX = 'ac'
SECTION_PREFIX = 'sc'
PLOT_POINT_PREFIX = 'ap'
CHARACTER_PREFIX = 'cr'
LOCATION_PREFIX = 'lc'
ITEM_PREFIX = 'it'
PRJ_NOTE_PREFIX = 'pn'
CH_ROOT = f'{ROOT_PREFIX}{CHAPTER_PREFIX}'
PL_ROOT = f'{ROOT_PREFIX}{PLOT_LINE_PREFIX}'
CR_ROOT = f'{ROOT_PREFIX}{CHARACTER_PREFIX}'
LC_ROOT = f'{ROOT_PREFIX}{LOCATION_PREFIX}'
IT_ROOT = f'{ROOT_PREFIX}{ITEM_PREFIX}'
PN_ROOT = f'{ROOT_PREFIX}{PRJ_NOTE_PREFIX}'

BRF_SYNOPSIS_SUFFIX = '_brf_synopsis'
CHAPTERS_SUFFIX = '_chapters_tmp'
CHARACTER_REPORT_SUFFIX = '_character_report'
CHARACTERS_SUFFIX = '_characters_tmp'
CHARLIST_SUFFIX = '_charlist_tmp'
DATA_SUFFIX = '_data'
GRID_SUFFIX = '_grid_tmp'
ITEM_REPORT_SUFFIX = '_item_report'
ITEMLIST_SUFFIX = '_itemlist_tmp'
ITEMS_SUFFIX = '_items_tmp'
LOCATION_REPORT_SUFFIX = '_location_report'
LOCATIONS_SUFFIX = '_locations_tmp'
LOCLIST_SUFFIX = '_loclist_tmp'
MANUSCRIPT_SUFFIX = '_manuscript_tmp'
PARTS_SUFFIX = '_parts_tmp'
PLOTLIST_SUFFIX = '_plotlist'
PLOTLINES_SUFFIX = '_plotlines_tmp'
PROJECTNOTES_SUFFIX = '_projectnote_report'
PROOF_SUFFIX = '_proof_tmp'
SECTIONLIST_SUFFIX = '_sectionlist'
SECTIONS_SUFFIX = '_sections_tmp'
STAGES_SUFFIX = '_structure_tmp'
XREF_SUFFIX = '_xref'


class Error(Exception):
    pass


locale.setlocale(locale.LC_TIME, "")
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('novelibre', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

WEEKDAYS = day_name
MONTHS = month_name


def norm_path(path):
    if path is None:
        path = ''
    return os.path.normpath(path)


def string_to_list(text, divider=';'):
    elements = []
    try:
        tempList = text.split(divider)
        for element in tempList:
            element = element.strip()
            if element and not element in elements:
                elements.append(element)
        return elements

    except:
        return []


def list_to_string(elements, divider=';'):
    try:
        text = divider.join(elements)
        return text

    except:
        return ''


def intersection(elemList, refList):
    return [elem for elem in elemList if elem in refList]


def open_document(document):
    try:
        os.startfile(norm_path(document))
    except:
        try:
            os.system('xdg-open "%s"' % norm_path(document))
        except:
            try:
                os.system('open "%s"' % norm_path(document))
            except:
                pass
from datetime import datetime
from datetime import timedelta
import re

from abc import ABC
from urllib.parse import quote



class File(ABC):
    DESCRIPTION = _('File')
    EXTENSION = None
    SUFFIX = None

    def __init__(self, filePath, **kwargs):
        self.novel = None
        self._filePath = None
        self.projectName = None
        self.projectPath = None
        self.sectionsSplit = False
        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath: str):
        if self.SUFFIX is not None:
            suffix = self.SUFFIX
        else:
            suffix = ''
        if filePath.lower().endswith(f'{suffix}{self.EXTENSION}'.lower()):
            self._filePath = filePath
            try:
                head, tail = os.path.split(os.path.realpath(filePath))
            except:
                head, tail = os.path.split(filePath)
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(tail.replace(f'{suffix}{self.EXTENSION}', ''))

    def is_locked(self):
        return False

    def read(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError



def indent(elem, level=0):
    PARAGRAPH_LEVEL = 5

    i = f'\n{level * "  "}'
    if elem:
        if not elem.text or not elem.text.strip():
            elem.text = f'{i}  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        if level < PARAGRAPH_LEVEL:
            for elem in elem:
                indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def fix_iso_dt(tlDateTime):
    if tlDateTime.startswith('-'):
        tlDateTime = tlDateTime.strip('-')
        isBc = True
    else:
        isBc = False
    dt = tlDateTime.split('-', 1)
    dt[0] = dt[0].zfill(4)
    tlDateTime = ('-').join(dt)
    if isBc:
        tlDateTime = f'-{tlDateTime}'
    return tlDateTime
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, MINYEAR


class SectionEvent:
    defaultDateTime = '1900-01-01 00:00:00'
    sectionColor = '170,240,160'

    def __init__(self, section):
        self._section = section

        self.title = section.title
        self.desc = section.desc
        self.sectionContent = section.sectionContent
        self.scType = section.scType
        self.scene = section.scene
        self.status = section.status
        self.notes = section.notes
        self.tags = section.tags
        self.appendToPrev = section.appendToPrev
        self.goal = section.goal
        self.conflict = section.conflict
        self.outcome = section.outcome
        self.date = section.date
        self.time = section.time
        self.day = section.day
        self.lastsMinutes = section.lastsMinutes
        self.lastsHours = section.lastsHours
        self.lastsDays = section.lastsDays
        self.characters = section.characters
        self.locations = section.locations
        self.items = section.items

        self.contId = None
        self._startDateTime = None
        self._endDateTime = None

        self.NULL_DATE = section.NULL_DATE
        self.NULL_TIME = section.NULL_TIME

    def set_date_time(self, startDateTime, endDateTime, isUnspecific):
        self._startDateTime = startDateTime
        self._endDateTime = endDateTime

        dtIsValid = True

        dt = startDateTime.split(' ')
        if dt[0].startswith('-'):
            startYear = -1 * int(dt[0].split('-')[1])
            dtIsValid = False
        else:
            startYear = int(dt[0].split('-')[0])
        if startYear < MINYEAR:
            self.date = self.NULL_DATE
            self.time = self.NULL_TIME
            dtIsValid = False
        else:
            self.date = dt[0]
            self.time = dt[1]
        if dtIsValid:
            sectionStart = datetime.fromisoformat(startDateTime)
            sectionEnd = datetime.fromisoformat(endDateTime)
            sectionDuration = sectionEnd - sectionStart
            lastsHours = sectionDuration.seconds // 3600
            lastsMinutes = (sectionDuration.seconds % 3600) // 60
            self.lastsDays = str(sectionDuration.days)
            self.lastsHours = str(lastsHours)
            self.lastsMinutes = str(lastsMinutes)
            if isUnspecific:
                try:
                    sectionDate = date.fromisoformat(self.date)
                    referenceDate = date.fromisoformat(self.defaultDateTime.split(' ')[0])
                    self.day = str((sectionDate - referenceDate).days)
                except:
                    self.day = None
                self.date = None

    def merge_date_time(self, source, defaultDay=0):
        if source.date is not None and source.date != self.NULL_DATE:
            if source.time:
                self._startDateTime = f'{source.date} {source.time}'
            else:
                self._startDateTime = f'{source.date} 00:00:00'
        elif source.date is None:
            if source.day:
                dayInt = int(source.day)
            else:
                dayInt = defaultDay
            if source.time:
                startTime = source.time
            else:
                startTime = '00:00:00'
            sectionDelta = timedelta(days=dayInt)
            defaultDate = self.defaultDateTime.split(' ')[0]
            startDate = (date.fromisoformat(defaultDate) + sectionDelta).isoformat()
            self._startDateTime = f'{startDate} {startTime}'
        elif self._startDateTime is None:
            self._startDateTime = self.defaultDateTime
        else:
            pass

        if source.date is not None and source.date == self.NULL_DATE:
            if self._endDateTime is None:
                self._endDateTime = self._startDateTime
        else:
            if source.lastsDays:
                lastsDays = int(source.lastsDays)
            else:
                lastsDays = 0
            if source.lastsHours:
                lastsSeconds = int(source.lastsHours) * 3600
            else:
                lastsSeconds = 0
            if source.lastsMinutes:
                lastsSeconds += int(source.lastsMinutes) * 60
            sectionDuration = timedelta(days=lastsDays, seconds=lastsSeconds)
            sectionStart = datetime.fromisoformat(self._startDateTime)
            sectionEnd = sectionStart + sectionDuration
            self._endDateTime = sectionEnd.isoformat(' ')
        if self._startDateTime > self._endDateTime:
            self._endDateTime = self._startDateTime

    def build_branch(self, xmlEvent, scId, dtMin, dtMax):
        scIndex = 0
        try:
            xmlEvent.find('start').text = self._startDateTime
        except(AttributeError):
            ET.SubElement(xmlEvent, 'start').text = self._startDateTime
        if (not dtMin) or (self._startDateTime < dtMin):
            dtMin = self._startDateTime
        scIndex += 1
        try:
            xmlEvent.find('end').text = self._endDateTime
        except(AttributeError):
            ET.SubElement(xmlEvent, 'end').text = self._endDateTime
        if (not dtMax) or (self._endDateTime > dtMax):
            dtMax = self._endDateTime
        scIndex += 1
        if not self.title:
            self.title = f'Unnamed section ID{scId}'
        try:
            xmlEvent.find('text').text = self.title
        except(AttributeError):
            ET.SubElement(xmlEvent, 'text').text = self.title
        scIndex += 1
        if xmlEvent.find('progress') is None:
            ET.SubElement(xmlEvent, 'progress').text = '0'
        scIndex += 1
        if xmlEvent.find('fuzzy') is None:
            ET.SubElement(xmlEvent, 'fuzzy').text = 'False'
        scIndex += 1
        if xmlEvent.find('fuzzy_start') is not None:
            scIndex += 1
        if xmlEvent.find('fuzzy_end') is not None:
            scIndex += 1
        if xmlEvent.find('locked') is None:
            ET.SubElement(xmlEvent, 'locked').text = 'False'
        scIndex += 1
        if xmlEvent.find('ends_today') is None:
            ET.SubElement(xmlEvent, 'ends_today').text = 'False'
        scIndex += 1
        if self.desc is not None:
            try:
                xmlEvent.find('description').text = self.desc
            except(AttributeError):
                if xmlEvent.find('labels') is None:
                    ET.SubElement(xmlEvent, 'description').text = self.desc
                else:
                    if xmlEvent.find('category') is not None:
                        scIndex += 1
                    desc = ET.Element('description')
                    desc.text = self.desc
                    xmlEvent.insert(scIndex, desc)
        elif xmlEvent.find('description') is not None:
            xmlEvent.remove(xmlEvent.find('description'))
        if xmlEvent.find('labels') is None:
            ET.SubElement(xmlEvent, 'labels').text = scId
        if xmlEvent.find('default_color') is None:
            ET.SubElement(xmlEvent, 'default_color').text = self.sectionColor
        return dtMin, dtMax

    def to_xml(self, xmlElement):

        self._section.title = self.title
        self._section.desc = self.desc
        self._section.sectionContent = self.sectionContent
        self._section.scType = self.scType
        self._section.scene = self.scene
        self._section.status = self.status
        self._section.notes = self.notes
        self._section.tags = self.tags
        self._section.appendToPrev = self.appendToPrev
        self._section.goal = self.goal
        self._section.conflict = self.conflict
        self._section.outcome = self.outcome
        self._section.date = self.date
        self._section.time = self.time
        self._section.day = self.day
        self._section.lastsMinutes = self.lastsMinutes
        self._section.lastsHours = self.lastsHours
        self._section.lastsDays = self.lastsDays
        self._section.characters = self.characters
        self._section.locations = self.locations
        self._section.items = self.items

        self._section.to_xml(xmlElement)


class TlFile(File):
    DESCRIPTION = 'Timeline'
    EXTENSION = '.timeline'
    SUFFIX = None

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        self._nvSvc = kwargs['nv_service']
        self._xmlTree = None
        self._sectionMarker = kwargs['section_label']
        SectionEvent.sectionColor = kwargs['section_color']

        try:
            self._newEventSpacing = int(kwargs['new_event_spacing'])
        except:
            self._newEventSpacing = 0

    def read(self):

        def remove_contId(event, text):
            if text:
                match = re.match('([\(\[][0-9]+[\)\]])', text)
                if match:
                    contId = match.group()
                    event.contId = contId
                    text = text.split(contId, 1)[1]
            return text

        if self.novel.referenceDate:
            SectionEvent.defaultDateTime = f'{self.novel.referenceDate} 00:00:00'
        else:
            SectionEvent.defaultDateTime = datetime.today().isoformat(' ', 'seconds')

        if not self.novel.sections:
            isOutline = True
        else:
            isOutline = False

        try:
            self._xmlTree = ET.parse(self.filePath)
        except:
            raise Error(f'{_("Can not process file")}: "{norm_path(self.filePath)}".')
        root = self._xmlTree.getroot()
        sectionCount = 0
        scIdsByDate = {}
        for event in root.iter('event'):
            scId = None
            sectionMatch = None
            if event.find('labels') is not None:
                labels = event.find('labels').text
                sectionMatch = re.search(f'{SECTION_PREFIX}[0-9]+', labels)
                if isOutline and sectionMatch is None:
                    sectionMatch = re.search(self._sectionMarker, labels)
            if sectionMatch is None:
                continue

            sectionDate = None
            if isOutline:
                sectionCount += 1
                sectionMarker = sectionMatch.group()
                scId = f'{SECTION_PREFIX}{sectionCount}'
                event.find('labels').text = labels.replace(sectionMarker, scId)
                self.novel.sections[scId] = SectionEvent(
                    self._nvSvc.make_section(
                    status=1,
                    scType=0,
                    scene=0,
                    ))

            else:
                try:
                    scId = sectionMatch.group()
                    self.novel.sections[scId] = SectionEvent(self.novel.sections[scId])
                except:
                    continue

            try:
                title = event.find('text').text
                title = remove_contId(self.novel.sections[scId], title)
                title = self._convert_to_novx(title)
                self.novel.sections[scId].title = title
            except:
                self.novel.sections[scId].title = f'Section {scId}'
            try:
                self.novel.sections[scId].desc = event.find('description').text
            except:
                pass

            startDateTime = fix_iso_dt(event.find('start').text)
            endDateTime = fix_iso_dt(event.find('end').text)

            if isOutline:
                isUnspecific = False
            else:
                if self.novel.sections[scId].day is not None:
                    isUnspecific = True
                else:
                    isUnspecific = False
            self.novel.sections[scId].set_date_time(startDateTime, endDateTime, isUnspecific)
            if not startDateTime in scIdsByDate:
                scIdsByDate[startDateTime] = []
            scIdsByDate[startDateTime].append(scId)

        srtSections = sorted(scIdsByDate.items())
        if isOutline:
            chId = f'{CHAPTER_PREFIX}1'
            self.novel.chapters[chId] = self._nvSvc.make_chapter(
                chType=0,
                title=f'{_("Chapter")} 1'
                )
            self.novel.tree.append(CH_ROOT, chId)
            for __, scList in srtSections:
                for scId in scList:
                    self.novel.tree.append(chId, scId)
            os.replace(self.filePath, f'{self.filePath}.bak')
            try:
                self._xmlTree.write(self.filePath, xml_declaration=True, encoding='utf-8')
            except:
                os.replace(f'{self.filePath}.bak', self.filePath)
                raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

    def write(self, source):

        def add_contId(event, text):
            if event.contId is not None:
                return f'{event.contId}{text}'
            return text

        def set_view_range(dtMin, dtMax):
            if dtMin is None:
                dtMin = SectionEvent.defaultDateTime
            if dtMax is None:
                dtMax = dtMin
            TIME_LIMIT = '0100-01-01 00:00:00'
            SEC_PER_DAY = 24 * 3600
            dt = dtMin.split(' ')
            if dt[0].startswith('-'):
                startYear = -1 * int(dt[0].split('-')[1])
            else:
                startYear = int(dt[0].split('-')[0])
            if startYear < 100:
                if dtMax == dtMin:
                    dtMax = TIME_LIMIT
                return dtMin, dtMax
            vrMax = datetime.fromisoformat(dtMax)
            vrMin = datetime.fromisoformat(dtMin)
            viewRange = (vrMax - vrMin).total_seconds()

            if viewRange > SEC_PER_DAY:
                margin = viewRange / 10
            else:
                margin = 3600
            dtMargin = timedelta(seconds=margin)
            try:
                vrMin -= dtMargin
                dtMin = vrMin.isoformat(' ', 'seconds')
            except OverflowError:
                pass
            try:
                vrMax += dtMargin
                dtMax = vrMax.isoformat(' ', 'seconds')
            except OverflowError:
                pass
            return dtMin, dtMax

        self.novel.chapters = {}
        self.novel.tree = self._nvSvc.make_nv_tree()

        if source.referenceDate:
            SectionEvent.defaultDateTime = f'{source.referenceDate} 00:00:00'
            ignoreUnspecific = False
        else:
            SectionEvent.defaultDateTime = datetime.today().isoformat(' ', 'seconds')
            ignoreUnspecific = True

        defaultDay = 0
        for chId in source.tree.get_children(CH_ROOT):
            self.novel.chapters[chId] = self._nvSvc.make_chapter()
            self.novel.tree.append(CH_ROOT, chId)
            for scId in source.tree.get_children(chId):
                if ignoreUnspecific and source.sections[scId].date is None:
                    continue

                if not scId in self.novel.sections:
                    self.novel.sections[scId] = SectionEvent(self._nvSvc.make_section())
                self.novel.tree.append(chId, scId)
                if source.sections[scId].title:
                    title = source.sections[scId].title
                    title = self._convert_from_novx(title)
                    title = add_contId(self.novel.sections[scId], title)
                    self.novel.sections[scId].title = title
                self.novel.sections[scId].desc = source.sections[scId].desc
                defaultDay += self._newEventSpacing
                self.novel.sections[scId].merge_date_time(source.sections[scId], defaultDay=defaultDay)
                self.novel.sections[scId].scType = source.sections[scId].scType
        sections = list(self.novel.sections)
        for scId in sections:
            if not scId in source.sections:
                del self.novel.sections[scId]

        dtMin = None
        dtMax = None

        srtSections = []
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType == 0:
                    srtSections.append(scId)
        if self._xmlTree is not None:
            root = self._xmlTree.getroot()
            events = root.find('events')
            trash = []
            scIds = []

            for event in events.iter('event'):
                if event.find('labels') is not None:
                    labels = event.find('labels').text
                    sectionMatch = re.search(f'{SECTION_PREFIX}[0-9]+', labels)
                else:
                    continue

                if sectionMatch is not None:
                    scId = sectionMatch.group()
                    if scId in srtSections:
                        scIds.append(scId)
                        dtMin, dtMax = self.novel.sections[scId].build_branch(event, scId, dtMin, dtMax)
                    else:
                        trash.append(event)

            for scId in srtSections:
                if not scId in scIds:
                    event = ET.SubElement(events, 'event')
                    dtMin, dtMax = self.novel.sections[scId].build_branch(event, scId, dtMin, dtMax)
            for event in trash:
                events.remove(event)

            dtMin, dtMax = set_view_range(dtMin, dtMax)
            view = root.find('view')
            period = view.find('displayed_period')
            period.find('start').text = dtMin
            period.find('end').text = dtMax
        else:
            root = ET.Element('timeline')
            ET.SubElement(root, 'version').text = '2.4.0 (3f207fbb63f0 2021-04-07)'
            ET.SubElement(root, 'timetype').text = 'gregoriantime'
            ET.SubElement(root, 'categories')
            events = ET.SubElement(root, 'events')
            for scId in srtSections:
                event = ET.SubElement(events, 'event')
                dtMin, dtMax = self.novel.sections[scId].build_branch(event, scId, dtMin, dtMax)

            dtMin, dtMax = set_view_range(dtMin, dtMax)
            view = ET.SubElement(root, 'view')
            period = ET.SubElement(view, 'displayed_period')
            ET.SubElement(period, 'start').text = dtMin
            ET.SubElement(period, 'end').text = dtMax
        indent(root)
        self._xmlTree = ET.ElementTree(root)

        backedUp = False
        if os.path.isfile(self.filePath):
            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
            except:
                raise Error(f'{_("Cannot overwrite file")}: "{norm_path(self.filePath)}".')
            else:
                backedUp = True
        try:
            self._xmlTree.write(self.filePath, xml_declaration=True, encoding='utf-8')
        except:
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

    def _convert_to_novx(self, text):
        if text is not None:
            if text.startswith(' ('):
                text = text.lstrip()
            elif text.startswith(' ['):
                text = text.lstrip()
        return text

    def _convert_from_novx(self, text, quick=False):
        if text is not None:
            if text.startswith('('):
                text = f' {text}'
            elif text.startswith('['):
                text = f' {text}'
        return text
import tkinter as tk

LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
CURRENT_LANGUAGE = locale.getlocale()[0][:2]
try:
    t = gettext.translation('nv_timeline', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:
    pass

APPLICATION = 'Timeline'
PLUGIN = f'{APPLICATION} plugin v@release'
INI_FILENAME = 'nv_timeline.ini'
INI_FILEPATH = '.novelibre/config'


class Plugin():
    VERSION = '@release'
    API_VERSION = '4.1'
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

    def install(self, model, view, controller, prefs):
        """Add a submenu to the main menu.
        
        Positional arguments:
            controller -- reference to the main controller instance of the application.
            view -- reference to the main view instance of the application.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        self._pluginMenu = tk.Menu(self._ui.mainMenu, tearoff=0)
        position = self._ui.mainMenu.index('end')
        self._ui.mainMenu.insert_cascade(position, label=APPLICATION, menu=self._pluginMenu)
        self._pluginMenu.add_command(label=_('Information'), command=self._info)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Create or update the timeline'), command=self._export_from_novx)
        self._pluginMenu.add_command(label=_('Update the project'), command=self._import_to_novx)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Edit the timeline'), command=self._launch_application)

        self._ui.newMenu.add_command(label=_('Create from Timeline...'), command=self._create_novx)

        self._ui.helpMenu.add_command(label=_('Timeline plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

    def disable_menu(self):
        self._ui.mainMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        self._ui.mainMenu.entryconfig(APPLICATION, state='normal')

    def _create_novx(self):
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
        target = self._mdl.prjFile
        message = ''
        try:
            target.novel = self._mdl.nvService.make_novel()
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True)
        finally:
            self._ui.set_status(f'{message}')

    def _info(self):
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
        if self._mdl.prjFile:
            timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
            if os.path.isfile(timelinePath):
                if self.OPTIONS['lock_on_export']:
                    self._ctrl.lock()
                open_document(timelinePath)
            else:
                self._ui.set_status(_('!No {} file available for this project.').format(APPLICATION))

