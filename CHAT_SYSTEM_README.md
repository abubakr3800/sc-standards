# 💡 Lighting Standards Chat System

A conversational AI system that answers questions about lighting standards using EN 12464-1:2021 and other lighting standards.

## 🚀 Quick Start

### 1. Start the Chat System
```bash
python start_chat_system.py
```

This will:
- Start the API server on port 8000
- Start the web interface on port 8501
- Open your browser automatically

### 2. Alternative: Start Components Separately

#### Start API Server Only:
```bash
python chat_api.py
```

#### Start Web Interface Only:
```bash
streamlit run chat_web_interface.py
```

#### Open HTML Interface:
Open `chat_web.html` in your browser

## 🌐 Access Points

- **Web Interface**: http://localhost:8501
- **API Endpoint**: http://localhost:8000
- **HTML Interface**: Open `chat_web.html` in browser

## 💬 How to Use

### Web Interface (Streamlit)
1. Go to http://localhost:8501
2. Type your question in the chat input
3. Get instant answers with confidence scores
4. View sources and recommendations
5. Use quick question buttons

### HTML Interface
1. Open `chat_web.html` in your browser
2. Type questions in the input field
3. Click "Send" or press Enter
4. View responses with sources and recommendations

### API Usage
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What is the illuminance requirement for office work?"}
)

data = response.json()
print(data["answer"])
print(f"Confidence: {data['confidence']:.1%}")
```

## 📚 Supported Questions

### Illuminance Questions
- "What is the illuminance requirement for office work?"
- "What is the illuminance for conference rooms?"
- "What is the illuminance for corridors?"

### UGR Questions
- "What is the UGR limit for office work?"
- "What is the UGR for conference rooms?"

### CRI Questions
- "What is the recommended CRI for office lighting?"
- "What is CRI?"

### Power Density Questions
- "What is the power density limit for office lighting?"

### General Questions
- "What is illuminance?"
- "What is UGR?"
- "What is CRI?"
- "What is uniformity?"

## 🏢 Supported Applications

- **Office**: General office work
- **Conference**: Meeting rooms
- **Corridor**: Hallways and passages
- **Reception**: Reception areas
- **Staircase**: Stairwells
- **Detailed Work**: Precision tasks

## 📊 Response Format

Each response includes:
- **Answer**: The main response to your question
- **Confidence**: How confident the system is (0-100%)
- **Sources**: Standards documents referenced
- **Recommendations**: Practical suggestions

## 🧪 Testing

Test the API:
```bash
python test_chat_api.py
```

## 🔧 API Endpoints

### POST /chat
Send a message to the chat bot
```json
{
  "message": "What is the illuminance requirement for office work?"
}
```

### GET /standards
Get list of available standards

### GET /help
Get help on how to use the API

## 📁 Files

- `chat_api.py` - FastAPI server
- `chat_web_interface.py` - Streamlit web interface
- `chat_web.html` - HTML interface
- `start_chat_system.py` - Startup script
- `test_chat_api.py` - Test script

## 🛠️ Requirements

- FastAPI
- Streamlit
- Requests
- Pydantic

Install with:
```bash
pip install fastapi uvicorn streamlit requests pydantic
```

## 🎯 Features

- **Instant Answers**: Get immediate responses to lighting standards questions
- **Confidence Scoring**: See how confident the system is in its answers
- **Source References**: Know which standards documents are referenced
- **Practical Recommendations**: Get actionable advice
- **Multiple Interfaces**: Web, HTML, and API access
- **Quick Questions**: Pre-built common questions
- **Real-time Chat**: Interactive conversation experience

## 🔍 Example Questions

1. "What is the illuminance requirement for office work?"
2. "What is the UGR limit for conference rooms?"
3. "What is the recommended CRI for office lighting?"
4. "What is the power density limit for office lighting?"
5. "What is illuminance?"
6. "What is UGR?"
7. "What is CRI?"

## 🚀 Getting Started

1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn streamlit requests pydantic
   ```

2. **Start the system**:
   ```bash
   python start_chat_system.py
   ```

3. **Ask questions**:
   - Go to http://localhost:8501
   - Type your question
   - Get instant answers!

## 🎉 Enjoy Your Lighting Standards Chat!

The system is now ready to answer all your lighting standards questions with confidence scores, sources, and practical recommendations!
