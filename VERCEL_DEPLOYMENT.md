# Vercel Deployment Guide

## 📋 Prerequisites
1. GitHub account
2. Vercel account (sign up at vercel.com with GitHub)
3. Git installed on your computer

## 🚀 Deployment Steps

### Step 1: Initialize Git Repository
Open PowerShell in the project folder and run:
```powershell
git init
git add .
git commit -m "Initial commit - Ready for Vercel deployment"
```

### Step 2: Push to GitHub
```powershell
# Create a new repository on GitHub (via browser)
# Then run these commands (replace YOUR_USERNAME and YOUR_REPO):

git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Vercel
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Vercel will auto-detect settings
5. Click "Deploy"
6. Wait 2-3 minutes for deployment

### Step 4: Access Your App
- You'll get a URL like: `https://your-app.vercel.app`
- Share this URL with anyone!

## 🔄 Auto-Deploy
Every time you push to GitHub, Vercel automatically redeploys your app.

## ⚙️ Environment Variables (if needed in future)
If you add API keys later:
1. Go to Project Settings in Vercel
2. Navigate to "Environment Variables"
3. Add your keys there

## 📝 Files Created for Vercel
- ✅ `vercel.json` - Vercel configuration
- ✅ `.gitignore` - Excludes unnecessary files
- ✅ Updated `app.py` - Production-ready

## 🆘 Troubleshooting
- **Build fails**: Check that all files are committed to Git
- **404 errors**: Ensure vercel.json routes are correct
- **Static files not loading**: Check static folder structure

## 🎯 Quick Command Reference
```powershell
# Check status
git status

# Add new changes
git add .
git commit -m "Description of changes"
git push

# View logs
vercel logs
```
