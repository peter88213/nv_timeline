[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog


### v4.1.2

- Fix a regression from v4.1.1 (c82cb1c) where the update process 
  from timeline fails due to a missing SectionEvent instance variable.

Compatibility: novelibre v4.1 API
Based on novxlib v4.1.0

### v4.1.1

- Fix the installation directory path.

Compatibility: novelibre v4.1 API
Based on novxlib v4.1.0

### v4.1.0

- Library update. Now reading and writing *.novx* version 1.4 files.
- Use factory methods and getters from the model's NvService object.

Compatibility: novelibre v4.1 API
Based on novxlib v4.0.1

### v3.3.3

- Make sure that changes are applied before checking for modification.

Based on novxlib v3.5.3

### v3.3.2

- Indent the novx files up to the content paragraph level, but not
inline elements within paragraphs.
- Set the default locale when creating a new project.

Based on novxlib v3.5.2

### v3.3.1

- Fix a bug where single spaces between emphasized text in section content are lost when writing novx files.

Based on novxlib v3.5.0

### v3.3.0

- Add "lock_on_export" option.

Based on novxlib v3.3.0
Compatibility: novelibre v3.6 API

### v3.2.0

- Library update. Now reading *.novx* version 1.3 files.

Based on novxlib v3.3.0
Compatibility: novelibre v3.6 API

### v3.1.0

- Library update. Now reading *.novx* version 1.2 files.

Based on novxlib v3.2.0
Compatibility: novelibre v3.5 API

### v3.0.1

- Show localized file date/time instead of ISO-formatted date/time.

Based on novxlib v3.0.1
Compatibility: novelibre v3.0 API

### v3.0.0

- Refactor the code for v3.0 API.
- Enable the online help in German.

Based on novxlib v2.0.0
Compatibility: novelibre v3.0 API

### v2.1.0

Update for "novelibre".

Based on novxlib v1.1.0

### v2.0.0

Preparations for renaming the application:
- Refactor the code for v2.0 API.
- Change the installation directory in the setup script.

Based on novxlib v1.1.0
Compatibility: noveltree v2.0 API

### v1.1.0

- Re-structure the website; adjust links.

Based on novxlib v1.1.0
Compatibility: noveltree v1.8 API

### v1.0.3

- Switch the online help to https://peter88213.github.io/noveltree-help/.

Based on novxlib v1.0.0
Compatibility: noveltree v1.0 API

### v1.0.2

- Setup copies the sample configuration file

Based on novxlib v1.0.0
Compatibility: noveltree v1.0 API

### v1.0.1

- Fix the plugin API version constant.
- Bugfix: Use a NovxFile instance as export source.
- Update the build process.

Based on novxlib v1.0.0
Compatibility: noveltree v1.0 API

### v1.0.0

- Release under the GPLv3 license.

Based on novxlib v1.0.0
Compatibility: noveltree v1.0 API
