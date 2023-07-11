import subprocess
import datetime
import os
import shutil

# Specify your VM name, output directory for the backups, and restic repository
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

def perform_restic_backup(repo, password, backup_directories):
    """Perform restic backup of the backup directories."""
    restic_args = ['restic', '-r', repo, '-p', password, 'backup']
    restic_args.extend(backup_directories)
    subprocess.run(restic_args)

# Generate a timestamp for the backup file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Backup VirtualBox VM')
parser.add_argument('--vm', help='name of the VM to backup')
parser.add_argument('--all', action='store_true', help='backup all VMs')
args = parser.parse_args()

# If both --vm and --all options are provided, exit the script
if args.vm and args.all:
    parser.error("Please specify either --vm or --all, not both.")

# If neither --vm nor --all option is provided, exit the script
if not args.vm and not args.all:
    parser.error("Please specify the name of the VM to backup using the --vm option, or use --all to backup all VMs.")

# Get the list of VMs to backup
if args.all:
    result = subprocess.run(['VBoxManage', 'list', 'vms'], capture_output=True, text=True)
    output = result.stdout
    vm_list = [line.split(' ')[0].strip('"') for line in output.splitlines()]
else:
    vm_list = [args.vm]

# Create a list of backup directories for restic
backup_directories = []

# Perform the backup for each VM
for vm_name in vm_list:
    print(f"Backing up VM: {vm_name}")

    # Check if the VM is running
    is_vm_running = check_vm_running(vm_name)

    # Stop the VM before backup if it is running
    if is_vm_running:
        # Prompt for user confirmation
        confirmation = input(f"This script will stop the VM '{vm_name}'. Make sure you have saved any important data. Do you want to proceed? (Y/N): ")
        if confirmation.upper() != "Y":
            print("Backup aborted. Skipping VM backup.")
            continue

        print("Powering off VM...")
        stop_vm(vm_name)

    # Create the VM-specific backup directory
    vm_directory = os.path.join(base_directory, vm_name.replace(" ", "_"))
    os.makedirs(vm_directory, exist_ok=True)

    # Create the backup file path
    backup_file_path = os.path.join(vm_directory, vm_name.replace(" ", "_") + '_' + timestamp + '.ovf')

    # Export the VM
    print("Exporting VM...")
    export_vm(vm_name, backup_file_path)

    # Start the VM if it was previously running
    if is_vm_running:
        print("Starting VM...")
        start_vm(vm_name)

    # Add the VM directory to the backup directories list
    backup_directories.append(vm_directory)

# Perform the restic backup of all backup directories
print("Performing restic backup...")
perform_restic_backup(restic_repo, restic_password, backup_directories)

# Remove the VM-specific backup directories
for vm_directory in backup_directories:
    shutil.rmtree(vm_directory)

print("Backup completed successfully.")
