"""
Qualizenz Article Management System with Upload & Download
Full-featured content management for developers
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path
import mimetypes
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# ==================== CONFIGURATION ====================

# File upload settings
UPLOAD_FOLDER = Path('./uploads')
ARTICLES_FOLDER = UPLOAD_FOLDER / 'articles'
PDF_FOLDER = UPLOAD_FOLDER / 'pdfs'
WORD_FOLDER = UPLOAD_FOLDER / 'documents'

# Create folders if they don't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
ARTICLES_FOLDER.mkdir(exist_ok=True)
PDF_FOLDER.mkdir(exist_ok=True)
WORD_FOLDER.mkdir(exist_ok=True)

# Maximum file sizes
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'md', 'html', 'zip'}

# Data storage
DATA_DIR = Path('./data')
DATA_DIR.mkdir(exist_ok=True)
ARTICLES_DB = DATA_DIR / 'articles_db.json'

# ==================== UTILITY FUNCTIONS ====================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_articles_db():
    """Load articles database"""
    if ARTICLES_DB.exists():
        with open(ARTICLES_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_articles_db(articles):
    """Save articles database"""
    with open(ARTICLES_DB, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

def generate_article_id():
    """Generate unique article ID"""
    return f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# ==================== ARTICLE MANAGEMENT ====================

@app.route('/api/articles/create', methods=['POST'])
def create_article():
    """Create new article with metadata"""
    try:
        data = request.json
        
        article = {
            'id': generate_article_id(),
            'title': data.get('title'),
            'description': data.get('description'),
            'category': data.get('category'),
            'tags': data.get('tags', []),
            'author': data.get('author', 'Qualizenz Team'),
            'content': data.get('content', ''),  # Article body content
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'draft',  # draft, published, archived
            'views': 0,
            'downloads': 0,
            'files': []  # List of attached files
        }
        
        articles = load_articles_db()
        articles.append(article)
        save_articles_db(articles)
        
        return jsonify({
            'success': True,
            'message': 'Article created',
            'article_id': article['id'],
            'article': article
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<article_id>/publish', methods=['PUT'])
def publish_article(article_id):
    """Publish an article (make it visible)"""
    try:
        articles = load_articles_db()
        
        for article in articles:
            if article['id'] == article_id:
                article['status'] = 'published'
                article['updated_at'] = datetime.now().isoformat()
                save_articles_db(articles)
                
                return jsonify({
                    'success': True,
                    'message': 'Article published',
                    'article': article
                }), 200
        
        return jsonify({'error': 'Article not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/published', methods=['GET'])
def get_published_articles():
    """Get all published articles (public)"""
    articles = load_articles_db()
    published = [a for a in articles if a['status'] == 'published']
    
    return jsonify({
        'total': len(published),
        'articles': published
    })

@app.route('/api/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    """Get single article"""
    articles = load_articles_db()
    
    for article in articles:
        if article['id'] == article_id:
            # Increment views
            article['views'] = article.get('views', 0) + 1
            save_articles_db(articles)
            
            return jsonify({
                'success': True,
                'article': article
            }), 200
    
    return jsonify({'error': 'Article not found'}), 404

# ==================== FILE UPLOAD ====================

@app.route('/api/articles/<article_id>/upload-file', methods=['POST'])
def upload_file_to_article(article_id):
    """Upload file (PDF, Word, etc.) to an article"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large (max 50MB)'}), 400
        
        # Get file extension
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        
        # Determine folder based on file type
        if file_ext == 'pdf':
            save_folder = PDF_FOLDER
        elif file_ext in ['doc', 'docx']:
            save_folder = WORD_FOLDER
        else:
            save_folder = ARTICLES_FOLDER
        
        # Save file with secure name
        filename = secure_filename(f"{article_id}_{datetime.now().timestamp()}.{file_ext}")
        filepath = save_folder / filename
        file.save(filepath)
        
        # Update article in database
        articles = load_articles_db()
        for article in articles:
            if article['id'] == article_id:
                file_record = {
                    'filename': filename,
                    'original_name': secure_filename(file.filename),
                    'file_type': file_ext,
                    'size_mb': round(file_size / 1024 / 1024, 2),
                    'uploaded_at': datetime.now().isoformat(),
                    'download_count': 0
                }
                
                if 'files' not in article:
                    article['files'] = []
                
                article['files'].append(file_record)
                article['updated_at'] = datetime.now().isoformat()
                save_articles_db(articles)
                
                return jsonify({
                    'success': True,
                    'message': 'File uploaded',
                    'file': file_record,
                    'download_url': f'/api/files/download/{filename}'
                }), 201
        
        return jsonify({'error': 'Article not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== FILE DOWNLOAD ====================

@app.route('/api/files/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file"""
    try:
        # Security check - verify filename
        filename = secure_filename(filename)
        
        # Try to find file in any folder
        for folder in [PDF_FOLDER, WORD_FOLDER, ARTICLES_FOLDER]:
            filepath = folder / filename
            if filepath.exists():
                # Log download
                log_download(filename)
                
                # Send file
                return send_file(
                    filepath,
                    as_attachment=True,
                    download_name=filename
                )
        
        return jsonify({'error': 'File not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def log_download(filename):
    """Log file downloads"""
    downloads = []
    downloads_file = DATA_DIR / 'downloads.json'
    
    if downloads_file.exists():
        with open(downloads_file, 'r') as f:
            downloads = json.load(f)
    
    downloads.append({
        'filename': filename,
        'timestamp': datetime.now().isoformat(),
        'user_ip': request.remote_addr
    })
    
    with open(downloads_file, 'w') as f:
        json.dump(downloads, f, indent=2)

# ==================== ARTICLE CONTENT VIEW ====================

@app.route('/api/articles/<article_id>/content', methods=['GET'])
def get_article_content(article_id):
    """Get article content as HTML"""
    try:
        articles = load_articles_db()
        
        for article in articles:
            if article['id'] == article_id and article['status'] == 'published':
                # Convert markdown to HTML if needed
                html_content = f"""
                <div class="article-view">
                    <h1>{article['title']}</h1>
                    <div class="article-meta">
                        <span>By {article['author']}</span> | 
                        <span>{article['created_at'][:10]}</span> |
                        <span>{article['views']} views</span>
                    </div>
                    <div class="article-body">
                        {article.get('content', '').replace(chr(10), '<br>')}
                    </div>
                    
                    <div class="article-files">
                        <h3>📥 Downloads</h3>
                        <ul>
                """
                
                for file in article.get('files', []):
                    html_content += f"""
                        <li>
                            <a href="/api/files/download/{file['filename']}">
                                📄 {file['original_name']} ({file['size_mb']}MB)
                            </a>
                            <span style="color: #999; font-size: 0.9em;">
                                {file['download_count']} downloads
                            </span>
                        </li>
                    """
                
                html_content += """
                        </ul>
                    </div>
                </div>
                """
                
                return jsonify({
                    'success': True,
                    'html': html_content,
                    'article': article
                }), 200
        
        return jsonify({'error': 'Article not found or not published'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ADMIN ENDPOINTS ====================

@app.route('/api/admin/articles', methods=['GET'])
def admin_list_articles():
    """List all articles (draft + published) - admin only"""
    articles = load_articles_db()
    
    return jsonify({
        'total': len(articles),
        'articles': articles,
        'stats': {
            'published': len([a for a in articles if a['status'] == 'published']),
            'draft': len([a for a in articles if a['status'] == 'draft']),
            'archived': len([a for a in articles if a['status'] == 'archived'])
        }
    })

@app.route('/api/admin/articles/<article_id>/delete', methods=['DELETE'])
def delete_article(article_id):
    """Delete an article"""
    try:
        articles = load_articles_db()
        articles = [a for a in articles if a['id'] != article_id]
        save_articles_db(articles)
        
        return jsonify({'success': True, 'message': 'Article deleted'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/articles/<article_id>/update', methods=['PUT'])
def update_article(article_id):
    """Update article metadata"""
    try:
        data = request.json
        articles = load_articles_db()
        
        for article in articles:
            if article['id'] == article_id:
                article.update({
                    'title': data.get('title', article['title']),
                    'description': data.get('description', article['description']),
                    'category': data.get('category', article['category']),
                    'tags': data.get('tags', article['tags']),
                    'content': data.get('content', article['content']),
                    'updated_at': datetime.now().isoformat()
                })
                save_articles_db(articles)
                
                return jsonify({
                    'success': True,
                    'message': 'Article updated',
                    'article': article
                }), 200
        
        return jsonify({'error': 'Article not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== STATISTICS ====================

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get admin statistics"""
    articles = load_articles_db()
    
    total_downloads = 0
    for article in articles:
        for file in article.get('files', []):
            total_downloads += file.get('download_count', 0)
    
    total_views = sum(a.get('views', 0) for a in articles)
    
    return jsonify({
        'total_articles': len(articles),
        'published_articles': len([a for a in articles if a['status'] == 'published']),
        'draft_articles': len([a for a in articles if a['status'] == 'draft']),
        'total_views': total_views,
        'total_downloads': total_downloads,
        'articles_by_category': get_articles_by_category(articles)
    })

def get_articles_by_category(articles):
    """Get count of articles by category"""
    categories = {}
    for article in articles:
        category = article.get('category', 'Uncategorized')
        categories[category] = categories.get(category, 0) + 1
    return categories

# ==================== ERROR HANDLERS ====================

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large"""
    return jsonify({'error': 'File too large (max 50MB)'}), 413

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

# ==================== MAIN ====================

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║      Qualizenz Content Management System                  ║
    ║      Complete Article Upload & Download Management        ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🚀 Server starting on http://localhost:5000
    
    📁 Upload Folders:
       - Articles: ./uploads/articles/
       - PDFs: ./uploads/pdfs/
       - Documents: ./uploads/documents/
    
    💾 Database: ./data/articles_db.json
    
    API ENDPOINTS:
    
    📝 ARTICLE MANAGEMENT:
       POST   /api/articles/create              - Create new article
       GET    /api/articles/published           - List published articles
       GET    /api/articles/<id>                - Get single article
       GET    /api/articles/<id>/content        - Get article with content
       PUT    /api/articles/<id>/publish        - Publish an article
       PUT    /api/admin/articles/<id>/update   - Update article
       DELETE /api/admin/articles/<id>/delete   - Delete article
    
    📤 FILE UPLOAD:
       POST   /api/articles/<id>/upload-file    - Upload file to article
       GET    /api/files/download/<filename>    - Download file
    
    📊 ADMIN:
       GET    /api/admin/articles               - List all articles
       GET    /api/admin/stats                  - Get statistics
    
    📘 USAGE:
       1. Create article: POST /api/articles/create
       2. Upload files: POST /api/articles/<id>/upload-file
       3. Publish: PUT /api/articles/<id>/publish
       4. Users read: GET /api/articles/published
       5. Users download: GET /api/files/download/<filename>
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
