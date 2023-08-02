# VirtualBox VM Backup Script

This script is designed to perform backups of VirtualBox VMs and create snapshots using restic for efficient storage. It provides options to backup a specific VM or all VMs on the system.

## Requirements

- VirtualBox
- restic (https://restic.net/) with an initialized repository for storage

## Usage

```bash
python backup_script.py --vm <VM_NAME>
```

- Backup a specific VM named `<VM_NAME>`.

```bash
python backup_script.py --all
```

- Backup all VMs on the system.

## Additional Options

### `--force`

```bash
python backup_script.py --vm <VM_NAME> --force
```

- Backup a specific VM without prompting to stop the VM, even if it is running.

## Configuration

Before running the script, make sure to configure the following variables in the script:

```python
# Specify the output directory for the backups
base_directory = 'C:\\path\\to\\backups\\'

# Specify the restic repository path
restic_repo = 'C:\\path\\to\\restic\\repository'

# Specify the path to the restic password file
restic_password = 'C:\\path\\to\\restic\\.secret'
```

## Important Notes

- This script requires VirtualBox and restic to be properly installed and configured on your system.
- The script will export each VM to an OVF file and perform a restic backup for each VM individually. Snapshots will be created for efficient storage.
- If the `--force` option is used, the script will stop a running VM without asking for user confirmation.
- The exported OVF files and backup snapshots will be stored in the specified `base_directory`.
- Restic snapshots will be created in the specified `restic_repo` for easy management and restoration.

## Disclaimer

This script is provided as-is without any warranties. Use it at your own risk and ensure you have tested it thoroughly in your specific environment before using it in production.
