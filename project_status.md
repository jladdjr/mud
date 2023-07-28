# Mud Project Status

| Goal       | Status      | Notes                                                             |
|:-----------|:------------|:------------------------------------------------------------------|
| Readme     | In Progress | Should introduce project and associated resources at a high level |
| Info Pages | Not Started | Installation, configuration, general usage                        |
| Test Hooks | Not Started | Make target for installing Git pre-commit hook                    |

## Development Goals

| Goal                                                                           | Status      | Notes                                                                                                                |
|:-------------------------------------------------------------------------------|:------------|:---------------------------------------------------------------------------------------------------------------------|
| Add ability to invoke installer / uninstaller using the CLI                    | Not Started | Should prompt user to confirm that they want to delete everything (and let them know what they will lose)            |
| Update creation of StorageController to source user's db configuration         | Not Started | Will need to either handle DB password securely, or defer to PostgreSQL's method of storing the password if possible |
| Update scan method to collect all file metadata used by StorageController      | Not Started |                                                                                                                      |
| Create install directory, place all install-related files under the new folder | Not Started |                                                                                                                      |

