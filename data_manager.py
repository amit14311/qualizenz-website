"""
Qualizenz - Content Generator & Data Management Utility
Handles AI-powered content generation, template creation, and analytics reporting
"""

import json
import csv
from datetime import datetime
from pathlib import Path

class QualizenzDataManager:
    """Manage all data for PharmQuality360"""
    
    def __init__(self, data_dir='./data'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def generate_article(self, title, category, content, tags=None):
        """Generate article record"""
        article = {
            'id': f"article_{datetime.now().timestamp()}",
            'title': title,
            'category': category,  # GMP, QA, QC, Validation, etc
            'content': content,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'views': 0,
            'shares': 0
        }
        return article
    
    def generate_template(self, title, category, template_type='free'):
        """Generate template record"""
        template = {
            'id': f"template_{datetime.now().timestamp()}",
            'title': title,
            'category': category,  # QA, QC, Production, etc
            'type': template_type,  # free or premium
            'created_at': datetime.now().isoformat(),
            'downloads': 0,
            'rating': 0,
            'file_path': f"templates/{category}/{title.replace(' ', '_')}.docx"
        }
        return template
    
    def generate_course(self, title, description, modules, duration_days):
        """Generate course record"""
        course = {
            'id': f"course_{datetime.now().timestamp()}",
            'title': title,
            'description': description,
            'modules': modules,
            'duration_days': duration_days,
            'created_at': datetime.now().isoformat(),
            'students_enrolled': 0,
            'price': 9.99,  # Default price
            'rating': 0
        }
        return course
    
    def save_articles_json(self, articles, filename='articles.json'):
        """Save articles to JSON file"""
        filepath = self.data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(articles)} articles to {filename}")
    
    def save_templates_json(self, templates, filename='templates.json'):
        """Save templates to JSON file"""
        filepath = self.data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(templates, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(templates)} templates to {filename}")
    
    def save_to_csv(self, data, filename, fieldnames):
        """Save data to CSV file"""
        filepath = self.data_dir / filename
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"✅ Saved to {filename}")
    
    def load_json(self, filename):
        """Load JSON file"""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def generate_report(self):
        """Generate analytics report"""
        subscribers = self.load_json('subscribers.json')
        contacts = self.load_json('contacts.json')
        downloads = self.load_json('downloads.json')
        articles = self.load_json('articles.json')
        templates = self.load_json('templates.json')
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'statistics': {
                'total_email_subscribers': len(subscribers),
                'total_contact_messages': len(contacts),
                'total_template_downloads': len(downloads),
                'total_articles': len(articles),
                'total_templates': len(templates),
            }
        }
        
        print("\n" + "="*60)
        print("📊 PharmQuality360 Analytics Report")
        print("="*60)
        print(f"Generated: {report['generated_at']}")
        print(f"📧 Email Subscribers: {report['statistics']['total_email_subscribers']}")
        print(f"💬 Contact Messages: {report['statistics']['total_contact_messages']}")
        print(f"📥 Template Downloads: {report['statistics']['total_template_downloads']}")
        print(f"📝 Articles Published: {report['statistics']['total_articles']}")
        print(f"📋 Templates Available: {report['statistics']['total_templates']}")
        print("="*60 + "\n")
        
        return report


# SAMPLE DATA GENERATOR
def generate_sample_data():
    """Generate sample articles and templates for testing"""
    
    manager = QualizenzDataManager()
    
    # Sample Articles
    sample_articles = [
        manager.generate_article(
            title="Complete Guide to FDA GMP Compliance",
            category="GMP",
            content="Comprehensive overview of FDA Good Manufacturing Practices requirements...",
            tags=["FDA", "GMP", "Compliance", "Regulations"]
        ),
        manager.generate_article(
            title="Data Integrity: 21 CFR Part 11 Explained",
            category="Data Integrity",
            content="Understanding electronic records and data integrity requirements...",
            tags=["Data Integrity", "21 CFR 11", "ALCOA+"]
        ),
        manager.generate_article(
            title="Process Validation: IQ, OQ, PQ Protocol",
            category="Validation",
            content="Step-by-step guide for equipment and process validation...",
            tags=["Validation", "IQ", "OQ", "PQ"]
        ),
        manager.generate_article(
            title="CAPA System: Root Cause Analysis Best Practices",
            category="Quality Assurance",
            content="How to implement effective CAPA processes...",
            tags=["CAPA", "Root Cause", "Quality"]
        ),
    ]
    
    # Sample Templates
    sample_templates = [
        manager.generate_template(
            title="SOP Template - Equipment Maintenance",
            category="QA",
            template_type="free"
        ),
        manager.generate_template(
            title="CAPA Form - Complete Package",
            category="QA",
            template_type="premium"
        ),
        manager.generate_template(
            title="Change Control Protocol",
            category="Production",
            template_type="free"
        ),
        manager.generate_template(
            title="Analytical Method Validation Checklist",
            category="QC",
            template_type="premium"
        ),
    ]
    
    # Sample Contacts
    sample_contacts = [
        {
            'name': 'John Doe',
            'email': 'john@pharma.com',
            'topic': 'training',
            'message': 'Interested in GMP training courses',
            'submitted_at': datetime.now().isoformat()
        }
    ]
    
    # Sample Subscribers
    sample_subscribers = [
        'qa.professional@pharma.com',
        'validation.expert@company.com',
        'quality.manager@pharma.co'
    ]
    
    # Save all data
    manager.save_articles_json(sample_articles)
    manager.save_templates_json(sample_templates)
    manager.save_to_csv(sample_contacts, 'contacts.csv', ['name', 'email', 'topic', 'message', 'submitted_at'])
    manager.save_to_csv([{'email': email} for email in sample_subscribers], 'subscribers.csv', ['email'])
    
    # Generate report
    manager.generate_report()
    
    print("\n✅ Sample data generated successfully!")
    print("📁 Data files location: ./data/")


# CONTENT GENERATION HELPER
class ContentGenerator:
    """Generate pharmaceutical content using templates"""
    
    @staticmethod
    def generate_sop_template(title, process, department='Quality Assurance'):
        """Generate SOP template structure"""
        return {
            'title': f"SOP: {title}",
            'department': department,
            'process_description': process,
            'objective': f"To establish standard operating procedure for {title}",
            'scope': "All personnel involved in this operation",
            'responsibilities': {
                'QA Manager': "Approval and oversight",
                'Operations': "Execution and compliance",
                'QC': "Testing and verification"
            },
            'procedure': [
                "Step 1: Preparation",
                "Step 2: Execution",
                "Step 3: Verification",
                "Step 4: Documentation"
            ],
            'safety_precautions': "All applicable regulatory and safety guidelines",
            'revision_history': [{
                'version': '1.0',
                'date': datetime.now().isoformat(),
                'changes': 'Initial version'
            }]
        }
    
    @staticmethod
    def generate_validation_protocol(equipment_name, facility_id):
        """Generate equipment validation protocol structure"""
        return {
            'protocol_id': f"VAL-{facility_id}-{datetime.now().strftime('%Y%m%d')}",
            'equipment': equipment_name,
            'facility_id': facility_id,
            'created_date': datetime.now().isoformat(),
            'phases': {
                'DQ': {
                    'description': 'Design Qualification',
                    'status': 'Pending',
                    'documents': []
                },
                'IQ': {
                    'description': 'Installation Qualification',
                    'status': 'Pending',
                    'documents': []
                },
                'OQ': {
                    'description': 'Operational Qualification',
                    'status': 'Pending',
                    'documents': []
                },
                'PQ': {
                    'description': 'Performance Qualification',
                    'status': 'Pending',
                    'documents': []
                }
            }
        }


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║    Qualizenz - Content Manager & Data Utility             ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Generate sample data
    generate_sample_data()
    
    # Demo content generation
    print("\n📝 Content Generation Demo:\n")
    
    sop = ContentGenerator.generate_sop_template(
        title="Cleaning Validation",
        process="Validation of cleaning procedures for pharmaceutical equipment"
    )
    print("Generated SOP Template:")
    print(json.dumps(sop, indent=2))
    
    protocol = ContentGenerator.generate_validation_protocol(
        equipment_name="Freeze Dryer XYZ-2000",
        facility_id="FAC001"
    )
    print("\nGenerated Validation Protocol:")
    print(json.dumps(protocol, indent=2))
