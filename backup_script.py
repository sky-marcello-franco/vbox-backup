import subprocess
import datetime
import os
import shutil

# Specify your VM name, output directory for the backups, and restic repository
vm_name = 'your_vm_name'
base_directory = 'C:\\path\\to\\backups\\'
restic_repo = 'C:\\path\\to\\restic\\repository'
restic_password = 'C:\\path\\to\\restic\\.secret'

def check_vm_running(vm_name):
    """Check if the VirtualBox VM is running."""
    result = subprocess.run(['VBoxManage', 'showvminfo', vm_name], capture_output=True)
    output = result.stdout.decode('utf-8')
    return "running (since" in output

def stop_vm(vm_name):
    """Stop the VirtualBox VM."""
    subprocess.run(['VBoxManage', 'controlvm', vm_name, 'poweroff'])

def start_vm(vm_name):
    """Start the VirtualBox VM."""
    subprocess.run(['VBoxManage', 'startvm', vm_name, '--type', 'headless'])

def export_vm(vm_name, output_path):
    """Export the VirtualBox VM to an OVF file."""
    subprocess.run(['VBoxManage', 'export', vm_name, '--output', output_path])

def perform_restic_backup(repo, password, vm_directory):
    """Perform restic backup of the backup directory."""
    subprocess.run(['restic', '-r', repo, '-p', password,  'backup', vm_directory])

# Generate a timestamp for the backup file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Create the VM-specific backup directory
vm_directory = os.path.join(base_directory, vm_name)
os.makedirs(vm_directory, exist_ok=True)

# Create the backup file path
backup_file_path = os.path.join(vm_directory, vm_name + '_' + timestamp + '.ovf')

# Check if VM is running
is_vm_running = check_vm_running(vm_name)

# Stop the VM before backup if it was running
if is_vm_running:
    # Prompt for user confirmation
    confirmation = input("This script will stop the specified VM. Make sure you have saved any important data. Do you want to proceed? (Y/N): ")
    if confirmation.upper() != "Y":
        print("Backup aborted. Exiting the script.")
        exit()
    print("Power off VM: ", end='', flush=True)
    stop_vm(vm_name)

# Perform the backup
print("Backup Started: ", end='', flush=True)
export_vm(vm_name, backup_file_path)

# Start the VM if it was previously running
if is_vm_running:
    print("Restarting VM: ", end='', flush=True)
    start_vm(vm_name)

# Perform restic backup of the backup directory
print("INFO: Performing restic backup: ")
perform_restic_backup(restic_repo, restic_password, vm_directory)

# Remove local backup directory
shutil.rmtree(vm_directory)
print("INFO: Local backup directory removed")

print("Backup completed successfully.")
