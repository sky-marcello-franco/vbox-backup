# VirtualBox VM Backup Script

This script allows you to create scheduled backups of a VirtualBox VM on Windows.

## Prerequisites

- Python 3.x installed
- VirtualBox installed and added to the system's PATH
- Restic installed and added to the system's PATH

## Usage

1. Modify the following variables at the top of the script according to your environment:
   - `base_directory`: Specify the base directory where you want to store the backups.
   - `restic_repo`: Specify the path to your Restic repository.
   - `restic_password`: Specify the password for your Restic repository.

2. Open a command prompt or terminal.

3. Navigate to the directory where the script is located.

4. Run the script using the following command:

   ```shell
   python backup_script.py --vm [vmname]
   ```

   This will initiate the backup process. You can either specify the name of the VM to backup using the --vm option, or use --all to backup all VMs.

5. The script will prompt you to confirm if you want to stop the specified VM before the backup. Make sure you have saved any important data. Enter `Y` to proceed or `N` to abort.

6. The script will start the backup process and display the progress.

7. Once the backup is completed, Restic will be invoked to create a backup of the backup directory in the specified Restic repository.

8. After the Restic backup is created, the local backup files will be deleted.

## Notes

It is recommended to schedule the script to run regularly using a task scheduler (e.g., Windows Task Scheduler) to automate the backup process.

## License

This script is released under the [MIT License](LICENSE).

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk. Make sure to test the script thoroughly and ensure the integrity of your backups.

Please refer to the original script for the full code and any additional functions or details not covered in this README.md summary.