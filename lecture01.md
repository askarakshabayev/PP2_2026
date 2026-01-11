# Lecture 1: Course Introduction & Getting Started with Python

## Course Overview: Programming Principles 2

### Course Syllabus (https://docs.google.com/document/d/1U4zZv1ZJKPCb0F27gUTFfsKxnscaRrIhicOgWKmAl3I/edit?usp=sharing)

### Assessment & Grading (https://docs.google.com/spreadsheets/d/1VMWG-9Vj9HrT_BMkLcZ_nxMuc8lb_KPXnrmGkpB7JQ4/edit?usp=sharing)

### Attendance
- Standard KBTU attendance rules apply

### Laboratory Works (TODO: Link to laboratory work)
- Weekly assignments must be completed
- All code must be uploaded to GitHub before the deadline

### Quizzes
- **Quiz 1**: Week 4 (February 15) - Contest on ejudge
- **Quiz 2**: Week 8 (March 15) - Contest on ejudge
- **Quiz 3**: Week 12 - Regular quiz
- **Note**: On contest weeks, there will be no regular lectures

### Final Project
- **Week 15**: Project defense
- No lectures during project defense week

---

## Useful Resources

### Official Documentation
- **Python Documentation**: https://docs.python.org/3/using/index.html
- **Download Python**: https://www.python.org/downloads/

### Learning Resources
- **W3Schools Python Tutorial**: https://www.w3schools.com/python/
- **Git How To**: https://githowto.com/

---

## Lecture 1 Content

### 1. Course Introduction

Welcome to Programming Principles 2! This course builds upon the fundamentals you learned in PP1 and dives deeper into Python programming. By the end of this course, you will:

- Master Python programming fundamentals
- Understand object-oriented programming concepts (basic)
- Work with files, databases, and external libraries
- Create interactive games using Pygame
- Collaborate effectively using Git and GitHub

---

### 2. Essential Tools

We'll be using four primary tools in this course:

1. **VSCode** - Code editor
2. **Python** - Programming language
3. **Git** - Version control system
4. **GitHub** - Code hosting platform

---

### 4. Installing Python

Python is the programming language we'll use throughout this course. You need to install it on your computer.

#### **Windows Installation**

1. Visit https://www.python.org/downloads/
2. Download the latest Python 3.x version
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Click "Install Now"
6. Verify installation:
   ```bash
   python --version
   ```

#### **macOS Installation**

**Method 1: Official Installer**
1. Visit https://www.python.org/downloads/
2. Download the macOS installer
3. Run the .pkg file
4. Follow installation prompts
5. Verify installation:
   ```bash
   python3 --version
   ```

**Method 2: Homebrew (Recommended)**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

#### **Linux Installation**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```
---

### 4. Installing VSCode

VSCode is a powerful, free code editor that we'll use for writing Python code.

#### **All Platforms**

1. Visit https://code.visualstudio.com/
2. Download for your operating system
3. Install the application
4. Launch VSCode

---

### 5. What is Git?

**Git** is a version control system that helps you:
- Track changes in your code over time
- Collaborate with others
- Revert to previous versions if something breaks
- Manage different versions of your project

Think of Git as a "time machine" for your code!

#### **Why Do We Need Git?**

Imagine you're writing code and:
- You make changes that break everything
- You want to try a new feature without affecting your working code
- Multiple people need to work on the same project
- You need to submit assignments and track your progress

Git solves all these problems!

---

### 6. Installing Git

#### **Windows**

1. Download Git from https://git-scm.com/download/win
2. Run the installer
3. Use default settings (just keep clicking "Next")
4. **Important selections**:
   - Choose "Git from the command line and also from 3rd-party software"
   - Use "Use Windows' default console window"
5. Verify installation:
   ```bash
   git --version
   ```

#### **macOS**

**Method 1: Xcode Command Line Tools**
```bash
xcode-select --install
```

**Method 2: Homebrew**
```bash
brew install git
```

Verify installation:
```bash
git --version
```

#### **Linux**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install git
```

Verify installation:
```bash
git --version
```

---

### 7. Working with Git

Now let's learn the basics of Git! We'll follow the first 13 exercises from [Git How To](https://githowto.com/).

#### **Exercise 1-2: Setup**

Configure your identity (Git needs to know who you are):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### **Exercise 3: Creating a Repository**

1. Create a new directory for your project:
   ```bash
   mkdir hello_world
   cd hello_world
   ```

2. Initialize a Git repository:
   ```bash
   git init
   ```

This creates a hidden `.git` folder that tracks all changes.

#### **Exercise 4: Checking Status**

```bash
git status
```

This shows:
- Which files are modified
- Which files are staged for commit
- Which files are untracked

#### **Exercise 5: Making Changes**

1. Create a file:
   ```bash
   echo "print('Hello, World!')" > hello.py
   ```

2. Check status:
   ```bash
   git status
   ```

You'll see `hello.py` is untracked.

#### **Exercise 6: Staging Changes**

Before committing, you need to "stage" files:

```bash
git add hello.py
```

Now check status again:
```bash
git status
```

The file is now "staged" and ready to commit.

#### **Exercise 7: Committing**

Save the staged changes with a commit:

```bash
git commit -m "Add hello world script"
```

The `-m` flag lets you add a message describing your changes.

#### **Exercise 8: Making More Changes**

1. Modify the file:
   ```bash
   echo "print('Git is awesome!')" >> hello.py
   ```

2. Check what changed:
   ```bash
   git diff
   ```

3. Stage and commit:
   ```bash
   git add hello.py
   git commit -m "Add additional print statement"
   ```

#### **Exercise 9: History**

View your commit history:

```bash
git log
```

For a more compact view:
```bash
git log --oneline
```

#### **Exercise 10: Checking Out Previous Versions**

You can view your project at any previous commit:

```bash
git log --oneline
# Copy a commit hash
git checkout <commit-hash>
```

To return to the latest version:
```bash
git checkout main
```
(or `master`, depending on your default branch name)

---

### 10. GitHub and How It Relates to Git

#### **What is GitHub?**

- **Git**: A tool on your computer for version control
- **GitHub**: A website that hosts Git repositories online

Think of it this way:
- **Git** = Microsoft Word (the tool)
- **GitHub** = Google Drive (where you store and share)

#### **Why Use GitHub?**

1. **Backup**: Your code is stored safely online
2. **Collaboration**: Multiple people can work on the same project
3. **Portfolio**: Showcase your projects to potential employers
4. **Submission**: You'll submit your TSISs via GitHub

---

### 11. Setting Up GitHub with Git

#### **Step 1: Create a GitHub Account**

1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration process
4. Verify your email

#### **Step 2: Connect Git to GitHub**

You've already configured your name and email. Now let's set up authentication.

**Using Personal Access Token (Recommended)**

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "My Laptop")
4. Select scopes: `repo`, `workflow`
5. Click "Generate token"
6. **IMPORTANT**: Copy the token immediately (you won't see it again!)

When pushing to GitHub, use the token as your password.

**Using SSH (Alternative)**

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

Add the public key to GitHub: Settings → SSH and GPG keys → New SSH key

#### **Step 3: Create a Repository on GitHub**

1. Click the "+" icon → "New repository"
2. Name it (e.g., "pp2-lab-works")
3. Choose "Public" or "Private"
4. Don't initialize with README (we'll push existing code)
5. Click "Create repository"

#### **Step 4: Link Local Repository to GitHub**

```bash
# Add remote repository
git remote add origin https://github.com/yourusername/pp2-lab-works.git

# Verify remote
git remote -v

# Push your code
git push -u origin main
```

If your default branch is `master` instead of `main`:
```bash
git push -u origin master
```

---

### 12. Git Workflow: Stage, Commit, Push

Here's the typical workflow you'll use for assignments:

#### **Step 1: Make Changes**
Write or modify your code files.

#### **Step 2: Check Status**
```bash
git status
```
See which files have changed.

#### **Step 3: Stage Changes**
```bash
# Stage specific file
git add filename.py

# Stage all changes
git add .
```

#### **Step 4: Commit Changes**
```bash
git commit -m "Descriptive message about what you changed"
```

**Good commit messages:**
- ✅ "Add function to calculate factorial"
- ✅ "Fix bug in user input validation"
- ✅ "Complete exercise 3 from TSIS 1"

**Bad commit messages:**
- ❌ "Update"
- ❌ "Changes"
- ❌ "asdfasdf"

#### **Step 5: Push to GitHub**
```bash
git push
```

This uploads your commits to GitHub.

#### **Complete Example Workflow**

```bash
# 1. Create/modify files
echo "def greet(name):" > functions.py
echo "    return f'Hello, {name}!'" >> functions.py

# 2. Check status
git status

# 3. Stage changes
git add functions.py

# 4. Commit
git commit -m "Add greeting function"

# 5. Push to GitHub
git push
```

---

### 13. Introduction to Python

Now that we have our tools set up, let's write some Python!

#### **Your First Python Program**

Create a file called `hello.py`:

```python
print("Hello, World!")
```

Run it:
```bash
python hello.py
# or on macOS/Linux:
python3 hello.py
```

#### **Python Basics - Quick Examples**

**Variables and Data Types:**
```python
# Variables
name = "Alice"
age = 20
height = 1.65
is_student = True

# Print
print(f"Name: {name}, Age: {age}")
```

**User Input:**
```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```

**Conditions:**
```python
age = int(input("Enter your age: "))

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

**Loops:**
```python
# For loop
for i in range(5):
    print(f"Number: {i}")

# While loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1
```

#### **Where to Learn More**

For detailed Python tutorials, visit:
- **W3Schools**: https://www.w3schools.com/python/

Work through the following sections on W3Schools:
1. Python Intro
2. Python Get Started
3. Python Syntax
4. Python Variables
5. Python Data Types
6. Python Operators
7. Python If...Else

---

### 14. Working with Teaching Assistants

#### **How to Get Help**

1. **Office Hours**: TAs will have scheduled office hours
2. **Online Communication**: Use designated communication channels (e.g., Discord, Telegram)
3. **Email**: For administrative questions

#### **When to Ask for Help**

✅ **DO ask when:**
- You've tried to solve the problem for 15-20 minutes
- You've searched online but don't understand the solutions
- You need clarification on assignment requirements
- You're getting an error you can't debug

❌ **DON'T ask for:**
- Complete solutions to assignments
- Someone to write your code for you

#### **How to Ask Good Questions**

**Bad question:**
> "My code doesn't work. Help!"

**Good question:**
> "I'm trying to read a file in Python, but I'm getting a FileNotFoundError. Here's my code:
> ```python
> with open('data.txt', 'r') as file:
>     content = file.read()
> ```
> I verified that data.txt is in the same folder. What am I doing wrong?"

Include:
1. What you're trying to do
2. What you expected to happen
3. What actually happened
4. What you've already tried

---

## Next Steps

Before the next lecture:

1. ✅ Install Python, VSCode, and Git
2. ✅ Create a GitHub account
3. ✅ Complete the first 10 exercises on [Git How To](https://githowto.com/)
4. ✅ Work through Python basics on [W3Schools](https://www.w3schools.com/python/)
5. ✅ Create a test repository and practice: stage, commit, push

---

## Summary

Today we covered:
- Course syllabus and grading system
- Essential tools: Python, VSCode, Git, GitHub
- Installing Python on different operating systems
- Understanding files and file systems
- What Git is and why we use it
- Basic Git commands and workflow
- How GitHub relates to Git
- Python introduction and basics
- How to work effectively with TAs

**Remember**: The best way to learn programming is by doing. Practice Git commands, write Python code, and don't be afraid to make mistakes!

---

**Questions?** Ask your TAs or instructor during office hours.

**Next Lecture**: Python Fundamentals - Data Types, Operators, and Control Flow
