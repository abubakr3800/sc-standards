"""
Chat API for Lighting Standards
Provides conversational interface to query lighting standards
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
from pathlib import Path
import re

app = FastAPI(title="Lighting Standards Chat API", version="1.0.0")

class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]
    recommendations: List[str]

class StandardsChatBot:
    """Chat bot for lighting standards queries"""
    
    def __init__(self):
        self.standards_data = self._load_standards()
        self.qa_pairs = self._create_qa_pairs()
    
    def _load_standards(self):
        """Load standards data from processed documents"""
        standards = {}
        try:
            uploads_dir = Path("uploads")
            if uploads_dir.exists():
                processed_files = list(uploads_dir.glob("*_processed.json"))
                for file_path in processed_files:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        standards[data['file_name']] = data
        except Exception as e:
            print(f"Warning: Could not load standards data: {e}")
        return standards
    
    def _create_qa_pairs(self):
        """Create question-answer pairs for common queries"""
        return {
            # Illuminance questions
            "illuminance office": {
                "answer": "For office work, the recommended illuminance is 500 lux (minimum 300 lux, maximum 1000 lux) according to EN 12464-1:2021.",
                "confidence": 0.95,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use LED luminaires with good uniformity", "Consider task lighting for detailed work"]
            },
            "illuminance conference": {
                "answer": "For conference rooms, the recommended illuminance is 300 lux (minimum 200 lux, maximum 500 lux) according to EN 12464-1:2021.",
                "confidence": 0.95,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Add dimming controls for presentations", "Consider accent lighting for visual interest"]
            },
            "illuminance corridor": {
                "answer": "For corridors, the recommended illuminance is 100 lux (minimum 50 lux, maximum 200 lux) according to EN 12464-1:2021.",
                "confidence": 0.95,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use energy-efficient LED lighting", "Ensure good uniformity for safety"]
            },
            
            # UGR questions
            "ugr office": {
                "answer": "For office work, the UGR (Unified Glare Rating) should be ≤19, with ≤16 recommended for computer work according to EN 12464-1:2021.",
                "confidence": 0.95,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use luminaires with good glare control", "Consider indirect lighting for computer areas"]
            },
            "ugr conference": {
                "answer": "For conference rooms, the UGR should be ≤22, with ≤19 recommended according to EN 12464-1:2021.",
                "confidence": 0.95,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use recessed or surface-mounted luminaires", "Avoid direct glare on presentation screens"]
            },
            
            # CRI questions
            "cri office": {
                "answer": "For office work, the CRI (Color Rendering Index) should be ≥80, with ≥90 recommended for color-critical tasks according to EN 12464-1:2021.",
                "confidence": 0.95,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use LED luminaires with high CRI", "Consider CRI ≥90 for design and graphics work"]
            },
            
            # Power density questions
            "power density office": {
                "answer": "For office lighting, the power density should be ≤3.5 W/m², with ≤2.5 W/m² recommended for energy efficiency according to EN 12464-1:2021.",
                "confidence": 0.95,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use energy-efficient LED luminaires", "Implement lighting controls for energy savings"]
            },
            
            # Uniformity questions
            "uniformity office": {
                "answer": "For office work, the uniformity should be ≥0.6, with ≥0.8 recommended for good lighting distribution according to EN 12464-1:2021.",
                "confidence": 0.95,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use appropriate spacing between luminaires", "Consider indirect lighting for better uniformity"]
            },
            
            # General questions
            "what is illuminance": {
                "answer": "Illuminance is the amount of light falling on a surface, measured in lux (lx). It indicates how bright a surface appears to the human eye.",
                "confidence": 0.90,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use appropriate illuminance levels for the task", "Consider daylight integration"]
            },
            "what is ugr": {
                "answer": "UGR (Unified Glare Rating) is a measure of glare from luminaires, with lower values indicating less glare. Values range from 10 (no glare) to 30 (unacceptable glare).",
                "confidence": 0.90,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Choose luminaires with low UGR values", "Consider indirect lighting for glare control"]
            },
            "what is cri": {
                "answer": "CRI (Color Rendering Index) measures how accurately a light source renders colors compared to natural light. Values range from 0 to 100, with 100 being perfect color rendering.",
                "confidence": 0.90,
                "sources": ["EN 12464-1:2021"],
                "recommendations": ["Use high CRI lighting for color-critical tasks", "Consider CRI ≥90 for design work"]
            }
        }
    
    def find_best_match(self, question: str) -> Optional[Dict]:
        """Find the best matching Q&A pair"""
        question_lower = question.lower()
        
        # Direct matches
        for key, value in self.qa_pairs.items():
            if key in question_lower:
                return value
        
        # Partial matches
        best_match = None
        best_score = 0
        
        for key, value in self.qa_pairs.items():
            score = self._calculate_similarity(question_lower, key)
            if score > best_score and score > 0.3:
                best_score = score
                best_match = value
        
        return best_match
    
    def _calculate_similarity(self, question: str, key: str) -> float:
        """Calculate similarity between question and key"""
        question_words = set(question.split())
        key_words = set(key.split())
        
        if not question_words or not key_words:
            return 0
        
        intersection = question_words.intersection(key_words)
        union = question_words.union(key_words)
        
        return len(intersection) / len(union)
    
    def generate_response(self, question: str) -> ChatResponse:
        """Generate response to a question"""
        # Find best match
        match = self.find_best_match(question)
        
        if match:
            return ChatResponse(
                answer=match["answer"],
                confidence=match["confidence"],
                sources=match["sources"],
                recommendations=match["recommendations"]
            )
        
        # If no match found, provide general guidance
        return ChatResponse(
            answer="I can help you with lighting standards questions. Try asking about illuminance, UGR, CRI, power density, or uniformity for specific applications like office, conference, or corridor lighting.",
            confidence=0.5,
            sources=["EN 12464-1:2021"],
            recommendations=["Be more specific about the application or parameter you're asking about"]
        )

# Initialize the chat bot
chat_bot = StandardsChatBot()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Lighting Standards Chat API",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Send a message to the chat bot",
            "/standards": "GET - List available standards",
            "/help": "GET - Get help on how to use the API"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat endpoint for asking questions about lighting standards"""
    try:
        response = chat_bot.generate_response(message.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/standards")
async def get_standards():
    """Get list of available standards"""
    return {
        "standards": list(chat_bot.standards_data.keys()),
        "total_standards": len(chat_bot.standards_data)
    }

@app.get("/help")
async def get_help():
    """Get help on how to use the API"""
    return {
        "usage": "Send a POST request to /chat with a JSON body containing 'message' field",
        "example_questions": [
            "What is the illuminance requirement for office work?",
            "What is the UGR limit for conference rooms?",
            "What is the recommended CRI for office lighting?",
            "What is the power density limit for office lighting?",
            "What is illuminance?",
            "What is UGR?",
            "What is CRI?"
        ],
        "supported_applications": [
            "office", "conference", "corridor", "reception", "staircase", "detailed work"
        ],
        "supported_parameters": [
            "illuminance", "UGR", "CRI", "power density", "uniformity"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
