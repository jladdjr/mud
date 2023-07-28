# Mud

A multi-machine deduper.

## Requirements

### Preparing the database

Before we begin, let's first note that `postgres` is heavily overloaded in the following procedure. `postgres` can refer to:
- the OS system account
- the PostgreSQL application account
- the postgres database

In the following instructions we will try to call out which specific role we are referring to :-)

#### Install PostgreSQL

On Debian, install the following:

<!-- https://www.postgresql.org/docs/15/index.html -->
- postgresql-15
- (optionally) postgresql-doc-15

Note that this will automatically create the postgres user for you.

This will also automatically create a database cluster for you, which can be confirmed by calling `pg_lsclusters`.

#### Create new database user ("mud")

By default, postgres will use `peer` authentication for the postgres user. This requires that you be logged in as the `postgres` _system_ user when calling `psql -U postgres`.

Do the following to create a new postgres (application) user, called `mud`, that will use _password_ authentication:

- Switch to the postgres system user with `sudo su` followed by `su postgres`
- Access the postgres database with `psql -U postgres`
- Create the mud user with:
  `CREATE ROLE mud WITH LOGIN PASSWORD 'thisisnotarealpassword';`

Next, add the following line to pg\_hba.conf to ensure password-based access is enabled for the `mud` user. Place this rule before all other existing rules to make sure it is evaluated first (the rules in pg\_hba.conf are evaluated sequentially).

  `local all mud md5`

Note: On Debian, this file is located at `/etc/postgresql/15/main/pg_hba.conf`

Next, prompt postgres to reload the pg_hba.conf configuration with:
  `pg_ctlcluster 15 main reload`

You can confirm that the `mud` user has access by logging out of the `postgres` user session and calling:
  `psql -U mud postgres`

If successful, this should log you into the `postgres` database (one of the default databases intially present) as the `mud` user.

#### Create new database ("mud")

1. Switch to the `postgres` user (`sudo su` followed by `su postrges`).
2. Create a new database and set the `mud` user as owner with `createdb -O mud mud`.

#### Troubleshooting database issues

Should you encounter errors during this process, consult the postgres log file located at `/var/log/postgresql/postgresql-15-main.log`

## Configuring Mud

Sample .mudrc file is provided below.
Can be in current working directory or in user's home folder.

```
[scan]
scan_dirs = [
    "/home/jim/foo",
    "/home/jim/bar"
    ]
```
