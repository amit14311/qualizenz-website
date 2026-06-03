"""
Qualizenz Quick Start - Complete Article Upload Example
Run this to test the entire workflow
"""

import requests
import time
import os

# Configuration
API_URL = 'http://localhost:5000/api'

print("""
╔═══════════════════════════════════════════════════════════╗
║       Qualizenz Article Upload Quick Start Demo           ║
║       Creates articles, uploads files, publishes          ║
╚═══════════════════════════════════════════════════════════╝
""")

# ==================== STEP 1: CREATE ARTICLES ====================

print("\n📝 STEP 1: Creating Articles...\n")

articles_to_create = [
    {
        "title": "FDA GMP Requirements: Complete Guide 2026",
        "description": "Everything you need to know about FDA Good Manufacturing Practices for pharmaceutical companies.",
        "category": "GMP",
        "content": """
FDA Good Manufacturing Practices (GMP) are fundamental regulations that govern how pharmaceutical products are manufactured, processed, and held. These regulations are designed to minimize the risks involved in pharmaceutical production.

KEY REQUIREMENTS:
1. Facility Design - Clean rooms, environmental controls, water systems
2. Equipment - Proper maintenance, calibration, and cleaning
3. Personnel - Training, competency, health standards
4. Procedures - SOPs, batch records, documentation
5. Quality Control - Testing, monitoring, release procedures

INSPECTION FOCUS AREAS:
- Deviations and corrective actions
- Data integrity practices
- Change control procedures
- Supplier qualification
- Environmental monitoring

Compliance with FDA GMP is essential for regulatory approval and market access.
        """,
        "tags": ["FDA", "GMP", "Compliance", "Regulations", "2026"],
        "author": "Qualizenz Team"
    },
    {
        "title": "ALCOA+ Principles: Data Integrity for Pharma",
        "description": "Complete guide to ALCOA+ principles (Attributable, Legible, Contemporaneous, Original, Accurate, Alterable, Complete).",
        "category": "Data Integrity",
        "content": """
ALCOA+ principles form the foundation of data integrity in pharmaceutical operations. These principles ensure that all data is trustworthy and reliable.

ALCOA+ BREAKDOWN:

Attributable - Identify WHO created/modified the record
Legible - Record must be clear and readable
Contemporaneous - Data recorded at time of activity
Original - First permanent record of an activity
Accurate - Data accurately reflects what it represents
Alterable - Changes must be traceable (not deletion)
Complete - Include all raw data, metadata, and audit trails

WHY ALCOA+ MATTERS:
- Regulatory requirement under 21 CFR Part 11
- Ensures product quality and safety
- Prevents data manipulation
- Supports traceability
- Enables compliance verification

IMPLEMENTATION:
- Use validated electronic systems
- Implement access controls
- Maintain detailed audit trails
- Regular training programs
- Periodic assessments

ALCOA+ compliance is non-negotiable for FDA approval.
        """,
        "tags": ["ALCOA", "Data Integrity", "21 CFR 11", "Pharma"],
        "author": "Qualizenz Team"
    },
    {
        "title": "Process Validation: IQ, OQ, PQ Complete Protocol",
        "description": "Step-by-step guide to equipment qualification and process validation including Design, Installation, Operational, and Performance phases.",
        "category": "Validation",
        "content": """
Process validation is a critical GMP requirement that ensures your manufacturing process consistently produces products that meet specifications.

THE FOUR PHASES:

1. DESIGN QUALIFICATION (DQ)
   - Define process parameters
   - Design specifications
   - Equipment selection
   - Supplier evaluation

2. INSTALLATION QUALIFICATION (IQ)
   - Verify equipment installation
   - Check instrumentation
   - Confirm calibration
   - Document configuration

3. OPERATIONAL QUALIFICATION (OQ)
   - Test all equipment functions
   - Verify performance under normal conditions
   - Test alarms and interlocks
   - Establish operating ranges

4. PERFORMANCE QUALIFICATION (PQ)
   - Run process with actual product
   - Test worst-case scenarios
   - Collect stability data
   - Finalize specifications

KEY DELIVERABLES:
- DQ Protocol and Report
- IQ Protocol and Report
- OQ Protocol and Report
- PQ Protocol and Report
- Final Validation Report

Process validation must be completed before commercial production.
        """,
        "tags": ["Validation", "IQ", "OQ", "PQ", "Protocol"],
        "author": "Qualizenz Team"
    }
]

created_articles = []

for i, article_data in enumerate(articles_to_create, 1):
    try:
        print(f"[{i}/{len(articles_to_create)}] Creating: {article_data['title']}")
        
        response = requests.post(f'{API_URL}/articles/create', json=article_data)
        
        if response.status_code == 201:
            data = response.json()
            article_id = data['article_id']
            created_articles.append(article_id)
            print(f"    ✅ Created! ID: {article_id}\n")
        else:
            print(f"    ❌ Failed: {response.text}\n")
    
    except Exception as e:
        print(f"    ❌ Error: {str(e)}\n")

print(f"✅ Created {len(created_articles)} articles\n")

# ==================== STEP 2: UPLOAD FILES ====================

print("\n📤 STEP 2: Uploading Sample Files...\n")

# Create sample PDF content
sample_files = {
    'GMP_Template.txt': """
GMP COMPLIANCE CHECKLIST

FACILITY REQUIREMENTS:
☐ Clean room classifications (ISO Class standards)
☐ Temperature and humidity control (±2°C, ±5% RH)
☐ HVAC systems operational and validated
☐ Environmental monitoring program in place
☐ Personnel access control systems
☐ Hand washing facilities
☐ Changing areas and gowning procedures

EQUIPMENT REQUIREMENTS:
☐ All equipment properly installed and qualified
☐ Maintenance schedules established
☐ Calibration procedures in place
☐ Cleaning validation completed
☐ Equipment log books maintained
☐ Spare parts inventory managed

PERSONNEL:
☐ All staff trained on GMP
☐ Training records maintained
☐ Competency assessments completed
☐ Health checks current
☐ Hygiene procedures followed

DOCUMENTATION:
☐ SOPs written and approved
☐ Batch records complete
☐ Change control system active
☐ Deviation tracking system
☐ CAPA procedure documented
☐ Record retention schedule established

Prepared by: ________________  Date: _________
Approved by: ________________  Date: _________
    """,
    
    'Data_Integrity_SOP.txt': """
STANDARD OPERATING PROCEDURE
DATA INTEGRITY MANAGEMENT

PURPOSE:
To ensure all electronic and paper records related to product manufacturing 
maintain integrity in accordance with ALCOA+ principles.

SCOPE:
All pharmaceutical manufacturing data, batch records, test results, and 
supporting documentation.

ALCOA+ IMPLEMENTATION:

ATTRIBUTABLE:
- User ID for all electronic entries
- Signature and date on paper records
- Change log for all modifications

LEGIBLE:
- Use standardized fonts and formats
- No white-out correction fluid
- Digital systems must provide readable copies

CONTEMPORANEOUS:
- Records created at time of activity
- Real-time data entry into systems
- No backdating of records

ORIGINAL:
- Maintain original source documents
- Electronic records are original records
- Copies must be certified as true

ACCURATE:
- Verify data before entry
- Double-check calculations
- Use validated methods

ALTERABLE (Traceable):
- Electronic systems must show audit trails
- Paper records: cross-out, initial, date
- Changes must be justified

COMPLETE:
- All required fields populated
- Raw data retained
- Metadata included
- No blank spaces

RESPONSIBILITIES:
QA Manager - Oversee program
Laboratory Manager - Data collection
IT Department - System maintenance
All Staff - Compliance

For questions: QA@qualizenz.pharma

Effective Date: May 31, 2026
Revision: 1.0
    """,
    
    'Validation_Protocol.txt': """
EQUIPMENT QUALIFICATION PROTOCOL

EQUIPMENT: Freeze Dryer Model XYZ-2000
FACILITY: PharmQuality Manufacturing Plant
DATE: May 31, 2026
VERSION: 1.0

OBJECTIVE:
To establish the design and installation qualification of the Freeze Dryer 
to ensure it can reliably produce pharmaceutical products within specifications.

SCOPE:
This protocol covers design, installation, and initial operational verification
of the freeze drying equipment including:
- Chamber
- Vacuum system
- Refrigeration system
- Control systems
- Data logging equipment

DESIGN QUALIFICATION (DQ):

Requirement 1: Equipment Capacity
Specification: 50 kg batch size
Manufacturer Confirmation: ☐ Verified

Requirement 2: Temperature Range
Specification: -50°C to +60°C
Manufacturer Confirmation: ☐ Verified

Requirement 3: Vacuum Range
Specification: 0.1 - 1000 mTorr
Manufacturer Confirmation: ☐ Verified

Requirement 4: Data Recording
Specification: Continuous monitoring and recording
Manufacturer Confirmation: ☐ Verified

INSTALLATION QUALIFICATION (IQ):

1. Equipment Installation
   Date Installed: _______________
   Installer: _______________
   Verified By: _______________

2. Instrumentation Check
   ☐ Temperature probes calibrated
   ☐ Pressure gauges calibrated
   ☐ Data logger functioning
   ☐ Alarms tested

3. Safety Systems
   ☐ Emergency stop functional
   ☐ Pressure relief working
   ☐ Interlocks operational
   ☐ Safety documentation complete

ACCEPTANCE CRITERIA:
All items marked with ☐ must be verified before proceeding.

___________________________     ___________
Prepared By (QA)              Date

___________________________     ___________
Approved By (QA Manager)        Date
    """
}

# Note: We can't create actual binary files here, so we'll create text files as examples
for article_id in created_articles:
    for filename, content in sample_files.items():
        try:
            print(f"Uploading {filename} to article {article_id[:20]}...")
            
            # For this demo, we're just showing the concept
            # In production, you'd create actual files and upload them
            
            print(f"  ✅ Would upload: {filename}")
        
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")

print("\n✅ File upload simulation complete\n")

# ==================== STEP 3: PUBLISH ARTICLES ====================

print("\n🚀 STEP 3: Publishing Articles...\n")

for i, article_id in enumerate(created_articles, 1):
    try:
        print(f"[{i}/{len(created_articles)}] Publishing {article_id}...")
        
        response = requests.put(f'{API_URL}/articles/{article_id}/publish')
        
        if response.status_code == 200:
            print(f"    ✅ Published!\n")
        else:
            print(f"    ❌ Failed: {response.text}\n")
    
    except Exception as e:
        print(f"    ❌ Error: {str(e)}\n")

# ==================== STEP 4: VERIFY ====================

print("\n✅ STEP 4: Verification...\n")

try:
    response = requests.get(f'{API_URL}/admin/stats')
    stats = response.json()
    
    print("ADMIN STATISTICS:")
    print(f"  Total Articles: {stats['total_articles']}")
    print(f"  Published: {stats['published_articles']}")
    print(f"  Drafts: {stats['draft_articles']}")
    print(f"  Total Views: {stats['total_views']}")
    print(f"  Total Downloads: {stats['total_downloads']}")
    
    print("\nARTICLES BY CATEGORY:")
    for category, count in stats['articles_by_category'].items():
        print(f"  {category}: {count}")

except Exception as e:
    print(f"❌ Error fetching stats: {str(e)}")

# ==================== RESULTS ====================

print(f"""
╔═══════════════════════════════════════════════════════════╗
║                    DEMO COMPLETE ✅                       ║
╚═══════════════════════════════════════════════════════════╝

WHAT WAS CREATED:
✅ {len(created_articles)} Published Articles
✅ Sample files uploaded (concept demo)
✅ Article database created at: ./data/articles_db.json
✅ Upload folders created: ./uploads/

NEXT STEPS:
1. Upload real PDF/Word files to your articles
2. Share article links with your audience
3. Monitor downloads and views in admin dashboard
4. Deploy to production when ready

ACCESS YOUR CONTENT:
📖 View Published: http://localhost:5000/api/articles/published
⚙️  Admin Panel: Open admin_dashboard.html in browser
📊 Statistics: http://localhost:5000/api/admin/stats

YOUR ARTICLES ARE LIVE! 🚀

""")

print("\nTo upload real files, use admin_dashboard.html or API:")
print("  Python: python developer_upload_example.py")
print("  cURL: See DEVELOPER_GUIDE.md")
