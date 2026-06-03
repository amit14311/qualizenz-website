"""
PharmQuality360 Backend Server
Flask application for handling form submissions, analytics, and data management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Data storage directory
DATA_DIR = Path('./data')
DATA_DIR.mkdir(exist_ok=True)

# Data file paths
SUBSCRIBERS_FILE = DATA_DIR / 'subscribers.json'
CONTACTS_FILE = DATA_DIR / 'contacts.json'
DOWNLOADS_FILE = DATA_DIR / 'downloads.json'
ANALYTICS_FILE = DATA_DIR / 'analytics.json'
ARTICLES_FILE = DATA_DIR / 'articles.json'
TEMPLATES_FILE = DATA_DIR / 'templates.json'

def load_json_file(filepath):
    """Load JSON data from file"""
    if not filepath.exists():
        return []
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_json_file(filepath, data):
    """Save JSON data to file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    return True

# ==================== NEWSLETTER ENDPOINTS ====================

@app.route('/api/newsletter/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Add email to newsletter subscribers"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        
        if not email or '@' not in email:
            return jsonify({'error': 'Invalid email address'}), 400
        
        subscribers = load_json_file(SUBSCRIBERS_FILE)
        
        if email in subscribers:
            return jsonify({
                'success': False,
                'message': 'Email already subscribed'
            }), 200
        
        subscribers.append(email)
        save_json_file(SUBSCRIBERS_FILE, subscribers)
        
        # Log analytics
        log_event('newsletter_subscribe', {'email': email})
        
        return jsonify({
            'success': True,
            'message': 'Successfully subscribed',
            'total_subscribers': len(subscribers)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/newsletter/subscribers', methods=['GET'])
def get_subscribers_count():
    """Get total subscriber count"""
    subscribers = load_json_file(SUBSCRIBERS_FILE)
    return jsonify({
        'total_subscribers': len(subscribers),
        'last_updated': datetime.now().isoformat()
    })

# ==================== CONTACT FORM ENDPOINTS ====================

@app.route('/api/contact/submit', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    try:
        data = request.json
        
        contact_record = {
            'name': data.get('name', 'Anonymous').strip(),
            'email': data.get('email', '').strip(),
            'topic': data.get('topic', 'general'),
            'message': data.get('message', '').strip(),
            'submitted_at': datetime.now().isoformat()
        }
        
        if not contact_record['email'] or not contact_record['message']:
            return jsonify({'error': 'Email and message are required'}), 400
        
        contacts = load_json_file(CONTACTS_FILE)
        contacts.append(contact_record)
        save_json_file(CONTACTS_FILE, contacts)
        
        log_event('contact_form_submit', contact_record)
        
        return jsonify({
            'success': True,
            'message': 'Thank you for contacting us',
            'total_contacts': len(contacts)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact/list', methods=['GET'])
def get_contacts():
    """Get all contact messages (admin only)"""
    contacts = load_json_file(CONTACTS_FILE)
    return jsonify({
        'total_contacts': len(contacts),
        'contacts': contacts
    })

# ==================== TEMPLATE DOWNLOAD TRACKING ====================

@app.route('/api/templates/download', methods=['POST'])
def track_template_download():
    """Track template downloads"""
    try:
        data = request.json
        template_id = data.get('template_id')
        
        download_record = {
            'template_id': template_id,
            'user_ip': request.remote_addr,
            'downloaded_at': datetime.now().isoformat()
        }
        
        downloads = load_json_file(DOWNLOADS_FILE)
        downloads.append(download_record)
        save_json_file(DOWNLOADS_FILE, downloads)
        
        log_event('template_download', download_record)
        
        return jsonify({
            'success': True,
            'message': 'Download tracked',
            'total_downloads': len(downloads)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates/download-stats', methods=['GET'])
def get_download_stats():
    """Get download statistics by template"""
    downloads = load_json_file(DOWNLOADS_FILE)
    
    stats = {}
    for download in downloads:
        template_id = download.get('template_id')
        stats[template_id] = stats.get(template_id, 0) + 1
    
    return jsonify({
        'total_downloads': len(downloads),
        'templates_stats': stats
    })

# ==================== ANALYTICS ENDPOINTS ====================

def log_event(event_name, event_data=None):
    """Log analytics event"""
    analytics = load_json_file(ANALYTICS_FILE)
    
    event = {
        'event_name': event_name,
        'event_data': event_data or {},
        'timestamp': datetime.now().isoformat(),
        'user_ip': request.remote_addr if request else None
    }
    
    analytics.append(event)
    save_json_file(ANALYTICS_FILE, analytics)

@app.route('/api/analytics/page-view', methods=['POST'])
def track_page_view():
    """Track page views"""
    try:
        data = request.json
        
        log_event('page_view', {
            'page': data.get('page'),
            'referrer': data.get('referrer')
        })
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Get analytics dashboard data"""
    subscribers = load_json_file(SUBSCRIBERS_FILE)
    contacts = load_json_file(CONTACTS_FILE)
    downloads = load_json_file(DOWNLOADS_FILE)
    analytics = load_json_file(ANALYTICS_FILE)
    
    # Count events
    page_views = len([e for e in analytics if e.get('event_name') == 'page_view'])
    
    return jsonify({
        'total_subscribers': len(subscribers),
        'total_contacts': len(contacts),
        'total_downloads': len(downloads),
        'total_page_views': page_views,
        'last_updated': datetime.now().isoformat()
    })

# ==================== ARTICLES ENDPOINTS ====================

@app.route('/api/articles/list', methods=['GET'])
def get_articles():
    """Get all articles"""
    articles = load_json_file(ARTICLES_FILE)
    return jsonify({
        'total_articles': len(articles),
        'articles': articles
    })

@app.route('/api/articles/add', methods=['POST'])
def add_article():
    """Add new article (AI-generated or manual)"""
    try:
        data = request.json
        
        article = {
            'id': data.get('id', f"article_{datetime.now().timestamp()}"),
            'title': data.get('title'),
            'content': data.get('content'),
            'category': data.get('category', 'GMP'),
            'tags': data.get('tags', []),
            'author': data.get('author', 'PharmQuality360'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        articles = load_json_file(ARTICLES_FILE)
        articles.append(article)
        save_json_file(ARTICLES_FILE, articles)
        
        log_event('article_published', {'article_id': article['id']})
        
        return jsonify({
            'success': True,
            'message': 'Article published',
            'article_id': article['id'],
            'total_articles': len(articles)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== TEMPLATES ENDPOINTS ====================

@app.route('/api/templates/list', methods=['GET'])
def get_templates():
    """Get all templates"""
    templates = load_json_file(TEMPLATES_FILE)
    return jsonify({
        'total_templates': len(templates),
        'templates': templates
    })

@app.route('/api/templates/add', methods=['POST'])
def add_template():
    """Add new template"""
    try:
        data = request.json
        
        template = {
            'id': data.get('id', f"template_{datetime.now().timestamp()}"),
            'title': data.get('title'),
            'description': data.get('description'),
            'category': data.get('category', 'QA'),
            'type': data.get('type', 'free'),  # free or premium
            'download_url': data.get('download_url'),
            'created_at': datetime.now().isoformat()
        }
        
        templates = load_json_file(TEMPLATES_FILE)
        templates.append(template)
        save_json_file(TEMPLATES_FILE, templates)
        
        return jsonify({
            'success': True,
            'message': 'Template added',
            'template_id': template['id'],
            'total_templates': len(templates)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH & STATUS ENDPOINTS ====================

@app.route('/api/status', methods=['GET'])
def api_status():
    """API health check"""
    return jsonify({
        'status': 'online',
        'service': 'Qualizenz Backend',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get comprehensive statistics"""
    subscribers = load_json_file(SUBSCRIBERS_FILE)
    contacts = load_json_file(CONTACTS_FILE)
    downloads = load_json_file(DOWNLOADS_FILE)
    articles = load_json_file(ARTICLES_FILE)
    templates = load_json_file(TEMPLATES_FILE)
    
    return jsonify({
        'subscribers': len(subscribers),
        'contacts': len(contacts),
        'downloads': len(downloads),
        'articles': len(articles),
        'templates': len(templates),
        'timestamp': datetime.now().isoformat()
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║      Qualizenz Backend Server                             ║
    ║      Flask API for Content Management & Analytics         ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Server starting on http://localhost:5000
    
    Available endpoints:
    
    Newsletter:
    - POST   /api/newsletter/subscribe
    - GET    /api/newsletter/subscribers
    
    Contacts:
    - POST   /api/contact/submit
    - GET    /api/contact/list
    
    Templates:
    - GET    /api/templates/list
    - POST   /api/templates/add
    - POST   /api/templates/download
    - GET    /api/templates/download-stats
    
    Articles:
    - GET    /api/articles/list
    - POST   /api/articles/add
    
    Analytics:
    - POST   /api/analytics/page-view
    - GET    /api/analytics/dashboard
    
    Status:
    - GET    /api/status
    - GET    /api/stats
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
