"""
Test Chat API
Simple test script to verify the chat API works
"""
import requests
import json

def test_api():
    """Test the chat API"""
    API_URL = "http://localhost:8000"
    
    print("🧪 Testing Chat API...")
    print("=" * 50)
    
    # Test questions
    test_questions = [
        "What is the illuminance requirement for office work?",
        "What is the UGR limit for conference rooms?",
        "What is the recommended CRI for office lighting?",
        "What is the power density limit for office lighting?",
        "What is illuminance?",
        "What is UGR?",
        "What is CRI?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={"message": question}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Answer: {data['answer']}")
                print(f"📊 Confidence: {data['confidence']:.1%}")
                print(f"📖 Sources: {', '.join(data['sources'])}")
                if data['recommendations']:
                    print(f"💡 Recommendations: {', '.join(data['recommendations'])}")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API. Make sure the server is running.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_api()
