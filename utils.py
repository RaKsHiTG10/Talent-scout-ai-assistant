# utils.py
import re
import json
import os
from datetime import datetime

def validate_email(email):
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone number format."""
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    # Check if result is numeric and reasonable length
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15

def save_candidate_data(candidate_info):
    """Save candidate information to a JSON file."""
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Generate a unique filename using timestamp and name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    name = candidate_info.get("name", "unknown").lower().replace(" ", "_")
    filename = f"data/candidate_{name}_{timestamp}.json"
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(candidate_info, f, indent=4)
    
    return filename

def extract_technologies(tech_stack_text):
    """Extract and categorize technologies from the candidate's tech stack."""
    # Common categories and their keywords
    categories = {
        "programming_languages": [
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", 
            "php", "swift", "kotlin", "go", "rust", "scala", "perl"
        ],
        "frontend": [
            "react", "angular", "vue", "svelte", "html", "css", "bootstrap", 
            "tailwind", "sass", "less", "jquery"
        ],
        "backend": [
            "node", "express", "django", "flask", "spring", "laravel", "rails", 
            "fastapi", "asp.net", "symfony"
        ],
        "databases": [
            "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", 
            "cassandra", "redis", "elasticsearch", "dynamodb", "mariadb"
        ],
        "devops": [
            "docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "gitlab", 
            "github", "terraform", "ansible", "ci/cd", "linux"
        ],
        "mobile": [
            "android", "ios", "react native", "flutter", "xamarin", "swift", 
            "kotlin", "objective-c"
        ],
        "ai_ml": [
            "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", 
            "opencv", "nlp", "computer vision", "machine learning"
        ]
    }
    
    result = {category: [] for category in categories}
    
    # Convert to lowercase for case-insensitive matching
    text_lower = tech_stack_text.lower()
    
    # Extract technologies for each category
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text_lower:
                # Check if it's a whole word match
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    result[category].append(keyword)
    
    # Remove empty categories
    result = {k: v for k, v in result.items() if v}
    
    return result
