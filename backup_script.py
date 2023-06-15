import subprocess
import datetime
import os

# Specify your VM name and output directory for the backups
vm_name = 'your_vm_name'
base_directory = 'C:\\path\\to\\backups\\'
retention_limit = 5

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
    stop_vm(vm_name)

# Perform the backup
export_vm(vm_name, backup_file_path)

# Start the VM if it was previously running
if is_vm_running:
    start_vm(vm_name)

# Remove older backups if retention limit exceeded
existing_backups = os.listdir(vm_directory)
backups_to_remove = len(existing_backups) - retention_limit
if backups_to_remove > 0:
    sorted_backups = sorted(existing_backups)
    for i in range(backups_to_remove):
        backup_to_remove = os.path.join(vm_directory, sorted_backups[i])
        os.remove(backup_to_remove)
