import subprocess
import datetime
import os
import shutil
import argparse

# Specify the output directory for the backups and restic repository
base_directory = 'C:\\path\\to\\backups\\'
restic_repo = 'C:\\path\\to\\restic\\repository'
restic_password = 'C:\\path\\to\\restic\\.secret'

def check_vm_running(vm_name):
    """Check if the VirtualBox VM is running."""
    result = subprocess.run(['VBoxManage', 'showvminfo', vm_name], capture_output=True, text=True)
    output = result.stdout
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
    """Perform restic backup of the backup directories."""
    subprocess.run(['restic', '-r', repo, '-p', password, 'backup', vm_directory])

# Generate a timestamp for the backup file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Backup VirtualBox VM')
parser.add_argument('--vm', help='name of the VM to backup')
parser.add_argument('--all', action='store_true', help='backup all VMs')
parser.add_argument('--force', action='store_true', help='Stops the vm without ask in case is running')
args = parser.parse_args()

# If both --vm and --all options are provided, exit the script
if args.vm and args.all:
    parser.error("Please specify either --vm or --all, not both.")

# If neither --vm nor --all option is provided, exit the script
if not args.vm and not args.all:
    args.all = True

# Get the list of VMs to backup
if args.all:
    result = subprocess.run(['VBoxManage', 'list', 'vms'], capture_output=True, text=True)
    output = result.stdout
    vm_list = [line.split(' ')[0].strip('"') for line in output.splitlines()]
else:
    vm_list = [args.vm]

# Iterate over the VMs and perform the backup
for vm_name in vm_list:
    print(f"Backing up VM: {vm_name}")

    # Check if the VM is running
    is_vm_running = check_vm_running(vm_name)

    # Stop the VM before backup if it is running
    if is_vm_running:
        if not args.force:
            # Prompt for user confirmation
            confirmation = input(f"This script will stop the VM '{vm_name}'. Make sure you have saved any important data. Do you want to proceed? (Y/N): ")
            if confirmation.upper() != "Y":
                print("Backup aborted. Skipping VM backup.")
                continue
        print("Powering off VM...")
        stop_vm(vm_name)

    # Create the VM-specific backup directory
    vm_directory = os.path.join(base_directory, vm_name)
    os.makedirs(vm_directory, exist_ok=True)

    # Create the backup file path
    backup_file_path = os.path.join(vm_directory, vm_name.replace(" ", "_") + '_' + timestamp + '.ovf')

    # Perform the VM export
    print("Exporting VM...")
    export_vm(vm_name, backup_file_path)

    # Start the VM if it was previously running
    if is_vm_running:
        print("Starting VM...")
        start_vm(vm_name)

    # Perform restic backup of the backup directory
    print("Performing restic backup...")
    perform_restic_backup(restic_repo, restic_password, vm_directory)

    # Remove the local backup directory
    shutil.rmtree(vm_directory)
    print("Local backup directory removed")

    print(f"Backup completed for VM: {vm_name}")

print("All VM backups completed.")
