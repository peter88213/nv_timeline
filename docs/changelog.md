[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog


### Version 5.0.1

Library update:
- Refactor the code for better maintainability.

API: 5.0
Based on novelibre 5.0.12

### Version 4.4.3

- Change the message window title.

Refactor the code for better maintainability:

- Replace global constants with class constants.
- Remove dead code.

Compatibility: novelibre 4.11 API
Based on novxlib 5.0.0

### Version 4.4.2

- Fix a regression from version 4.4.1.

Compatibility: novelibre 4.11 API
Based on novxlib 4.7.1

### Version 4.4.1

- Complete the SectionEvent initialization.

Compatibility: novelibre 4.11 API
Based on novxlib 4.7.1

### Version 4.4.0

- Add a tooltip to the toolbar button.

Compatibility: novelibre 4.11 API
Based on novxlib 4.6.4

### Version 4.3.3

- Refactor: Change import order for a quick start.

Compatibility: novelibre 4.3 API
Based on novxlib 4.6.3

### Version 4.3.2

- Refactor for future Python versions.

Compatibility: novelibre 4.3 API
Based on novxlib 4.5.9

### Version 4.3.1

- Refactor localization.

Compatibility: novelibre 4.3 API
Based on novxlib 4.4.0

### Version 4.3.0

- Move the **Timeline** submenu from the main menu to the **Tools** menu.
- Add a "Timeline" button to the button bar.

Compatibility: novelibre 4.3 API
Based on novxlib 4.4.0

### Version 4.2.2

- Update the German translation.

Compatibility: novelibre 4.3 API
Based on novxlib 4.2.3

### Version 4.2.1

- Refactor the code for future API update,
  making the prefs argument of the Plugin.install() method optional.

Compatibility: novelibre 4.3 API
Based on novxlib 4.1.0

### Version 4.2.0

- Refactor the code for better maintainability.

Compatibility: novelibre 4.3 API
Based on novxlib 4.1.0

### Version 4.1.3

- Fix a bug where writing the .novx file during update has a side effect 
  on the project's actual model, replacing the nvTreeview delegate with 
  a nvTree instance, where not all required methods are implemented. 
  This bug exists from the very beginning. 

Compatibility: novelibre 4.1 API
Based on novxlib 4.1.0

### Version 4.1.2

- Fix a regression from version 4.1.1 (c82cb1c) where the update process 
  from timeline fails due to a missing SectionEvent instance variable.

Compatibility: novelibre 4.1 API
Based on novxlib 4.1.0

### Version 4.1.1

- Fix the installation directory path.

Compatibility: novelibre 4.1 API
Based on novxlib 4.1.0

### Version 4.1.0

- Library update. Now reading and writing *.novx* version 1.4 files.
- Use factory methods and getters from the model's NvService object.

Compatibility: novelibre 4.1 API
Based on novxlib 4.0.1

### Version 3.3.3

- Make sure that changes are applied before checking for modification.

Based on novxlib 3.5.3

### Version 3.3.2

- Indent the novx files up to the content paragraph level, but not
inline elements within paragraphs.
- Set the default locale when creating a new project.

Based on novxlib 3.5.2

### Version 3.3.1

- Fix a bug where single spaces between emphasized text in section content are lost when writing novx files.

Based on novxlib 3.5.0

### Version 3.3.0

- Add "lock_on_export" option.

Based on novxlib 3.3.0
Compatibility: novelibre 3.6 API

### Version 3.2.0

- Library update. Now reading *.novx* version 1.3 files.

Based on novxlib 3.3.0
Compatibility: novelibre 3.6 API

### Version 3.1.0

- Library update. Now reading *.novx* version 1.2 files.

Based on novxlib 3.2.0
Compatibility: novelibre 3.5 API

### Version 3.0.1

- Show localized file date/time instead of ISO-formatted date/time.

Based on novxlib 3.0.1
Compatibility: novelibre 3.0 API

### Version 3.0.0

- Refactor the code for v3.0 API.
- Enable the online help in German.

Based on novxlib 2.0.0
Compatibility: novelibre 3.0 API

### Version 2.1.0

Update for "novelibre".

Based on novxlib 1.1.0

### Version 2.0.0

Preparations for renaming the application:
- Refactor the code for v2.0 API.
- Change the installation directory in the setup script.

Based on novxlib 1.1.0
Compatibility: noveltree 2.0 API

### Version 1.1.0

- Re-structure the website; adjust links.

Based on novxlib 1.1.0
Compatibility: noveltree 1.8 API

### Version 1.0.3

- Switch the online help to https://peter88213.github.io/noveltree-help/.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API

### Version 1.0.2

- Setup copies the sample configuration file

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API

### Version 1.0.1

- Fix the plugin API version constant.
- Bugfix: Use a NovxFile instance as export source.
- Update the build process.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API

### Version 1.0.0

- Release under the GPLv3 license.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API
