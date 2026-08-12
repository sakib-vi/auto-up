import subprocess
import os

def quick_github_push(message="Update files"):
    """One-line GitHub push function with safety checks"""
    # ১. কারেন্ট ডিরেক্টরিতে .git ফোল্ডার আছে কিনা তা চেক করা
    if not os.path.exists(".git"):
        print("❌ Error: এটি কোনো Git repository নয়! প্রথমে 'git init' করুন।")
        return

    # ২. কমিট মেসেজের ডাবল কোট এস্কেপ করা যাতে শেল কমান্ড ক্র্যাশ না করে
    safe_message = message.replace('"', '\\"')

    commands = [
        "git add .",
        f'git commit -m "{safe_message}"',
        "git push"
    ]
    
    # ৩. কমান্ডগুলো ধাপে ধাপে রান করা এবং কোনো একটি ফেইল করলে থামানো
    for cmd in commands:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # কোনো কারণে কমান্ড ফেইল করলে (যেমন: commit করার মতো কোনো পরিবর্তন না থাকলে)
        if result.returncode != 0:
            # যদি 'nothing to commit' মেসেজ আসে, তবে পুশ স্কিপ করা যেতে পারে
            if "nothing to commit" in result.stderr or "nothing to commit" in result.stdout:
                print("ℹ️ No changes detected to commit.")
                continue
            else:
                print(f"❌ Error in command: {cmd}")
                print(f"Details: {result.stderr.strip()}")
                return
    
    print("✅ Done! Files uploaded to GitHub")

# Usage
if __name__ == "__main__":
    quick_github_push("Added new feature")
