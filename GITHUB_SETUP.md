# Setting Up Your GitHub Repository

Follow these steps to initialize and push your YouTubeAutoBackupTool project to GitHub:

## Step 1: Initialize Git Repository (if not already done)

```bash
# Navigate to your project directory (if needed)
cd path/to/YouTubeAutoBackupTool

# Initialize git repository
git init
```

## Step 2: Create .gitignore file (already done)

Your .gitignore file already contains appropriate entries for Python projects.

## Step 3: Stage Your Files

```bash
# Add all files except those specified in .gitignore
git add .
```

## Step 4: Create Initial Commit

```bash
# Create your first commit with a descriptive message
git commit -m "Initial commit: YouTubeAutoBackupTool project structure"
```

## Step 5: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com/)
2. Log in to your account
3. Click the "+" icon in the upper right corner and select "New repository"
4. Enter "YouTubeAutoBackupTool" as the Repository name
5. Add a description: "A professional PySide6-based Python application that automatically downloads and backs up YouTube videos and channels."
6. Choose "Public" (or "Private" if you prefer)
7. **DO NOT** initialize the repository with a README, .gitignore, or license (since you already have these files)
8. Click "Create repository"

## Step 6: Link Your Local Repository to GitHub

GitHub will show instructions after creating the repository. Follow these commands:

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/YouTubeAutoBackupTool.git

# Rename your default branch to main (industry standard practice)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

## Step 7: Add Topics to Your Repository (on GitHub)

After pushing your code, add relevant topics to your repository:
1. Go to your repository on GitHub
2. Click the gear icon next to "About" on the right sidebar
3. Add topics like: `youtube`, `backup`, `download`, `pyside6`, `python`, `youtube-api`

## Step 8: Set Up GitHub Actions (Optional)

To set up basic CI/CD with GitHub Actions:

1. Create a `.github/workflows` directory:
```bash
mkdir -p .github/workflows
```

2. Create a basic workflow file for testing:
```bash
# Create the workflow file
touch .github/workflows/python-tests.yml
```

3. Add the following content to the workflow file:
```yaml
name: Python Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
        pip install -r requirements.txt
    - name: Test with pytest
      run: |
        pytest
```

4. Commit and push this workflow file:
```bash
git add .github/workflows/python-tests.yml
git commit -m "Add GitHub Actions workflow for testing"
git push
```

## Step 9: Create a Release (Optional but Recommended)

Once your code is stable:

1. Go to your repository on GitHub
2. Click on "Releases" on the right sidebar
3. Click "Create a new release"
4. Tag version: v1.0.0
5. Release title: "Initial Release"
6. Description: Add key features and any setup instructions
7. Click "Publish release"

This will create a tagged release that users can download directly.

## Best Practices Checklist

- [x] Clear, descriptive README
- [x] Proper licensing (MIT)
- [x] Comprehensive .gitignore
- [x] Well-structured project layout
- [x] Documentation
- [x] Requirements file
- [ ] GitHub Actions for CI/CD (optional)
- [ ] Regular releases (optional)
- [ ] Issue templates (optional)
- [ ] Pull request templates (optional)

Following these steps will ensure your repository follows industry standards and best practices! 