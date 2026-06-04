// SMOOTH SCROLL NAVIGATION
function scrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// NEWSLETTER FORM HANDLING
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.getElementById('newsletterForm');
    const newsletterMessage = document.getElementById('newsletterMessage');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('newsletterEmail').value;
            
            // Save to local storage for demo
            let subscribers = JSON.parse(localStorage.getItem('subscribers')) || [];
            
            if (!subscribers.includes(email)) {
                subscribers.push(email);
                localStorage.setItem('subscribers', JSON.stringify(subscribers));
                
                // Show success message
                newsletterMessage.innerHTML = `
                    <div class="success-message" style="
                        background-color: #D1FAE5;
                        color: #065F46;
                        padding: 12px;
                        border-radius: 6px;
                        margin-top: 1rem;
                    ">
                        Success. Thank you! You are on the Qualizenz article update list.
                    </div>
                `;
                
                // Log to console for debugging
                console.log('Newsletter subscriber added:', email);
                console.log('Total subscribers:', subscribers.length);
                
                // Reset form
                newsletterForm.reset();
                
                // Clear message after 5 seconds
                setTimeout(() => {
                    newsletterMessage.innerHTML = '';
                }, 5000);
            } else {
                newsletterMessage.innerHTML = `
                    <div class="warning-message" style="
                        background-color: #FEF3C7;
                        color: #92400E;
                        padding: 12px;
                        border-radius: 6px;
                        margin-top: 1rem;
                    ">
                        You are already subscribed.
                    </div>
                `;
            }
        });
    }

    // TOPIC SUGGESTION FORM HANDLING
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(contactForm);
            const name = formData.get('name') || 'Anonymous';
            const email = formData.get('email') || 'no-email@example.com';
            const topic = formData.get('topic') || 'general';
            const message = formData.get('message') || '';
            
            // Save to local storage
            let contacts = JSON.parse(localStorage.getItem('contacts')) || [];
            contacts.push({
                name: name,
                email: email,
                topic: topic,
                message: message,
                timestamp: new Date().toISOString()
            });
            localStorage.setItem('contacts', JSON.stringify(contacts));
            
            console.log('Topic suggestion saved:', { name, email, topic });
            
            alert('Thank you. Your article topic suggestion has been saved.');
            contactForm.reset();
        });
    }
});

// DOWNLOAD FILTERING
function filterTemplates(type, event) {
    const templates = document.querySelectorAll('.template-card');
    const buttons = document.querySelectorAll('.filter-btn');
    
    // Update active button
    buttons.forEach(btn => btn.classList.remove('active'));
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Filter downloadable resources
    templates.forEach(template => {
        if (type === 'all' || template.dataset.type === type) {
            template.style.display = 'block';
            setTimeout(() => {
                template.style.opacity = '1';
            }, 10);
        } else {
            template.style.display = 'none';
        }
    });
}

// DOWNLOAD ARTICLE OR RESOURCE
function downloadTemplate(templateId) {
    console.log('Downloading resource:', templateId);
    
    // Log download
    let downloads = JSON.parse(localStorage.getItem('downloads')) || [];
    downloads.push({
        resourceId: templateId,
        timestamp: new Date().toISOString()
    });
    localStorage.setItem('downloads', JSON.stringify(downloads));
    
    alert(`Resource "${templateId}" selected.\n\nIn production, this will download the article PDF or checklist file.`);
}

// ANALYTICS TRACKING
function trackPageView() {
    const pageData = {
        page: window.location.pathname,
        timestamp: new Date().toISOString(),
        referrer: document.referrer,
        userAgent: navigator.userAgent
    };
    
    console.log('Page View:', pageData);
    
    // Store analytics data
    let pageViews = JSON.parse(localStorage.getItem('pageViews')) || [];
    pageViews.push(pageData);
    localStorage.setItem('pageViews', JSON.stringify(pageViews));
}

// DASHBOARD DATA RETRIEVAL
function getDashboardData() {
    return {
        subscribers: JSON.parse(localStorage.getItem('subscribers')) || [],
        topicSuggestions: JSON.parse(localStorage.getItem('contacts')) || [],
        downloads: JSON.parse(localStorage.getItem('downloads')) || [],
        pageViews: JSON.parse(localStorage.getItem('pageViews')) || []
    };
}

// DISPLAY DASHBOARD (for development/testing)
function showDashboard() {
    const data = getDashboardData();
    console.log('=== Qualizenz Dashboard ===');
    console.log('Total Email Subscribers:', data.subscribers.length);
    console.log('Total Topic Suggestions:', data.topicSuggestions.length);
    console.log('Total Resource Downloads:', data.downloads.length);
    console.log('Total Page Views:', data.pageViews.length);
    console.log('Subscribers:', data.subscribers);
    console.log('Topic Suggestions:', data.topicSuggestions);
    console.log('Downloads:', data.downloads);
    console.log('Page Views:', data.pageViews);
}

// SMOOTH SCROLL FOR ANCHOR LINKS
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// MOBILE MENU (if needed)
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
}

// Initialize on page load
window.addEventListener('load', function() {
    trackPageView();
    console.log('Qualizenz website loaded successfully');
    console.log('Type "showDashboard()" in console to see analytics');
});

// FORM VALIDATION
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// NOTIFICATION SYSTEM
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: ${type === 'success' ? '#10B981' : '#4F46E5'};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// EXPORT DATA FOR BACKUP
function exportData() {
    const data = getDashboardData();
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `qualizenz-data-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    console.log('Data exported successfully');
}
