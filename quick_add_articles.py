"""
Quick Article Adder for Qualizenz
Add articles to your website instantly!
"""

import requests
import json
from datetime import datetime

# ============================================
# QUICK ADD - Just fill in the blanks
# ============================================

# ARTICLE 1
article_1 = {
    "title": "FDA GMP Requirements: Complete Guide 2026",
    "content": "The FDA Good Manufacturing Practices (GMP) are fundamental regulations that all pharmaceutical manufacturers must follow. This comprehensive guide covers all key requirements including facility design, equipment maintenance, personnel qualifications, and documentation practices. Learn what inspectors look for and how to ensure compliance.",
    "category": "GMP",
    "tags": ["FDA", "GMP", "Compliance", "Regulations", "2026"],
    "author": "Qualizenz Team"
}

# ARTICLE 2
article_2 = {
    "title": "ALCOA+ Principles: Data Integrity Explained",
    "content": "ALCOA+ stands for Attributable, Legible, Contemporaneous, Original, and Accurate. These principles, plus Alterable and Complete, form the foundation of data integrity in pharmaceutical operations. This article explains each principle with real-world examples and implementation strategies for achieving compliance with 21 CFR Part 11.",
    "category": "Data Integrity",
    "tags": ["ALCOA", "Data Integrity", "21 CFR 11", "Electronic Records"],
    "author": "Qualizenz Team"
}

# ARTICLE 3
article_3 = {
    "title": "Process Validation: IQ, OQ, PQ Protocol",
    "content": "Process validation ensures that your manufacturing process consistently produces products that meet specifications. Learn about the four critical phases: Design Qualification (DQ), Installation Qualification (IQ), Operational Qualification (OQ), and Performance Qualification (PQ). This complete guide includes templates and case studies.",
    "category": "Validation",
    "tags": ["Validation", "IQ", "OQ", "PQ", "Process Validation"],
    "author": "Qualizenz Team"
}

# ARTICLE 4
article_4 = {
    "title": "CAPA System: Root Cause Analysis Best Practices",
    "content": "A strong CAPA (Corrective and Preventive Action) system is essential for maintaining product quality. This guide walks you through the complete process from identifying deviations to implementing preventive measures. Learn root cause analysis techniques, effectiveness checks, and how to avoid repeat issues.",
    "category": "Quality Assurance",
    "tags": ["CAPA", "Root Cause Analysis", "Deviations", "Quality"],
    "author": "Qualizenz Team"
}

# ARTICLE 5
article_5 = {
    "title": "OOS Investigation: Out-of-Specification Guide",
    "content": "Out-of-Specification (OOS) results indicate that a product test result falls outside established limits. This comprehensive guide explains the investigation process, when to reject results, statistical tools for analysis, and preventive measures. Includes real-world case studies and decision trees.",
    "category": "Quality Control",
    "tags": ["OOS", "Testing", "Quality Control", "Investigation"],
    "author": "Qualizenz Team"
}

# ============================================
# FUNCTION TO ADD ARTICLES
# ============================================

def add_article_to_backend(article, api_url="http://localhost:5000"):
    """
    Add article to Qualizenz backend
    Requires: python app.py to be running
    """
    try:
        url = f"{api_url}/api/articles/add"
        response = requests.post(url, json=article)
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ SUCCESS: {article['title']}")
            print(f"   Article ID: {data.get('article_id')}")
            print(f"   Total articles: {data.get('total_articles')}\n")
            return True
        else:
            print(f"❌ FAILED: {article['title']}")
            print(f"   Error: {response.text}\n")
            return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

# ============================================
# MAIN: ADD ALL ARTICLES
# ============================================

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║    Qualizenz Quick Article Adder                          ║
    ║    Make sure: python app.py is running first!             ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # List of all articles to add
    articles = [article_1, article_2, article_3, article_4, article_5]
    
    print(f"📝 Adding {len(articles)} articles...\n")
    
    success_count = 0
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] Adding: {article['title']}")
        if add_article_to_backend(article):
            success_count += 1
    
    print("="*60)
    print(f"📊 RESULTS: {success_count}/{len(articles)} articles added successfully")
    print("="*60)
    
    if success_count == len(articles):
        print("\n✅ All articles added! Open index.html to see them.")
    else:
        print("\n⚠️ Some articles failed. Make sure:")
        print("   1. python app.py is running")
        print("   2. Server is at http://localhost:5000")
        print("   3. Network connection is active")
