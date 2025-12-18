# StudyAI - Interactive Economics Study Tool

An interactive study tool inspired by NotebookLM, featuring AI-powered teacher-student dialogue mode and video summaries for learning Introductory Microeconomics.

## 🎯 Features

### 1. 🎙️ Audio Two-Person Dialogue Mode
- **Interactive Q&A**: Ask questions and get detailed explanations from an AI teacher
- **Text-to-Speech**: Listen to responses with natural voice synthesis
- **Voice Input**: Use your microphone to ask questions (speech-to-text)
- **Contextual Responses**: AI provides topic-specific explanations with follow-up questions
- **Conversation History**: Track your learning progress

### 2. 📺 Video Summaries
- **Embedded YouTube Videos**: Watch curated educational videos directly in the app
- **Video Notes**: Key takeaways highlighted for quick revision
- **Visual Learning**: Understand complex concepts through visual explanations

### 3. 📚 Study Content
- **Chapter Topics**: Complete coverage of Introductory Microeconomics Chapter 1
- **Key Terms**: Important definitions and concepts
- **Exam Tips**: Strategic advice for exams

### 4. 📝 Self-Assessment
- **Interactive Quiz**: 8 multiple-choice questions with instant feedback
- **Explanations**: Learn from your mistakes with detailed explanations
- **Score Tracking**: Monitor your progress

### 5. 🃏 Flashcards
- **Flip Cards**: Interactive flashcards for revision
- **Shuffle Mode**: Randomize cards for better retention
- **All Terms View**: Quick access to all key terms

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Navigate to the project folder**:
   ```bash
   cd study_tool
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## 📖 How to Use

### Home Page
- View all chapter topics at a glance
- Click on any topic card to read detailed content
- Check exam tips for test preparation

### AI Dialogue Mode
1. Navigate to "AI Dialogue" section
2. Type your question or click suggested questions
3. Use the microphone button for voice input
4. Enable/disable voice responses with the toggle
5. Click the speaker icon on any response to hear it again

### Video Summaries
1. Go to "Video Summaries" section
2. Watch embedded YouTube videos
3. Read key takeaways below each video

### Quiz
1. Navigate to "Quiz" section
2. Answer questions by clicking options
3. See immediate feedback and explanations
4. Track your score
5. Retake quiz to improve

### Flashcards
1. Go to "Flashcards" section
2. Click cards to flip and see definitions
3. Use arrows to navigate between cards
4. Shuffle for random order
5. Click mini-cards below to jump to specific terms

## 🎨 Features

- **Dark/Light Theme**: Toggle between themes for comfortable reading
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Keyboard Shortcuts**: Press Enter to send messages
- **Smooth Animations**: Pleasant user experience

## 📂 Project Structure

```
study_tool/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Stylesheet
    └── js/
        └── main.js       # JavaScript functionality
```

## 🔧 Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **APIs**: Web Speech API (text-to-speech, speech-to-text)
- **Videos**: YouTube Embed

## 📚 Content Coverage

Based on **Introductory Microeconomics - Chapter 1**:
1. What is Economics?
2. Central Problems of an Economy
3. Economic Systems (Capitalist, Socialist, Mixed)
4. Production Possibility Curve (PPC)
5. Positive vs Normative Economics

## 💡 Tips for Best Experience

1. Use Chrome or Edge for best voice feature support
2. Allow microphone access for voice input
3. Use headphones for better audio experience
4. Complete the quiz after watching videos
5. Use flashcards daily for retention

## 🐛 Troubleshooting

**Voice not working?**
- Ensure your browser supports Web Speech API
- Check if voice is enabled (toggle button)
- Try refreshing the page

**Videos not loading?**
- Check your internet connection
- Try refreshing the page
- Ensure YouTube is not blocked

**App not starting?**
- Verify Python is installed
- Check if Flask is installed correctly
- Ensure port 5000 is not in use

## 📄 License

This project is created for educational purposes as part of an internship assignment.

---

**Happy Learning! 📚✨**
