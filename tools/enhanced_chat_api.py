"""
Enhanced Chat API for Lighting Standards
Uses actual standards data and AI for higher accuracy
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Tuple
import json
import re
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Enhanced Lighting Standards Chat API", version="2.0.0")

class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]
    recommendations: List[str]
    extracted_data: Optional[Dict] = None

class EnhancedStandardsChatBot:
    """Enhanced chat bot that uses actual standards data and AI"""
    
    def __init__(self):
        self.standards_data = self._load_standards()
        self.embedding_model = self._load_embedding_model()
        self.qa_embeddings = self._create_qa_embeddings()
        self.extracted_parameters = self._extract_parameters_from_standards()
        logger.info(f"Loaded {len(self.standards_data)} standards documents")
        logger.info(f"Extracted {len(self.extracted_parameters)} parameters")
    
    def _load_embedding_model(self):
        """Load sentence transformer model"""
        try:
            model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded embedding model successfully")
            return model
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            return None
    
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
                        logger.info(f"Loaded standard: {data['file_name']}")
        except Exception as e:
            logger.error(f"Could not load standards data: {e}")
        return standards
    
    def _extract_parameters_from_standards(self):
        """Extract lighting parameters from standards data"""
        parameters = {}
        
        for doc_name, doc_data in self.standards_data.items():
            text_content = doc_data.get('text_content', '')
            
            # Extract illuminance values
            illuminance_patterns = [
                r'(\d+)\s*lux\s*(?:minimum|min|≥|>=)',
                r'(?:minimum|min|≥|>=)\s*(\d+)\s*lux',
                r'illuminance[:\s]*(\d+)\s*lux',
                r'(\d+)\s*lx\s*(?:minimum|min|≥|>=)',
                r'(?:minimum|min|≥|>=)\s*(\d+)\s*lx'
            ]
            
            for pattern in illuminance_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    value = int(match)
                    if 'illuminance' not in parameters:
                        parameters['illuminance'] = []
                    parameters['illuminance'].append({
                        'value': value,
                        'source': doc_name,
                        'context': self._extract_context(text_content, match)
                    })
            
            # Extract UGR values
            ugr_patterns = [
                r'UGR[:\s]*(?:≤|<=|maximum|max)\s*(\d+)',
                r'(?:≤|<=|maximum|max)\s*(\d+)\s*UGR',
                r'glare[:\s]*(?:≤|<=|maximum|max)\s*(\d+)'
            ]
            
            for pattern in ugr_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    value = int(match)
                    if 'ugr' not in parameters:
                        parameters['ugr'] = []
                    parameters['ugr'].append({
                        'value': value,
                        'source': doc_name,
                        'context': self._extract_context(text_content, match)
                    })
            
            # Extract CRI values
            cri_patterns = [
                r'CRI[:\s]*(?:≥|>=|minimum|min)\s*(\d+)',
                r'(?:≥|>=|minimum|min)\s*(\d+)\s*CRI',
                r'color rendering[:\s]*(?:≥|>=|minimum|min)\s*(\d+)'
            ]
            
            for pattern in cri_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    value = int(match)
                    if 'cri' not in parameters:
                        parameters['cri'] = []
                    parameters['cri'].append({
                        'value': value,
                        'source': doc_name,
                        'context': self._extract_context(text_content, match)
                    })
        
        return parameters
    
    def _extract_context(self, text: str, match: str, context_length: int = 100):
        """Extract context around a match"""
        try:
            index = text.lower().find(match.lower())
            if index != -1:
                start = max(0, index - context_length)
                end = min(len(text), index + len(match) + context_length)
                return text[start:end].strip()
        except:
            pass
        return ""
    
    def _create_qa_embeddings(self):
        """Create embeddings for Q&A pairs"""
        qa_pairs = {
            "illuminance office": "What is the illuminance requirement for office work?",
            "illuminance conference": "What is the illuminance requirement for conference rooms?",
            "illuminance corridor": "What is the illuminance requirement for corridors?",
            "ugr office": "What is the UGR limit for office work?",
            "ugr conference": "What is the UGR limit for conference rooms?",
            "cri office": "What is the CRI requirement for office lighting?",
            "power density office": "What is the power density limit for office lighting?",
            "uniformity office": "What is the uniformity requirement for office lighting?",
            "what is illuminance": "What is illuminance?",
            "what is ugr": "What is UGR?",
            "what is cri": "What is CRI?",
            "what is uniformity": "What is uniformity?"
        }
        
        if self.embedding_model:
            questions = list(qa_pairs.values())
            embeddings = self.embedding_model.encode(questions)
            return {
                'questions': questions,
                'embeddings': embeddings,
                'qa_pairs': qa_pairs
            }
        return None
    
    def _find_best_match_ai(self, question: str) -> Tuple[Optional[str], float]:
        """Find best match using AI embeddings"""
        if not self.embedding_model or not self.qa_embeddings:
            return None, 0.0
        
        try:
            question_embedding = self.embedding_model.encode([question])
            similarities = cosine_similarity(question_embedding, self.qa_embeddings['embeddings'])[0]
            
            best_index = np.argmax(similarities)
            best_similarity = similarities[best_index]
            
            if best_similarity > 0.3:  # Threshold for matching
                best_question = self.qa_embeddings['questions'][best_index]
                return best_question, float(best_similarity)
        except Exception as e:
            logger.error(f"Error in AI matching: {e}")
        
        return None, 0.0
    
    def _get_parameter_from_standards(self, parameter_type: str, application: str = None) -> Dict:
        """Get parameter values from actual standards data"""
        if parameter_type not in self.extracted_parameters:
            return {}
        
        values = self.extracted_parameters[parameter_type]
        
        # Filter by application if specified
        if application:
            filtered_values = []
            for value in values:
                context_lower = value['context'].lower()
                if application.lower() in context_lower:
                    filtered_values.append(value)
            values = filtered_values if filtered_values else values
        
        if not values:
            return {}
        
        # Calculate statistics
        numeric_values = [v['value'] for v in values if isinstance(v['value'], (int, float))]
        
        if not numeric_values:
            return {}
        
        result = {
            'values': values,
            'min': min(numeric_values),
            'max': max(numeric_values),
            'avg': sum(numeric_values) / len(numeric_values),
            'sources': list(set(v['source'] for v in values))
        }
        
        return result
    
    def _generate_enhanced_answer(self, question: str, parameter_type: str, application: str = None) -> Dict:
        """Generate answer using actual standards data"""
        param_data = self._get_parameter_from_standards(parameter_type, application)
        
        if not param_data:
            return {
                "answer": f"I couldn't find specific {parameter_type} requirements in the standards. Please check the standards documents.",
                "confidence": 0.3,
                "sources": [],
                "recommendations": ["Check the standards documents for specific requirements"],
                "extracted_data": None
            }
        
        # Generate answer based on actual data
        if parameter_type == 'illuminance':
            answer = f"Based on the standards data, {parameter_type} requirements are: "
            if application:
                answer += f"For {application}, "
            answer += f"minimum {param_data['min']} lux, maximum {param_data['max']} lux, average {param_data['avg']:.0f} lux."
        elif parameter_type == 'ugr':
            answer = f"Based on the standards data, UGR (Unified Glare Rating) should be ≤{param_data['max']}, with typical values around {param_data['avg']:.0f}."
        elif parameter_type == 'cri':
            answer = f"Based on the standards data, CRI (Color Rendering Index) should be ≥{param_data['min']}, with typical values around {param_data['avg']:.0f}."
        else:
            answer = f"Based on the standards data, {parameter_type} requirements are: minimum {param_data['min']}, maximum {param_data['max']}, average {param_data['avg']:.1f}."
        
        # Add context from standards
        if param_data['values']:
            context_examples = [v['context'][:100] + "..." for v in param_data['values'][:2]]
            if context_examples:
                answer += f" Context from standards: {' '.join(context_examples)}"
        
        return {
            "answer": answer,
            "confidence": 0.85,  # Higher confidence for data-driven answers
            "sources": param_data['sources'],
            "recommendations": self._generate_recommendations(parameter_type, param_data),
            "extracted_data": param_data
        }
    
    def _generate_recommendations(self, parameter_type: str, param_data: Dict) -> List[str]:
        """Generate recommendations based on actual data"""
        recommendations = []
        
        if parameter_type == 'illuminance':
            if param_data['avg'] > 500:
                recommendations.append("Consider energy-efficient LED luminaires for high illuminance requirements")
            recommendations.append("Ensure good uniformity across the space")
            recommendations.append("Consider task lighting for detailed work areas")
        elif parameter_type == 'ugr':
            if param_data['max'] <= 19:
                recommendations.append("Use luminaires with good glare control")
                recommendations.append("Consider indirect lighting for computer areas")
        elif parameter_type == 'cri':
            if param_data['min'] >= 80:
                recommendations.append("Use high-quality LED luminaires with good color rendering")
                recommendations.append("Consider CRI ≥90 for color-critical tasks")
        
        return recommendations
    
    def generate_response(self, question: str) -> ChatResponse:
        """Generate enhanced response to a question"""
        question_lower = question.lower()
        
        # Try AI-based matching first
        best_match, similarity = self._find_best_match_ai(question)
        
        if best_match and similarity > 0.3:
            # Determine parameter type and application
            parameter_type = None
            application = None
            
            if 'illuminance' in question_lower:
                parameter_type = 'illuminance'
            elif 'ugr' in question_lower:
                parameter_type = 'ugr'
            elif 'cri' in question_lower:
                parameter_type = 'cri'
            elif 'power' in question_lower and 'density' in question_lower:
                parameter_type = 'power_density'
            elif 'uniformity' in question_lower:
                parameter_type = 'uniformity'
            
            # Determine application
            if 'office' in question_lower:
                application = 'office'
            elif 'conference' in question_lower:
                application = 'conference'
            elif 'corridor' in question_lower:
                application = 'corridor'
            elif 'reception' in question_lower:
                application = 'reception'
            
            # Generate enhanced answer
            if parameter_type:
                result = self._generate_enhanced_answer(question, parameter_type, application)
                return ChatResponse(**result)
        
        # Fallback to basic response
        return ChatResponse(
            answer="I can help you with lighting standards questions. Try asking about illuminance, UGR, CRI, power density, or uniformity for specific applications like office, conference, or corridor lighting.",
            confidence=0.5,
            sources=["EN 12464-1:2021"],
            recommendations=["Be more specific about the parameter or application you're asking about"],
            extracted_data=None
        )

# Initialize the enhanced chat bot
chat_bot = EnhancedStandardsChatBot()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Enhanced Lighting Standards Chat API",
        "version": "2.0.0",
        "features": [
            "AI-powered question matching",
            "Real standards data extraction",
            "Higher accuracy responses",
            "Context-aware answers"
        ],
        "endpoints": {
            "/chat": "POST - Send a message to the chat bot",
            "/standards": "GET - List available standards",
            "/parameters": "GET - List extracted parameters",
            "/help": "GET - Get help on how to use the API"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Enhanced chat endpoint"""
    try:
        response = chat_bot.generate_response(message.message)
        return response
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/standards")
async def get_standards():
    """Get list of available standards"""
    return {
        "standards": list(chat_bot.standards_data.keys()),
        "total_standards": len(chat_bot.standards_data)
    }

@app.get("/parameters")
async def get_parameters():
    """Get extracted parameters from standards"""
    return {
        "parameters": list(chat_bot.extracted_parameters.keys()),
        "extracted_data": chat_bot.extracted_parameters
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
        ],
        "accuracy_features": [
            "AI-powered question matching",
            "Real standards data extraction",
            "Context-aware responses",
            "Higher confidence scoring"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
