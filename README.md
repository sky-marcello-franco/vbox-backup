# VirtualBox VM Backup Script

This script allows you to create scheduled backups of a VirtualBox VM on Windows. It exports the VM to an OVF (Open Virtualization Format) file, providing a convenient way to back up the VM's disk and configuration.

## Prerequisites

- **VirtualBox**: Ensure that VirtualBox is installed on your Windows system.
- **Python**: Install Python (version 3 or higher) on your Windows system.

## Usage

1. Clone or download the script file to your local machine.

2. Open the script file in a text editor.

3. Locate the `vm_name` variable in the script. Replace `'YOUR_VM_NAME'` with the actual name or UUID of the VirtualBox VM you want to back up.

4. Locate the base_directory variable in the script. Modify the variable to specify the base directory where you want the backups to be stored.

5. Save the changes to the script file.

6. Open a command prompt and navigate to the directory containing the script.

7. Run the script with the following command:

   ```bash
   python backup_script.py
   ```

8. The script will perform the following steps:

   - Check if the specified VM is running. If it is, it will stop the VM.
   - Export the VM to an OVF file in the specified backup directory.
   - Start the VM again if it was previously running.
   - Maintain a retention policy of 5 backups, removing older backups if necessary.

9. The backup files will be stored in the backup directory in the following format:

   ```
   <backup_directory>/<vm_name>/<vm_name>_<timestamp>.ovf
   ```

## Customization

- **Backup Directory**: Modify the `base_directory` variable in the script to specify the base directory where the backups will be stored.

- **Retention Policy**: By default, the script retains the latest 5 backups. Modify the `retention_limit` variable in the script to adjust the number of backups to retain.

## Important Note

- The script requires VirtualBox to be installed and accessible via the command-line (`VBoxManage` command). 

- It is recommended to schedule the script to run regularly using a task scheduler (e.g., Windows Task Scheduler) to automate the backup process.

Feel free to modify and adapt the script according to your specific requirements.

## License

This script is released under the MIT License. Please see the [LICENSE](LICENSE) file for more details.

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk. Make sure to test the script thoroughly and ensure the integrity of your backups.

Please refer to the original script for the full code and any additional functions or details not covered in this README.md summary.