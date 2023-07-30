# Mud Project Status

| Goal       | Status      | Notes                                                             |
|:-----------|:------------|:------------------------------------------------------------------|
| Readme     | In Progress | Should introduce project and associated resources at a high level |
| Info Pages | Not Started | Installation, configuration, general usage                        |
| Test Hooks | Not Started | Make target for installing Git pre-commit hook                    |

## Development Goals

| Goal                                                                           | Status      | Notes                                                                                                     |
|:-------------------------------------------------------------------------------|:------------|:----------------------------------------------------------------------------------------------------------|
| De-normalize hashes                                                            | Not Started | Create table for hashes, use hash foreign keys in other tables                                            |
| Update metadata if it already exists                                           | Not Started |                                                                                                           |
| Create records to note when scans happened                                     | Not Started |                                                                                                           |
| Skip files that haven't changed since last scan                                | Not Started |                                                                                                           |
| Create progress bar for scans                                                  | Not Started |                                                                                                           |
| Create first analyzer / report (e.g. largest files, redundant files)           | Not Started |                                                                                                           |
| Add ability to invoke installer / uninstaller using the CLI                    | Not Started | Should prompt user to confirm that they want to delete everything (and let them know what they will lose) |
| Create install directory, place all install-related files under the new folder | Not Started |                                                                                                           |

