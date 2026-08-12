import os
import subprocess
import sys
from datetime import datetime


class GitHubUploader:
    def __init__(self, repo_path, github_url=None):
        """
        Initialize the GitHub Uploader.
        """
        self.repo_path = os.path.abspath(
            os.path.expanduser(repo_path.strip())
        )
        self.github_url = github_url.strip() if github_url else None

    def run_command(self, command):
        """
        Run a terminal command inside the repository directory.
        """
        if not os.path.exists(self.repo_path):
            print(f"❌ Error: Directory not found: {self.repo_path}")
            return False

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ Success: {command}")

                if result.stdout.strip():
                    print(result.stdout.strip())

                return True

            print(f"❌ Error executing: {command}")

            if result.stderr.strip():
                print(f"Details: {result.stderr.strip()}")

            return False

        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

    def init_repo(self):
        """
        Initialize a new Git repository.
        """
        print(f"\n🔧 Initializing Git repository at:")
        print(self.repo_path)

        if not os.path.exists(self.repo_path):
            try:
                os.makedirs(self.repo_path, exist_ok=True)
            except Exception as e:
                print(f"❌ Failed to create directory: {e}")
                return False

        return self.run_command("git init")

    def add_remote(self):
        """
        Add or update the GitHub remote origin.
        """
        if not self.github_url:
            print("⚠️ GitHub URL was not provided.")
            return False

        print("\n🔗 Configuring GitHub remote...")

        # Check whether origin already exists
        check_remote = subprocess.run(
            "git remote get-url origin",
            shell=True,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        if check_remote.returncode == 0:
            # Update existing origin
            return self.run_command(
                f'git remote set-url origin "{self.github_url}"'
            )

        # Add new origin
        return self.run_command(
            f'git remote add origin "{self.github_url}"'
        )

    def add_files(self):
        """
        Add all files to the staging area.
        """
        print("\n📁 Adding files...")
        return self.run_command("git add .")

    def commit_changes(self, message=None):
        """
        Commit staged changes with a custom or automatic message.
        """
        if not message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Auto commit: {timestamp}"

        print(f"\n💾 Creating commit: {message}")

        # Escape double quotes in the commit message
        safe_message = message.replace('"', '\\"')

        result = self.run_command(
            f'git commit -m "{safe_message}"'
        )

        # Git returns an error code when there is nothing to commit.
        # This should not always be treated as a fatal error.
        if not result:
            status_result = subprocess.run(
                "git status --porcelain",
                shell=True,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if not status_result.stdout.strip():
                print("ℹ️ Nothing to commit. Working tree is clean.")
                return True

        return result

    def get_current_branch(self):
        """
        Get the current Git branch name.
        """
        result = subprocess.run(
            "git branch --show-current",
            shell=True,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            branch = result.stdout.strip()

            if branch:
                return branch

        return "main"

    def push_to_github(self, branch=None):
        """
        Push the current branch to GitHub.
        """
        if not branch:
            branch = self.get_current_branch()

        print(f"\n🚀 Pushing to GitHub: {branch}")

        return self.run_command(
            f'git push -u origin "{branch}"'
        )

    def full_upload(self, commit_message=None, branch=None):
        """
        Perform the complete GitHub upload process.
        """
        print("\n" + "=" * 55)
        print("        GITHUB AUTO UPLOADER")
        print("=" * 55)

        # Step 1: Add files
        if not self.add_files():
            print("\n❌ Failed to add files.")
            return False

        # Step 2: Commit changes
        if not self.commit_changes(commit_message):
            print("\n❌ Failed to create commit.")
            return False

        # Step 3: Configure remote
        if self.github_url:
            if not self.add_remote():
                print("\n❌ Failed to configure GitHub remote.")
                return False

        # Step 4: Push to GitHub
        if not self.push_to_github(branch):
            print("\n❌ Failed to push to GitHub.")
            return False

        print("\n" + "=" * 55)
        print("        ✅ UPLOAD COMPLETED SUCCESSFULLY")
        print("=" * 55)

        return True


class InteractiveUploader:
    """
    Interactive console menu for the GitHub Auto Uploader.
    """

    def __init__(self):
        self.uploader = None

    def show_menu(self):
        """
        Display the main menu.
        """
        print("\n" + "=" * 45)
        print("        GITHUB AUTO UPLOADER TOOL")
        print("=" * 45)

        print("\n1. Set Up a New Repository")
        print("2. Upload to an Existing Repository")
        print("3. Upload with Custom Commit Message")
        print("4. Check Git Status")
        print("5. Exit")

    def setup_new_repo(self):
        """
        Set up a new Git repository and upload it to GitHub.
        """
        path = input("\n📂 Enter repository path: ").strip()

        if not path:
            print("❌ Repository path cannot be empty.")
            return

        github_url = input("🔗 Enter GitHub repository URL: ").strip()

        if not github_url:
            print("❌ GitHub URL cannot be empty.")
            return

        self.uploader = GitHubUploader(
            path,
            github_url
        )

        if not self.uploader.init_repo():
            return

        commit_msg = input(
            "\n💬 Enter commit message "
            "(press Enter for automatic message): "
        ).strip()

        self.uploader.full_upload(
            commit_msg if commit_msg else None
        )

    def upload_existing(self, custom_message=False):
        """
        Upload an existing Git repository to GitHub.
        """
        path = input("\n📂 Enter repository path: ").strip()

        full_path = os.path.abspath(
            os.path.expanduser(path)
        )

        if not path or not os.path.exists(full_path):
            print("❌ Please provide a valid existing repository path.")
            return

        # Check whether it is a Git repository
        git_folder = os.path.join(full_path, ".git")

        if not os.path.exists(git_folder):
            print("❌ This directory is not a Git repository.")
            print("💡 Use option 1 to initialize a new repository.")
            return

        commit_msg = input(
            "💬 Enter commit message "
            "(press Enter for automatic message): "
        ).strip()

        branch = input(
            "🌿 Enter branch name "
            "(press Enter for current branch): "
        ).strip()

        self.uploader = GitHubUploader(full_path)

        self.uploader.full_upload(
            commit_msg if commit_msg else None,
            branch if branch else None
        )

    def check_status(self):
        """
        Check the Git status of a repository.
        """
        path = input("\n📂 Enter repository path: ").strip()

        full_path = os.path.abspath(
            os.path.expanduser(path)
        )

        if not path or not os.path.exists(full_path):
            print("❌ Please provide a valid repository path.")
            return

        print(f"\n📊 Git status for:")
        print(full_path)
        print()

        subprocess.run(
            "git status",
            shell=True,
            cwd=full_path
        )

    def run(self):
        """
        Start the interactive menu.
        """
        while True:
            self.show_menu()

            choice = input(
                "\n👉 Enter your choice (1-5): "
            ).strip()

            if choice == "1":
                self.setup_new_repo()

            elif choice == "2":
                self.upload_existing()

            elif choice == "3":
                self.upload_existing(custom_message=True)

            elif choice == "4":
                self.check_status()

            elif choice == "5":
                print("\n👋 Goodbye! Happy Coding!")
                sys.exit(0)

            else:
                print("\n⚠️ Invalid choice. Please try again.")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    app = InteractiveUploader()
    app.run()
