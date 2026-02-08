"""
Civic Issue Reporter & Analyzer - Backend API (GEMINI VERSION)
Uses Google AI Studio / Gemini API for multimodal analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import base64
from datetime import datetime
import os
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Initialize Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

ANALYSIS_PROMPT = """You are an AI assistant for a civic issue reporting system in Pakistan. 
Analyze the provided image and/or description of a public infrastructure problem.

Your task:
1. Classify the type of issue (Road Infrastructure, Water & Sanitation, Electrical, Waste Management, etc.)
2. Assess severity level (critical, high, medium, low)
3. Determine urgency (Emergency/Immediate/Priority/Monitor)
4. Identify safety warnings
5. Recommend specific actions for municipal authorities
6. Assign to appropriate department

Respond ONLY with a valid JSON object in this exact format:
{
  "issue_classification": {
    "type": "string - category of issue",
    "severity": "critical/high/medium/low",
    "urgency": "string - when action needed"
  },
  "ai_analysis": {
    "detected_elements": ["array of visual/textual observations"],
    "risk_level": "critical/high/medium/low",
    "estimated_impact": "string - who/what is affected"
  },
  "recommended_actions": ["array of specific action items"],
  "safety_warnings": ["array of safety concerns"],
  "priority_score": number (0-100),
  "assigned_department": "string - which government department",
  "reasoning": "brief explanation of your analysis"
}

Consider Pakistani context: common infrastructure issues, local government departments (WASA, CDA, LDA, etc.), and urgent safety concerns."""


@app.route('/api/analyze', methods=['POST'])
def analyze_issue():
    """
    Analyze a civic issue using Gemini's multimodal capabilities
    Accepts: image (base64), description (text)
    Returns: JSON analysis report
    """
    try:
        data = request.json
        description = data.get('description', '')
        image_data = data.get('image')  # base64 encoded image
        
        if not description and not image_data:
            return jsonify({'error': 'Please provide description or image'}), 400
        
        # Prepare content for Gemini
        gemini_parts = []
        
        # Add text prompt
        prompt_text = ANALYSIS_PROMPT
        if description:
            prompt_text += f"\n\nCitizen's description: {description}"
        
        gemini_parts.append(prompt_text)
        
        # Add image if provided
        if image_data:
            # Remove data:image/jpeg;base64, prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 to bytes
            image_bytes = base64.b64decode(image_data)
            
            # Create PIL Image for Gemini
            image = Image.open(io.BytesIO(image_bytes))
            
            gemini_parts.append(image)
        
        # Call Gemini API
        response = model.generate_content(
            gemini_parts,
            generation_config={
                'temperature': 0.4,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )
        
        # Parse AI response
        ai_response = response.text
        
        # Extract JSON from response (in case there's extra text)
        json_start = ai_response.find('{')
        json_end = ai_response.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            ai_response = ai_response[json_start:json_end]
        
        analysis = json.loads(ai_response)
        
        # Create complete report
        report = {
            "report_id": f"CIV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "issue_classification": analysis.get("issue_classification", {}),
            "location": {
                "description": description[:200],
                "coordinates": None  # Would be added from GPS/user input
            },
            "ai_analysis": analysis.get("ai_analysis", {}),
            "recommended_actions": analysis.get("recommended_actions", []),
            "safety_warnings": analysis.get("safety_warnings", []),
            "priority_score": analysis.get("priority_score", 50),
            "assigned_department": analysis.get("assigned_department", "Municipal Services"),
            "citizen_description": description,
            "ai_reasoning": analysis.get("reasoning", ""),
            "status": "submitted",
            "created_at": datetime.now().isoformat(),
            "ai_model": "Gemini 2.0 Flash"
        }
        
        return jsonify(report)
        
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse AI response: {str(e)}', 'raw_response': ai_response[:500]}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Civic Issue Analyzer API',
        'version': '1.0.0',
        'ai_model': 'Gemini 2.0 Flash'
    })


@app.route('/api/reports', methods=['GET'])
def get_reports():
    """
    Get all submitted reports (in production, this would query a database)
    For demo purposes, returns mock data
    """
    mock_reports = [
        {
            "report_id": "CIV-20260207120000",
            "timestamp": "2026-02-07T12:00:00",
            "issue_classification": {
                "type": "Road Infrastructure",
                "severity": "high",
                "urgency": "Immediate attention required"
            },
            "priority_score": 85,
            "status": "in_progress"
        },
        {
            "report_id": "CIV-20260207110000",
            "timestamp": "2026-02-07T11:00:00",
            "issue_classification": {
                "type": "Water & Sanitation",
                "severity": "critical",
                "urgency": "Emergency response"
            },
            "priority_score": 95,
            "status": "resolved"
        }
    ]
    return jsonify(mock_reports)


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get statistics for government dashboard
    """
    stats = {
        "total_reports": 156,
        "pending": 23,
        "in_progress": 45,
        "resolved": 88,
        "by_severity": {
            "critical": 12,
            "high": 34,
            "medium": 67,
            "low": 43
        },
        "by_category": {
            "Road Infrastructure": 56,
            "Water & Sanitation": 32,
            "Electrical": 28,
            "Waste Management": 40
        },
        "avg_response_time_hours": 18.5,
        "resolution_rate": 0.564
    }
    return jsonify(stats)


if __name__ == '__main__':
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("=" * 60)
        print("WARNING: GOOGLE_API_KEY not set!")
        print("=" * 60)
        print("Get your free API key from:")
        print("https://aistudio.google.com/apikey")
        print()
        print("Then set it with:")
        print("export GOOGLE_API_KEY='your-key-here'")
        print("=" * 60)
    else:
        print("✅ Google API Key detected!")
        print("🚀 Starting server with Gemini 2.0 Flash...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
