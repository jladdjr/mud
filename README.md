# Mud

A multi-machine deduper.

## Requirements

On Debian, install the following:

<!-- https://www.postgresql.org/docs/13/index.html -->
- postgresql-13
- (optionally) postgresql-doc-13

Note that this will automatically create the postgres user for you.

## Sample .mud config file

```
[scan]
scan_dirs = [
    "/home/jim/foo",
    "/home/jim/bar"
    ]
```
