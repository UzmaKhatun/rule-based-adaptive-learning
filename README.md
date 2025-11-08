# 🧮 Math Adventures - Adaptive Learning System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A rule-based adaptive math learning system that dynamically adjusts puzzle difficulty based on real-time performance analysis. Built with Python and Streamlit, featuring ML-ready architecture for future enhancement.

## 🎯 Features

- **Adaptive Learning Engine**: Automatically adjusts difficulty based on accuracy and response time
- **Three Difficulty Levels**: Easy, Medium, and Hard with appropriate problem ranges
- **Real-time Performance Tracking**: Comprehensive metrics and analytics
- **Dual Interface**: Beautiful web UI (Streamlit) 
- **Smart Recommendations**: Personalized learning insights and next steps

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/UzmaKhatun/rule-based-adaptive-learning.git

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

**Web Interface (Recommended):**
```bash
streamlit run main.py
```
Open your browser at `http://localhost:8501`

## 📁 Project Structure

```
math-adventures-adaptive-learning/
├── main.py                 # Entry point
├── ui.py                   # Streamlit web interface
├── puzzle_generator.py     # Math problem generation
├── tracker.py              # Performance tracking
├── adaptive_engine.py      # Adaptive difficulty logic
├── requirements.txt        # Python dependencies
└── README.md              # This file

```

## 🧠 How It Works

### Adaptive Algorithm

The system uses a rule-based approach with ML-inspired performance scoring:

```
Performance Score = (Accuracy × 0.7) + (Speed Score × 0.3)
```

**Adaptation Rules:**
- Performance > 0.8 → Increase difficulty
- Performance < 0.4 → Decrease difficulty
- Otherwise → Maintain current level

### Key Components

| Component | Purpose |
|-----------|---------|
| **Puzzle Generator** | Creates math problems for each difficulty level |
| **Performance Tracker** | Logs correctness, response time, and trends |
| **Adaptive Engine** | Analyzes performance and adjusts difficulty |
| **User Interface** | Displays problems and provides feedback |

## 📊 Difficulty Levels

| Level | Number Range | Operations | Target Audience |
|-------|-------------|------------|-----------------|
| Easy | 1-10 | +, - | Ages 5-7 |
| Medium | 5-20 | +, -, × | Ages 7-9 |
| Hard | 10-50 | +, -, ×, ÷ | Ages 9-10 |

## 🎮 Usage Example

1. **Start**: Enter your name and choose starting difficulty
2. **Practice**: Solve 10 adaptive math problems
3. **Feedback**: Get instant correctness indication
4. **Adapt**: System automatically adjusts difficulty
5. **Summary**: View comprehensive performance report

----

## 👨‍💻 Author

**Uzma Khatun**

### 📞 Contact

- Email : uzmakhatun0205@gmail.com
- [LinkedIn](https://www.linkedin.com/in/uzma-khatun-88b990334/)
- [GitHub](https://github.com/UzmaKhatun)
- [Portfolio](https://portfolio-uzmakhatun.netlify.app/)

---

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ for adaptive learning
