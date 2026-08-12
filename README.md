# GitHub Auto Uploader Tool 🚀

এটি একটি Python-based automation tool, যার সাহায্যে খুব সহজেই terminal থেকে যেকোনো local project GitHub-এ upload এবং update করা যায়।

## Features

- 🔧 নতুন Git Repository setup করা।
- 📁 Project-এর সব files একসাথে GitHub-এ push করা।
- 💾 Automatic অথবা custom commit message ব্যবহার করা।
- 🌿 Custom branch select করে push করা।
- 🔗 GitHub remote URL configure করা।
- 📊 সহজে Git status check করা।
- ⚡ `push.py` ব্যবহার করে দ্রুত changes push করা।
- 🛡️ Basic Git error handling এবং safety checks রয়েছে।

## Requirements

এই tool ব্যবহার করার আগে আপনার computer-এ এগুলো install থাকতে হবে:

- Python 3.x
- Git
- GitHub account
- একটি GitHub repository

## How to Use

প্রথমে project folder-এ terminal খুলুন।

তারপর main uploader চালান:

```bash
python github_uploader.py
```

চালানোর পর একটি interactive menu দেখতে পাবেন:
```
1. Set Up a New Repository
2. Upload to an Existing Repository
3. Upload with Custom Commit Message
4. Check Git Status
5. Exit
```
আপনার প্রয়োজন অনুযায়ী option select করুন।

Option 1: New Repository Setup

নতুন কোনো local project GitHub-এ upload করতে:

Set Up a New Repository select করুন।
আপনার local project path দিন।
আপনার GitHub repository URL দিন।
একটি commit message দিন অথবা automatic message-এর জন্য Enter চাপুন।
Branch name প্রয়োজন হলে দিন।
Tool automatically files add, commit এবং push করবে।

Option 2: Existing Repository Upload

আগে থেকেই Git repository থাকা কোনো project update করতে:

Upload to an Existing Repository select করুন।
Repository path দিন।
Commit message দিন।
Branch name দিন অথবা Enter চাপলে current branch ব্যবহার হবে।
Tool automatically changes GitHub-এ push করবে।
Option 3: Custom Commit Message

নিজের পছন্দমতো commit message দিয়ে upload করতে পারবেন।

Example:

Added calculator history feature

অথবা:

Fixed login page bug
Option 4: Check Git Status

এই option দিয়ে repository-এর current Git status দেখতে পারবেন।

এতে জানা যাবে:

কোন files modified হয়েছে
কোন files staged হয়েছে
কোন files untracked রয়েছে
Repository clean কিনা
Quick Push

যদি শুধু দ্রুত changes GitHub-এ push করতে চান, তাহলে:
```
python push.py
```
এটি automatically:

Git Add → Git Commit → Git Push

এই তিনটি কাজ করবে।

Example Output
=======================================================
        GITHUB AUTO UPLOADER
=======================================================

📁 Adding files...

💾 Creating commit: Added new feature

🔗 Configuring GitHub remote...

🚀 Pushing to GitHub: main

=======================================================
        ✅ UPLOAD COMPLETED SUCCESSFULLY
=======================================================
Project Structure
github-auto-uploader/
│
├── github_uploader.py
├── push.py
└── README.md


**File Description**
github_uploader.py → Main interactive GitHub uploader.
push.py → Quick GitHub push utility.
README.md → Project documentation.

**Important Notes**
আপনার system-এ Git এবং Python properly installed থাকতে হবে।
GitHub authentication আগে থেকে configured থাকতে হবে।
Push করার সময় সঠিক GitHub repository URL ব্যবহার করুন।
কোনো password, API key, token বা sensitive information GitHub-এ upload করবেন না।
Sensitive files থাকলে .gitignore ব্যবহার করুন।
Future Improvements

এই project-এ ভবিষ্যতে আরও features যোগ করা যেতে পারে:

🤖 GitHub API দিয়ে automatically repository create করা।
🔐 Better GitHub authentication system।
📄 Automatic .gitignore generation।
🖥️ GUI version তৈরি করা।
🚀 GitHub Release automation।
🌿 Advanced branch management।
🤖 AI-based automatic commit message generation।

**License**
```
This project is open source and can be used for educational and personal purposes.
