import subprocess
import os

def print_banner():
    banner = """
    ****************************************
    *                                      *
    *            GIT RESET                 *
    *          Let's try again...          *
    *                                      *
    ****************************************
    """
    print(banner)

def prompt_user():
    while True:
        response = input("Are you sure you want to perform a hard reset? (y/n): ").strip().lower()
        if response in ['y', 'n']:
            return response
        print("Invalid input. Please enter 'y' or 'n'.")

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing '{command}':")
        print(error.decode('utf-8'))
        return False
    print(output.decode('utf-8'))
    return True

def main():
    print_banner()

    response = prompt_user()
    if response == 'n':
        print("Operation canceled.")
        return

    print("Fetching latest changes from remote...")
    if not run_command("git fetch origin"):
        return

    print("Determining current branch...")
    branch = subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True).decode('utf-8').strip()
    print(f"Current branch: {branch}")

    print(f"Resetting local branch to match origin/{branch}...")
    if not run_command(f"git reset --hard origin/{branch}"):
        return

    print("Cleaning up untracked files and directories...")
    if not run_command("git clean -fd"):
        return

    print("Checking final status...")
    run_command("git status")

    print("Repository has been successfully reset to match the remote.")

if __name__ == "__main__":
    main()
