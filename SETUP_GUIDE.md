# 🎓 Interactive Study Tool - Setup Guide

## Overview
This is an AI-powered study tool inspired by NotebookLM, featuring:
- ✅ **Real AI Responses** using Google Gemini (free API)
- ✅ **YouTube Video Q&A** - Ask questions about video content
- ✅ **Two-Person Dialogue Mode** - Simulated Teacher-Student conversations
- ✅ **Quiz & Flashcards** - Test your knowledge

## Quick Start
The app is running at: http://127.0.0.1:5000

## 🔑 Enable Real AI Responses (Recommended!)

To get intelligent, context-aware answers, set up the **FREE** Google Gemini API:

### Step 1: Get Free API Key
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### Step 2: Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
cd study_tool
python app.py
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
cd study_tool
python app.py
```

### Step 3: Restart the Server
After setting the environment variable, restart the Flask server.

## Features

### 1. AI Dialogue Mode
- Ask any question about Oligopoly
- Get contextual answers from the chapter AND YouTube videos
- Two modes: Teacher-Student dialogue or direct Teacher explanation

### 2. Video Summaries with Q&A
- Watch embedded YouTube videos
- **Ask questions specifically about video content!**
- AI reads the video transcripts and answers based on them

### 3. Quiz
- 10 multiple choice questions
- Explanations for each answer
- Track your score

### 4. Flashcards
- 25 key terms and definitions
- Click to flip
- Shuffle and auto-flip features

## Content Sources
- **PDF Chapter:** AQA Economics Oligopoly content
- **YouTube Videos:**
  - https://youtu.be/Ec19ljjvlCI - Oligopoly Overview
  - https://youtu.be/Z_S0VA4jKes - Game Theory

## Technical Stack
- Backend: Flask (Python)
- AI: Google Gemini 1.5 Flash (free tier)
- Video Transcripts: youtube-transcript-api
- Frontend: HTML5, CSS3, JavaScript
- Voice: Web Speech API
