function scrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: "smooth" });
    }
}

function readStore(key, fallback) {
    try {
        return JSON.parse(localStorage.getItem(key)) || fallback;
    } catch {
        return fallback;
    }
}

function writeStore(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function saveRecord(key, record) {
    const rows = readStore(key, []);
    rows.push({
        id: `${key}-${Date.now()}`,
        createdAt: new Date().toISOString(),
        ...record
    });
    writeStore(key, rows);
    return rows;
}

document.addEventListener("DOMContentLoaded", function() {
    applySiteSettings();
    initSearch();
    initCatalogSearch();
    initNewsletterForm();
    initContactForm();
    initConsultingForm();
    trackPageView();
});

async function applySiteSettings() {
    let settings = readStore("site_settings", null);

    try {
        const response = await fetch("/api/site-settings", { cache: "no-store" });
        if (response.ok) {
            settings = await response.json();
            writeStore("site_settings", settings);
        }
    } catch {
        // Static hosting fallback uses browser-stored settings if available.
    }

    if (!settings) return;

    setText("headerBannerText", settings.header_banner_text);
    setText("announcementText", settings.announcement_text);
    setText("homeHeroTitle", settings.hero_title);
    setText("homeHeroIntro", settings.hero_intro);
    setText("footerDisclaimerText", settings.footer_disclaimer);

    const announcementBar = document.getElementById("announcementBar");
    if (announcementBar && settings.announcement_visible === false) {
        announcementBar.style.display = "none";
    }

    if (settings.sections) {
        Object.entries(settings.sections).forEach(([key, visible]) => {
            document.querySelectorAll(`[data-section-key="${key}"]`).forEach(section => {
                section.style.display = visible ? "" : "none";
            });
        });
    }
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element && value) {
        element.textContent = value;
    }
}

function initSearch() {
    const search = document.getElementById("siteSearch");
    if (!search) return;

    search.addEventListener("input", function() {
        const query = this.value.trim().toLowerCase();
        const cards = document.querySelectorAll(".searchable-content [data-search], .searchable-item[data-search]");

        cards.forEach(card => {
            const haystack = `${card.dataset.search || ""} ${card.innerText}`.toLowerCase();
            card.style.display = !query || haystack.includes(query) ? "" : "none";
        });
    });
}

function initCatalogSearch() {
    document.querySelectorAll(".catalog-search").forEach(input => {
        input.addEventListener("input", function() {
            const group = this.dataset.target;
            const query = this.value.trim().toLowerCase();
            const cards = document.querySelectorAll(`[data-group="${group}"]`);

            cards.forEach(card => {
                const haystack = `${card.dataset.search || ""} ${card.innerText}`.toLowerCase();
                card.style.display = !query || haystack.includes(query) ? "" : "none";
            });
        });
    });
}

function initNewsletterForm() {
    const newsletterForm = document.getElementById("newsletterForm");
    const newsletterMessage = document.getElementById("newsletterMessage");
    if (!newsletterForm) return;

    newsletterForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const email = document.getElementById("newsletterEmail").value.trim().toLowerCase();
        const subscribers = readStore("newsletter_subscribers", []);

        if (subscribers.some(row => row.email === email)) {
            newsletterMessage.innerHTML = messageBox("You are already subscribed.", "warning");
            return;
        }

        saveRecord("newsletter_subscribers", {
            email,
            source: "homepage_newsletter"
        });

        newsletterMessage.innerHTML = messageBox("Success. You are subscribed to Qualizenz updates.", "success");
        newsletterForm.reset();
    });
}

function initContactForm() {
    const contactForm = document.getElementById("contactForm");
    if (!contactForm) return;

    contactForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const formData = new FormData(contactForm);

        saveRecord("contact_messages", {
            name: formData.get("name"),
            email: formData.get("email"),
            topic: formData.get("topic"),
            message: formData.get("message")
        });

        alert("Thank you. Your message has been recorded.");
        contactForm.reset();
    });
}

function initConsultingForm() {
    const consultingForm = document.getElementById("consultingForm");
    if (!consultingForm) return;

    consultingForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const formData = new FormData(consultingForm);
        const file = formData.get("document");

        saveRecord("consulting_requests", {
            name: formData.get("name"),
            email: formData.get("email"),
            phone: formData.get("phone"),
            country: formData.get("country"),
            company: formData.get("company"),
            service: formData.get("service"),
            message: formData.get("message"),
            documentName: file && file.name ? file.name : ""
        });

        alert("Thank you. Your consulting inquiry has been recorded.");
        consultingForm.reset();
    });
}

function filterResources(group, type, event) {
    const cards = document.querySelectorAll(`[data-group="${group}"]`);
    const section = event && event.target ? event.target.closest("section") : null;
    const buttons = section ? section.querySelectorAll(".filter-btn") : [];

    buttons.forEach(btn => btn.classList.remove("active"));
    if (event && event.target) {
        event.target.classList.add("active");
    }

    cards.forEach(card => {
        card.style.display = type === "all" || card.dataset.type === type ? "" : "none";
    });
}

function filterTemplates(type, event) {
    filterResources("sop", type, event);
}

function downloadTemplate(resourceId) {
    const downloads = saveRecord("downloads", {
        resourceId,
        page: window.location.pathname
    });

    updateStatistic("download_count", downloads.length);
    alert(`Resource selected: ${resourceId}\n\nConnect payment/download delivery later for paid products. Free resources can be delivered by email automation or direct file link.`);
}

function previewResource(title) {
    alert(`${title}\n\nPreview page or sample PDF can be connected when the file is ready.`);
}

function trackPageView() {
    const pageViews = saveRecord("website_statistics", {
        type: "page_view",
        page: window.location.pathname || "/",
        referrer: document.referrer || "",
        userAgent: navigator.userAgent
    });

    updateStatistic("page_views", pageViews.length);
}

function updateStatistic(name, value) {
    const stats = readStore("qualizenz_stats", {});
    stats[name] = value;
    stats.updatedAt = new Date().toISOString();
    writeStore("qualizenz_stats", stats);
}

function getDashboardData() {
    return {
        articles: readStore("articles", seedArticles()),
        categories: readStore("categories", seedCategories()),
        sop_templates: readStore("sop_templates", []),
        validation_templates: readStore("validation_templates", []),
        free_resources: readStore("free_resources", []),
        consulting_requests: readStore("consulting_requests", []),
        contact_messages: readStore("contact_messages", []),
        newsletter_subscribers: readStore("newsletter_subscribers", []),
        downloads: readStore("downloads", []),
        website_statistics: readStore("website_statistics", []),
        stats: readStore("qualizenz_stats", {})
    };
}

function showDashboard() {
    console.log("Qualizenz Dashboard", getDashboardData());
}

function messageBox(text, type) {
    const colors = {
        success: ["#D1FAE5", "#065F46"],
        warning: ["#FEF3C7", "#92400E"],
        info: ["#DBEAFE", "#1E3A8A"]
    };
    const color = colors[type] || colors.info;
    return `<div style="background:${color[0]};color:${color[1]};padding:12px;border-radius:6px;margin-top:1rem;">${text}</div>`;
}

function toggleMobileMenu() {
    const categoryNav = document.querySelector(".category-nav");
    if (categoryNav) {
        categoryNav.classList.toggle("active");
    }
}

function seedCategories() {
    return [
        "GMP",
        "Quality Assurance",
        "Quality Control",
        "Data Integrity",
        "Documentation and GDP",
        "SOP Management",
        "CAPA",
        "Deviation",
        "Change Control",
        "Risk Management",
        "Validation",
        "Qualification",
        "Cleaning Validation",
        "Process Validation",
        "Computer System Validation",
        "Sterile Manufacturing",
        "BFS Technology",
        "Terminal Sterilization",
        "Environmental Monitoring",
        "HVAC",
        "Purified Water",
        "WFI",
        "Pure Steam",
        "Compressed Air",
        "Nitrogen System",
        "Warehouse",
        "Vendor Qualification",
        "Audit Readiness",
        "Regulatory Guidance",
        "Pharmaceutical Greenfield Projects"
    ];
}

function seedArticles() {
    return [
        {
            id: "article-001",
            title: "How to Write a GMP SOP",
            category: "Documentation and GDP",
            author: "Qualizenz Team",
            publishDate: "2026-06-04",
            status: "Published",
            summary: "A practical guide to SOP structure, approval, training and document control.",
            seoTitle: "How to Write a GMP SOP | Qualizenz",
            seoDescription: "Learn how to write GMP SOPs for pharmaceutical quality systems.",
            keywords: "GMP SOP templates, pharmaceutical QA documentation",
            views: 0
        },
        {
            id: "article-002",
            title: "IQ, OQ and PQ Explained",
            category: "Validation",
            author: "Qualizenz Team",
            publishDate: "2026-06-04",
            status: "Published",
            summary: "A simple explanation of installation, operational and performance qualification.",
            seoTitle: "IQ OQ PQ Explained | Qualizenz",
            seoDescription: "Understand pharmaceutical validation and qualification stages.",
            keywords: "pharmaceutical validation templates, IQ OQ PQ",
            views: 0
        }
    ];
}

function exportData() {
    const data = getDashboardData();
    const dataBlob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `qualizenz-data-${new Date().toISOString().split("T")[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}
