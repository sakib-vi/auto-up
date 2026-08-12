import os
import subprocess
import sys
from datetime import datetime

class GitHubUploader:
    def __init__(self, repo_path, github_url=None):
        # পাথের স্পেস ট্রিম করা এবং ইউজার ডিরেক্টরি (~), রিলে티브 পাথকে অ্যাবসোলিউট পাথে রূপান্তর করা
        self.repo_path = os.path.abspath(os.path.expanduser(repo_path.strip()))
        self.github_url = github_url.strip() if github_url else None

    def run_command(self, command):
        """টার্মিনালে কমান্ড রান করার সাধারণ মেথড"""
        if not os.path.exists(self.repo_path):
            print(f"❌ Error: ডিরেক্টরি খুঁজে পাওয়া যায়নি: {self.repo_path}")
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
            else:
                print(f"❌ Error executing: {command}")
                print(f"Details: {result.stderr.strip()}")
                return False
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

    def init_repo(self):
        """নতুন Git repository ডিরেক্টরিতে চালু করা"""
        print(f"\n🔧 Initializing Git Repository at {self.repo_path}...")
        if not os.path.exists(self.repo_path):
            try:
                os.makedirs(self.repo_path, exist_ok=True)
            except Exception as e:
                print(f"❌ ডিরেক্টরি তৈরি করা সম্ভব হয়নি: {e}")
                return False
        return self.run_command("git init")

    def add_remote(self):
        """GitHub রিমোট অরিজিন যুক্ত করা"""
        if self.github_url:
            print("\n🔗 Adding remote origin...")
            # পূর্ববর্তী কোনো অরিজিন থাকলে কনф্লিক্ট এড়াতে তা রিমুভ করে নতুনটি সেট করা হচ্ছে
            self.run_command("git remote remove origin")
            return self.run_command(f"git remote add origin {self.github_url}")
        return False

    def add_files(self):
        """সব ফাইল স্টেজিং এরিয়াতে (Staging Area) যুক্ত করা"""
        print("\n📁 Adding files...")
        return self.run_command("git add .")

    def commit_changes(self, message=None):
        """কাস্টম অথবা অটোমেটিক মেসেজ দিয়ে পরিবর্তনগুলো কমিট করা"""
        if not message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Auto commit: {timestamp}"
        print(f"\n💾 Committing: {message}")
        
        # মেসেজে ডাবল কোট থাকলে তা এস্কেপ করা যেন褪েল কমান্ডে ইরর না আসে
        safe_message = message.replace('"', '\\"')
        return self.run_command(f'git commit -m "{safe_message}"')

    def push_to_github(self, branch="main"):
        """GitHub রিমোট রিপোজিটরিতে কোড পুশ করা"""
        print(f"\n🚀 Pushing to {branch} branch...")
        return self.run_command(f"git push -u origin {branch}")

    def full_upload(self, commit_message=None, branch="main"):
        """সম্পূর্ণ আপলোড প্রক্রিয়াটি ধাপে ধাপে সম্পন্ন করা"""
        print("=" * 50)
        print("🎯 STARTING GITHUB AUTO UPLOAD")
        print("=" * 50)
        
        if not self.add_files():
            print("❌ Failed to add files to staging area.")
            return False
            
        self.commit_changes(commit_message)
        
        if self.github_url:
            self.add_remote()
            
        self.push_to_github(branch)
        print("\n" + "=" * 50)
        print("✨ UPLOAD COMPLETE!")
        print("=" * 50)

class InteractiveUploader:
    """ইন্টারেক্টিভ কনসোল মেনু সিস্টেম"""
    def __init__(self):
        self.uploader = None

    def show_menu(self):
        print("\n" + "=" * 40)
        print("      GITHUB AUTO UPLOADER TOOL")
        print("=" * 40)
        print("\n1. নতুন Repository Setup করুন")
        print("2. Existing Repository তে Upload করুন")
        print("3. Custom Commit Message দিয়ে Upload")
        print("4. শুধু Status চেক করুন")
        print("5. Exit")

    def setup_new_repo(self):
        path = input("\n📂 Repository path দিন: ").strip()
        if not path:
            print("❌ Path ফাঁকা রাখা যাবে না!")
            return
        github_url = input("🔗 GitHub URL দিন: ").strip()
        if not github_url:
            print("❌ GitHub URL ফাঁকা রাখা যাবে না!")
            return
            
        self.uploader = GitHubUploader(path, github_url)
        self.uploader.init_repo()
        commit_msg = input("\n💬 Commit message দিন (Enter চাপলে auto): ").strip()
        self.uploader.full_upload(commit_msg if commit_msg else None)

    def upload_existing(self):
        path = input("\n📂 Repository path দিন: ").strip()
        if not path or not os.path.exists(os.path.abspath(os.path.expanduser(path))):
            print("❌ সঠিক এবং বিদ্যমান Repository Path প্রদান করুন!")
            return
        commit_msg = input("💬 Commit message (Enter চাপলে auto-generated): ").strip()
        branch = input("🌿 Branch name (default: main): ").strip() or "main"
        
        self.uploader = GitHubUploader(path)
        self.uploader.full_upload(
            commit_msg if commit_msg else None,
            branch
        )

    def check_status(self):
        path = input("\n📂 Repository path din: ").strip()
        full_path = os.path.abspath(os.path.expanduser(path))
        if not path or not os.path.exists(full_path):
            print("❌ সঠিক এবং বিদ্যমান Repository Path প্রদান করুন!")
            return
        
        print(f"\n📊 Checking git status for: {full_path}")
        subprocess.run("git status", shell=True, cwd=full_path)

    def run(self):
        while True:
            self.show_menu()
            choice = input("\n👉 Choice দিন (1-5): ").strip()
            if choice == "1":
                self.setup_new_repo()
            elif choice == "2" or choice == "3":
                self.upload_existing()
            elif choice == "4":
                self.check_status()
            elif choice == "5":
                print("\n👋 Goodbye! Happy Coding!")
                sys.exit()
            else:
                print("\n⚠️ Invalid choice! আবার চেষ্টা করুন।")
                input("\n⏸️ চালিয়ে যেতে Enter চাপুন...")

if __name__ == "__main__":
    app = InteractiveUploader()
    app.run()
