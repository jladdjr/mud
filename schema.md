# Schema Design

## machine

Description:
Represents a host.

- Primary Key machine_id
- String hostname
- String description

## scan_session

Description:
Represents a session in which mud scanned directories to collect file metadata.

- Primary Key scan_session_id
- Foreign Key scan_state_id
- Foreign Key scanned_machine_id
  - Note that a scan can only collect metadata on the local machine
- DateTime scan_start
- DateTime scan_stop

## scan_states

Description:
The states representing the life cycle of a scan. Validates scan states for the scan_session table.

- Primary Key scan_state_id
- str scan_state

## file_metadata_snapshot

Description:
Represents metadata about a file at a given point in time.

- Primary Key file_metadata_snapshot_id
- Foreign Key file_id
- DateTime scan_time
- Int file_size
- String sha256
- DateTime created
- DateTime modified

## file_metadata_snapshot

Description:
Represents a specific file located on a specific machine.

- Primary Key file_id
- Foreign Key machine_id
- String absolute_path

## dedup_session

Description:
Represents a session in which mud analyzed file metadata to identify duplicates.

- Primary Key dedup_session_id
- Foreign Key dedup_state_id
- DateTime dedup_start
- DateTime dedup_stop

## dedup_states

Description:
The states representing the life cycle of a dedup session. Validates scan states for the dedup_session table.

- Primary Key dedup_state_id
- str dedup_state
