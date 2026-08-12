import subprocess
import os


def quick_github_push(message="Update files"):
    """
    Quickly add, commit, and push changes to GitHub.
    """

    # Check whether the current directory is a Git repository
    if not os.path.exists(".git"):
        print("❌ Error: This is not a Git repository.")
        print("💡 Run 'git init' first.")
        return False

    # Escape double quotes in the commit message
    safe_message = message.replace('"', '\\"')

    commands = [
        "git add .",
        f'git commit -m "{safe_message}"',
        "git push"
    ]

    # Run commands one by one
    for command in commands:
        print(f"\n▶ Running: {command}")

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            # Handle the case where there are no changes to commit
            if (
                "nothing to commit" in result.stderr.lower()
                or "nothing to commit" in result.stdout.lower()
            ):
                print("ℹ️ No changes detected. Continuing to push...")
                continue

            print(f"❌ Command failed: {command}")

            if result.stderr.strip():
                print(f"Details: {result.stderr.strip()}")

            return False

        # Display command output if available
        if result.stdout.strip():
            print(result.stdout.strip())

    print("\n✅ Done! Changes have been pushed to GitHub.")
    return True


# Usage
if __name__ == "__main__":
    quick_github_push("Added new feature")
