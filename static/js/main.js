// StudyBot AI - Main JavaScript
// Fully Functional Interactive Study Tool

// ============== GLOBAL STATE ==============
let currentSection = 'home';
let currentQuizIndex = 0;
let quizScore = 0;
let quizAnswered = false;
let quizData = [];
let currentCardIndex = 0;
let flashcards = [];
let aiStatus = 'checking';

// ============== INITIALIZATION ==============
document.addEventListener('DOMContentLoaded', () => {
    console.log('StudyBot AI Initializing...');
    initializeApp();
});

async function initializeApp() {
    try {
        await checkAIStatus();
        await loadTopics();
        await loadQuizData();
        await loadFlashcardsData();
        showSection('home');
        setupEventListeners();
        console.log('StudyBot AI Ready!');
    } catch (error) {
        console.error('Initialization error:', error);
    }
}

function setupEventListeners() {
    // Chat input Enter key
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Video input Enter keys
    document.querySelectorAll('[id^="video-input-"]').forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const videoId = input.id.replace('video-input-', '');
                askVideoQuestion(videoId);
            }
        });
    });

    // Keyboard navigation for flashcards
    document.addEventListener('keydown', (e) => {
        if (currentSection === 'flashcards') {
            if (e.key === 'ArrowLeft') prevCard();
            else if (e.key === 'ArrowRight') nextCard();
            else if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                flipCard();
            }
        }
    });

    // Modal close on outside click
    const modal = document.getElementById('topic-modal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
    }
}

// ============== NAVIGATION ==============
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show target section
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('active');
        currentSection = sectionId;
    }
    
    // Activate corresponding nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        const onclick = link.getAttribute('onclick');
        if (onclick && onclick.includes(`'${sectionId}'`)) {
            link.classList.add('active');
        }
    });

    // Reset quiz when entering quiz section
    if (sectionId === 'quiz' && quizData.length > 0) {
        renderQuestion();
    }
}

// ============== AI STATUS ==============
async function checkAIStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        
        if (statusDot && statusText) {
            if (data.gemini_enabled) {
                statusDot.classList.add('online');
                statusText.textContent = 'AI Online';
                aiStatus = 'online';
            } else {
                statusDot.classList.remove('online');
                statusText.textContent = 'Demo Mode';
                aiStatus = 'demo';
            }
        }
    } catch (error) {
        console.error('Status check failed:', error);
    }
}

// ============== THEME ==============
function toggleTheme() {
    document.body.classList.toggle('dark');
    const icon = document.querySelector('.theme-btn i');
    if (icon) {
        if (document.body.classList.contains('dark')) {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
}

// ============== TOPICS ==============
async function loadTopics() {
    try {
        const response = await fetch('/api/topics');
        const data = await response.json();
        const topicsGrid = document.getElementById('topics-grid');
        
        if (topicsGrid && data.topics) {
            topicsGrid.innerHTML = data.topics.map(topic => `
                <div class="topic-card" onclick="askAboutTopic('${escapeHtml(topic.title)}')">
                    <h4>${escapeHtml(topic.title)}</h4>
                    <p>${escapeHtml(topic.description || 'Click to learn more')}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to load topics:', error);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function askAboutTopic(topic) {
    showSection('dialogue');
    setTimeout(() => {
        const input = document.getElementById('chat-input');
        if (input) {
            input.value = `Tell me about ${topic}`;
            sendMessage();
        }
    }, 300);
}

// ============== CHAT FUNCTIONS ==============
async function sendMessage() {
    const input = document.getElementById('chat-input');
    if (!input) return;
    
    const message = input.value.trim();
    if (!message) return;
    
    input.value = '';
    input.disabled = true;
    
    // Add user message
    addChatMessage(message, 'user');
    
    // Show loading
    const loadingId = 'loading-' + Date.now();
    addChatMessage('<i class="fas fa-spinner fa-spin"></i> Thinking...', 'bot', loadingId);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        removeChatMessage(loadingId);
        
        if (data.response) {
            addChatMessage(data.response, 'bot');
        } else if (data.error) {
            addChatMessage('Sorry, there was an error: ' + data.error, 'bot');
        }
    } catch (error) {
        console.error('Chat error:', error);
        removeChatMessage(loadingId);
        addChatMessage('Sorry, there was a network error. Please try again.', 'bot');
    } finally {
        input.disabled = false;
        input.focus();
    }
}

function addChatMessage(text, sender, id = null) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    if (id) messageDiv.id = id;
    
    const icon = sender === 'bot' ? 'fa-robot' : 'fa-user';
    const formattedText = formatMessage(text);
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${icon}"></i>
        </div>
        <div class="message-content">${formattedText}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

function removeChatMessage(id) {
    const message = document.getElementById(id);
    if (message) message.remove();
}

function formatMessage(text) {
    if (!text) return '';
    
    // Convert bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    // Convert bullet points
    const lines = text.split('<br>');
    let result = [];
    let inList = false;
    
    for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('• ') || trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
            if (!inList) {
                result.push('<ul>');
                inList = true;
            }
            result.push(`<li>${trimmed.substring(2)}</li>`);
        } else {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            result.push(line);
        }
    }
    
    if (inList) result.push('</ul>');
    
    return result.join('');
}

function askQuestion(question) {
    const input = document.getElementById('chat-input');
    if (input) {
        input.value = question;
        sendMessage();
    }
}

// ============== VIDEO Q&A ==============
async function askVideoQuestion(videoId) {
    const input = document.getElementById(`video-input-${videoId}`);
    const answerDiv = document.getElementById(`video-answer-${videoId}`);
    
    if (!input || !answerDiv) {
        console.error('Video elements not found for:', videoId);
        return;
    }
    
    const question = input.value.trim();
    if (!question) {
        answerDiv.innerHTML = '<div class="response" style="color: var(--warning);">Please enter a question first.</div>';
        return;
    }
    
    input.disabled = true;
    answerDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Analyzing video transcript...</div>';
    
    try {
        const response = await fetch(`/api/video/${videoId}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        if (data.response) {
            answerDiv.innerHTML = `<div class="response">${formatMessage(data.response)}</div>`;
        } else if (data.answer) {
            answerDiv.innerHTML = `<div class="response">${formatMessage(data.answer)}</div>`;
        } else if (data.error) {
            answerDiv.innerHTML = `<div class="response" style="border-left-color: var(--error);">Error: ${data.error}</div>`;
        } else {
            answerDiv.innerHTML = `<div class="response">Sorry, I couldn't find relevant information in the video.</div>`;
        }
    } catch (error) {
        console.error('Video Q&A error:', error);
        answerDiv.innerHTML = '<div class="response" style="border-left-color: var(--error);">Network error. Please try again.</div>';
    } finally {
        input.disabled = false;
        input.value = '';
    }
}

// ============== QUIZ FUNCTIONS ==============
async function loadQuizData() {
    try {
        const response = await fetch('/api/quiz');
        const data = await response.json();
        
        if (data.questions && Array.isArray(data.questions)) {
            quizData = data.questions;
            currentQuizIndex = 0;
            quizScore = 0;
            quizAnswered = false;
            console.log(`Loaded ${quizData.length} quiz questions`);
        }
    } catch (error) {
        console.error('Failed to load quiz:', error);
    }
}

function renderQuestion() {
    const quizContent = document.getElementById('quiz-content');
    const quizResults = document.getElementById('quiz-results');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (!quizContent || !quizData.length) {
        if (quizContent) {
            quizContent.innerHTML = '<p>Loading quiz questions...</p>';
        }
        return;
    }
    
    // Hide results, show content
    if (quizResults) quizResults.classList.remove('show');
    quizContent.style.display = 'block';
    
    // Check if quiz complete
    if (currentQuizIndex >= quizData.length) {
        showQuizResults();
        return;
    }
    
    const question = quizData[currentQuizIndex];
    const letters = ['A', 'B', 'C', 'D'];
    
    quizContent.innerHTML = `
        <div class="quiz-question">
            <h3>Question ${currentQuizIndex + 1}: ${escapeHtml(question.question)}</h3>
            <div class="quiz-options" id="quiz-options">
                ${question.options.map((opt, i) => `
                    <div class="quiz-option" onclick="selectQuizOption(${i})" data-index="${i}">
                        <span class="option-letter">${letters[i]}</span>
                        <span>${escapeHtml(opt)}</span>
                    </div>
                `).join('')}
            </div>
            <div id="quiz-explanation" class="quiz-explanation" style="display: none;"></div>
        </div>
    `;
    
    // Update progress bar
    updateQuizProgress();
    
    // Update navigation buttons
    if (prevBtn) {
        prevBtn.disabled = currentQuizIndex === 0;
        prevBtn.style.background = currentQuizIndex === 0 ? 'var(--bg)' : '';
    }
    if (nextBtn) {
        nextBtn.innerHTML = currentQuizIndex >= quizData.length - 1 
            ? 'Finish <i class="fas fa-check"></i>' 
            : 'Next <i class="fas fa-arrow-right"></i>';
    }
    
    quizAnswered = false;
}

function selectQuizOption(index) {
    if (quizAnswered) return;
    quizAnswered = true;
    
    const question = quizData[currentQuizIndex];
    const options = document.querySelectorAll('.quiz-option');
    const explanation = document.getElementById('quiz-explanation');
    
    // Find correct answer index (answer can be text or index)
    let correctIndex = question.answer;
    if (typeof question.answer === 'string') {
        correctIndex = question.options.findIndex(opt => opt === question.answer);
    }
    
    // Check if correct
    const isCorrect = index === correctIndex;
    if (isCorrect) quizScore++;
    
    // Style all options
    options.forEach((opt, i) => {
        opt.style.pointerEvents = 'none';
        opt.classList.remove('selected');
        
        if (i === correctIndex) {
            opt.classList.add('correct');
        } else if (i === index && !isCorrect) {
            opt.classList.add('incorrect');
        }
    });
    
    // Show explanation
    if (explanation) {
        const icon = isCorrect ? '✓' : '✗';
        const status = isCorrect ? 'Correct!' : 'Incorrect';
        explanation.innerHTML = `
            <strong style="color: ${isCorrect ? 'var(--success)' : 'var(--error)'}">
                ${icon} ${status}
            </strong><br>
            ${question.explanation || 'The correct answer is option ' + ['A', 'B', 'C', 'D'][correctIndex] + '.'}
        `;
        explanation.style.display = 'block';
    }
}

function updateQuizProgress() {
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.getElementById('progress-text');
    
    if (progressFill) {
        const progress = ((currentQuizIndex + 1) / quizData.length) * 100;
        progressFill.style.width = `${progress}%`;
    }
    
    if (progressText) {
        progressText.textContent = `Question ${currentQuizIndex + 1} of ${quizData.length}`;
    }
}

function nextQuestion() {
    if (!quizAnswered && currentQuizIndex < quizData.length) {
        // Force user to answer first
        alert('Please select an answer before continuing.');
        return;
    }
    
    if (currentQuizIndex < quizData.length - 1) {
        currentQuizIndex++;
        renderQuestion();
    } else {
        showQuizResults();
    }
}

function prevQuestion() {
    if (currentQuizIndex > 0) {
        currentQuizIndex--;
        quizAnswered = true; // Allow viewing previous without re-answering
        renderQuestion();
    }
}

function showQuizResults() {
    const quizContent = document.getElementById('quiz-content');
    const quizResults = document.getElementById('quiz-results');
    
    if (quizContent) quizContent.style.display = 'none';
    if (!quizResults) return;
    
    quizResults.classList.add('show');
    
    const percentage = Math.round((quizScore / quizData.length) * 100);
    let icon, message, color;
    
    if (percentage >= 80) {
        icon = '🏆';
        message = 'Excellent work! You really know your stuff!';
        color = 'var(--success)';
    } else if (percentage >= 60) {
        icon = '👍';
        message = 'Good job! Keep studying to improve!';
        color = 'var(--primary)';
    } else if (percentage >= 40) {
        icon = '📖';
        message = 'Not bad! Review the material and try again.';
        color = 'var(--warning)';
    } else {
        icon = '📚';
        message = 'Keep learning! Review the chapter and videos.';
        color = 'var(--error)';
    }
    
    quizResults.innerHTML = `
        <div class="results-card">
            <div class="results-icon">${icon}</div>
            <h2>Quiz Complete!</h2>
            <div class="score-display">
                <span class="score-num" style="color: ${color}">${quizScore}</span>
                <span class="score-total">/ ${quizData.length}</span>
            </div>
            <p style="color: var(--text-light); margin-bottom: 0.5rem;">${percentage}%</p>
            <p style="color: var(--text-light); margin-bottom: 1.5rem;">${message}</p>
            <button class="btn" onclick="restartQuiz()" style="background: var(--primary); color: white;">
                <i class="fas fa-redo"></i> Try Again
            </button>
        </div>
    `;
}

function restartQuiz() {
    currentQuizIndex = 0;
    quizScore = 0;
    quizAnswered = false;
    renderQuestion();
}

// ============== FLASHCARD FUNCTIONS ==============
async function loadFlashcardsData() {
    try {
        const response = await fetch('/api/flashcards');
        const data = await response.json();
        
        if (data.flashcards && Array.isArray(data.flashcards)) {
            flashcards = data.flashcards;
            currentCardIndex = 0;
            console.log(`Loaded ${flashcards.length} flashcards`);
            renderFlashcard();
            renderFlashcardGrid();
        }
    } catch (error) {
        console.error('Failed to load flashcards:', error);
    }
}

function renderFlashcard() {
    if (!flashcards.length) return;
    
    const card = flashcards[currentCardIndex];
    const flashcard = document.getElementById('flashcard');
    const termEl = document.getElementById('card-term');
    const defEl = document.getElementById('card-definition');
    const counter = document.getElementById('card-counter');
    
    // Reset flip state
    if (flashcard) {
        flashcard.classList.remove('flipped');
    }
    
    // Update content after a brief delay for animation
    setTimeout(() => {
        if (termEl) termEl.textContent = card.term;
        if (defEl) defEl.textContent = card.definition;
    }, 150);
    
    if (counter) {
        counter.textContent = `${currentCardIndex + 1} / ${flashcards.length}`;
    }
}

function flipCard() {
    const flashcard = document.getElementById('flashcard');
    if (flashcard) {
        flashcard.classList.toggle('flipped');
    }
}

function nextCard() {
    if (flashcards.length === 0) return;
    
    currentCardIndex = (currentCardIndex + 1) % flashcards.length;
    renderFlashcard();
}

function prevCard() {
    if (flashcards.length === 0) return;
    
    currentCardIndex = (currentCardIndex - 1 + flashcards.length) % flashcards.length;
    renderFlashcard();
}

function shuffleCards() {
    if (flashcards.length === 0) return;
    
    // Fisher-Yates shuffle
    for (let i = flashcards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [flashcards[i], flashcards[j]] = [flashcards[j], flashcards[i]];
    }
    
    currentCardIndex = 0;
    renderFlashcard();
    renderFlashcardGrid();
}

function renderFlashcardGrid() {
    const grid = document.getElementById('flashcard-grid');
    if (!grid || !flashcards.length) return;
    
    grid.innerHTML = flashcards.map((card, index) => `
        <div class="fc-mini" onclick="goToCard(${index})">
            <h5>${escapeHtml(card.term)}</h5>
            <p>${escapeHtml(card.definition.substring(0, 80))}${card.definition.length > 80 ? '...' : ''}</p>
        </div>
    `).join('');
}

function goToCard(index) {
    if (index >= 0 && index < flashcards.length) {
        currentCardIndex = index;
        renderFlashcard();
        
        // Scroll to flashcard viewer
        const viewer = document.querySelector('.flashcard-viewer');
        if (viewer) {
            viewer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

// ============== MODAL FUNCTIONS ==============
function showTopicModal(title, content) {
    const modal = document.getElementById('topic-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    
    if (modal && modalTitle && modalBody) {
        modalTitle.textContent = title;
        modalBody.textContent = content;
        modal.classList.add('show');
    }
}

function closeModal() {
    const modal = document.getElementById('topic-modal');
    if (modal) {
        modal.classList.remove('show');
    }
}

// ============== UTILITY FUNCTIONS ==============
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Console log for debugging
console.log('StudyBot AI JavaScript loaded successfully');
