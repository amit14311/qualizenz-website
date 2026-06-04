-- Qualizenz database schema for future backend integration.
-- Suitable as a starting point for PostgreSQL, SQLite, MySQL, or Supabase with minor type adjustments.

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    slug VARCHAR(180) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    slug VARCHAR(280) NOT NULL UNIQUE,
    category_id INTEGER,
    author VARCHAR(150),
    publish_date DATE,
    status VARCHAR(30) DEFAULT 'draft',
    featured_image VARCHAR(500),
    summary TEXT,
    content TEXT,
    seo_meta_title VARCHAR(250),
    seo_meta_description TEXT,
    keywords TEXT,
    related_articles TEXT,
    call_to_action TEXT,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE sop_templates (
    id INTEGER PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    category VARCHAR(150),
    description TEXT,
    file_type VARCHAR(50),
    access_type VARCHAR(30) DEFAULT 'paid',
    price DECIMAL(10, 2),
    preview_url VARCHAR(500),
    download_url VARCHAR(500),
    purchase_url VARCHAR(500),
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE validation_templates (
    id INTEGER PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    category VARCHAR(150),
    description TEXT,
    file_type VARCHAR(50),
    access_type VARCHAR(30) DEFAULT 'paid',
    price DECIMAL(10, 2),
    preview_url VARCHAR(500),
    download_url VARCHAR(500),
    purchase_url VARCHAR(500),
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE free_resources (
    id INTEGER PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    category VARCHAR(150),
    description TEXT,
    file_type VARCHAR(50),
    download_url VARCHAR(500),
    email_capture_required BOOLEAN DEFAULT TRUE,
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE consulting_requests (
    id INTEGER PRIMARY KEY,
    name VARCHAR(180) NOT NULL,
    email VARCHAR(180) NOT NULL,
    phone VARCHAR(80),
    country VARCHAR(120),
    company VARCHAR(220),
    service_required VARCHAR(220),
    message TEXT,
    uploaded_document_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contact_messages (
    id INTEGER PRIMARY KEY,
    name VARCHAR(180) NOT NULL,
    email VARCHAR(180) NOT NULL,
    topic VARCHAR(180),
    message TEXT,
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE newsletter_subscribers (
    id INTEGER PRIMARY KEY,
    email VARCHAR(180) NOT NULL UNIQUE,
    source VARCHAR(120),
    status VARCHAR(50) DEFAULT 'subscribed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE downloads (
    id INTEGER PRIMARY KEY,
    resource_type VARCHAR(80),
    resource_id INTEGER,
    email VARCHAR(180),
    ip_address VARCHAR(80),
    user_agent TEXT,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE website_statistics (
    id INTEGER PRIMARY KEY,
    event_type VARCHAR(80),
    page_url VARCHAR(500),
    resource_type VARCHAR(80),
    resource_id INTEGER,
    referrer VARCHAR(500),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
