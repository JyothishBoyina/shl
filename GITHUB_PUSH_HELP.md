# GitHub Push Instructions

## Issue
Git authentication popup is not appearing. This is a common issue with Git Credential Manager on Windows.

## Solution Options

### Option 1: Use GitHub Desktop (Easiest)
1. Download GitHub Desktop: https://desktop.github.com/
2. Open GitHub Desktop
3. File → Add Local Repository
4. Select: `c:\Users\conne\Downloads\SHL\shl-project`
5. Click "Publish repository"
6. Repository name: `SHL-Assessment-Recommender`
7. Uncheck "Keep this code private" (or keep checked if you want it private)
8. Click "Publish repository"

### Option 2: Use Personal Access Token
1. Go to GitHub: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "SHL Project"
4. Select scopes: `repo` (all)
5. Click "Generate token"
6. Copy the token (save it somewhere safe!)
7. Run this command (replace YOUR_TOKEN with the actual token):

```bash
git push https://YOUR_TOKEN@github.com/Abiads/SHL-Assessment-Recommender.git main
```

### Option 3: Configure Git Credential Manager
1. Open a new PowerShell window as Administrator
2. Run:
```bash
git config --global credential.helper manager-core
```
3. Then try push again:
```bash
cd c:\Users\conne\Downloads\SHL\shl-project
git push -u origin main
```

### Option 4: Use SSH (More Setup)
1. Generate SSH key:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
2. Add to GitHub: https://github.com/settings/keys
3. Change remote to SSH:
```bash
git remote set-url origin git@github.com:Abiads/SHL-Assessment-Recommender.git
git push -u origin main
```

## Recommended
**Use GitHub Desktop** - it's the easiest and most reliable method for Windows users.

## Current Status
- ✅ Code is committed locally
- ✅ Remote is configured correctly
- ⏳ Waiting to push to GitHub

Once pushed, you can proceed with deployment to Render and Streamlit Cloud.
