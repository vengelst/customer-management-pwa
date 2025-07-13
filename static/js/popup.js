// Popup system for customer and contact hover details
let popupTimeout;
let contactPopupTimeout;
let currentPopup = null;
let currentContactPopup = null;
let currentContactData = null;
let currentCustomerId = null;
let currentContactId = null;

function showCustomerPopup(element, customerId, event) {
    // Clear any existing timeout
    clearTimeout(popupTimeout);
    
    // If popup is already showing for this customer, don't reload
    if (currentCustomerId === customerId && currentPopup && currentPopup.style.display === 'block') {
        return;
    }
    
    // Hide any existing popup
    const popup = document.getElementById('customerPopup');
    if (popup.style.display === 'block') {
        popup.style.display = 'none';
    }
    
    // Check if we're on mobile (screen width < 768px)
    const isMobile = window.innerWidth < 768;
    
    if (isMobile) {
        // Center popup on mobile
        popup.style.left = '50%';
        popup.style.top = '50%';
        popup.style.transform = 'translate(-50%, -50%)';
        popup.style.position = 'fixed';
        popup.style.zIndex = '1050';
        popup.style.maxWidth = '90vw';
        popup.style.maxHeight = '80vh';
        popup.style.overflow = 'auto';
    } else {
        // Desktop positioning
        popup.style.position = 'absolute';
        popup.style.transform = 'none';
        popup.style.maxWidth = 'none';
        popup.style.maxHeight = 'none';
        popup.style.overflow = 'visible';
        
        // Get element position
        const rect = element.getBoundingClientRect();
        
        // Position popup to the right of the element
        popup.style.left = (rect.right + window.scrollX + 10) + 'px';
        popup.style.top = (rect.top + window.scrollY) + 'px';
        
        // Adjust position if popup goes off screen
        const popupRect = popup.getBoundingClientRect();
        if (popupRect.right > window.innerWidth) {
            popup.style.left = (rect.left + window.scrollX - popupRect.width - 10) + 'px';
        }
        if (popupRect.bottom > window.innerHeight) {
            popup.style.top = (rect.bottom + window.scrollY - popupRect.height) + 'px';
        }
    }
    
    popup.style.display = 'block';
    
    // Load customer data
    loadCustomerData(customerId);
    currentPopup = popup;
    currentCustomerId = customerId;
}

function hideCustomerPopup() {
    popupTimeout = setTimeout(() => {
        const popup = document.getElementById('customerPopup');
        if (popup) {
            popup.style.display = 'none';
            currentPopup = null;
            currentCustomerId = null;
        }
        hideContactPopup();
    }, 500);
}

function showContactPopup(element, contact, event) {
    // Clear any existing timeout
    clearTimeout(contactPopupTimeout);
    clearTimeout(popupTimeout);
    
    // If popup is already showing for this contact, don't reload
    if (currentContactId === contact.id && currentContactPopup && currentContactPopup.style.display === 'block') {
        return;
    }
    
    // Get the contact popup element
    const popup = document.getElementById('contactPopup');
    if (!popup) return;
    
    // Hide any existing contact popup
    if (popup.style.display === 'block') {
        popup.style.display = 'none';
    }
    
    // Check if we're on mobile (screen width < 768px)
    const isMobile = window.innerWidth < 768;
    
    if (isMobile) {
        // Center popup on mobile
        popup.style.left = '50%';
        popup.style.top = '50%';
        popup.style.transform = 'translate(-50%, -50%)';
        popup.style.position = 'fixed';
        popup.style.zIndex = '1060';
        popup.style.maxWidth = '90vw';
        popup.style.maxHeight = '80vh';
        popup.style.overflow = 'auto';
    } else {
        // Desktop positioning
        popup.style.position = 'absolute';
        popup.style.transform = 'none';
        popup.style.maxWidth = 'none';
        popup.style.maxHeight = 'none';
        popup.style.overflow = 'visible';
        popup.style.zIndex = '1060'; // Higher than customer popup
        
        // Get element position
        const rect = element.getBoundingClientRect();
        
        // Position popup to the right of the contact element
        popup.style.left = (rect.right + window.scrollX + 10) + 'px';
        popup.style.top = (rect.top + window.scrollY) + 'px';
        
        // Adjust position if popup goes off screen
        const popupRect = popup.getBoundingClientRect();
        if (popupRect.right > window.innerWidth) {
            popup.style.left = (rect.left + window.scrollX - popupRect.width - 10) + 'px';
        }
        if (popupRect.bottom > window.innerHeight) {
            popup.style.top = (rect.bottom + window.scrollY - popupRect.height) + 'px';
        }
    }
    
    popup.style.display = 'block';
    
    // Load contact data
    renderContactPopup(contact);
    currentContactPopup = popup;
    currentContactId = contact.id;
    
    // Stop event propagation to prevent customer popup from hiding
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
}

function hideContactPopup() {
    contactPopupTimeout = setTimeout(() => {
        const popup = document.getElementById('contactPopup');
        if (popup && !popup.matches(':hover')) {
            popup.style.display = 'none';
            currentContactPopup = null;
            currentContactId = null;
        }
    }, 300);
}

function loadCustomerData(customerId) {
    fetch(`/api/customer/${customerId}`)
        .then(response => response.json())
        .then(data => {
            currentContactData = data;
            renderCustomerPopup(data);
        })
        .catch(error => {
            console.error('Error loading customer data:', error);
        });
}

function renderCustomerPopup(data) {
    const popup = document.getElementById('customerPopup');
    const title = popup.querySelector('#popupTitle');
    const content = popup.querySelector('#popupContent');
    
    title.textContent = data.company_name;
    
    let html = `
        <div class="popup-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="info-item">
                        <strong>Branche:</strong> ${data.industry || 'Nicht angegeben'}
                    </div>
                    <div class="info-item">
                        <strong>Adresse:</strong> ${data.address || 'Nicht angegeben'}
                    </div>
                    <div class="info-item">
                        <strong>Stadt:</strong> ${data.city || 'Nicht angegeben'}
                    </div>
                    <div class="info-item">
                        <strong>PLZ:</strong> ${data.postal_code || 'Nicht angegeben'}
                    </div>
                    <div class="info-item">
                        <strong>Land:</strong> ${data.country || 'Nicht angegeben'}
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <strong>Website:</strong> ${data.website ? `<a href="javascript:void(0)" onclick="openWebsite('${data.website}')">${data.website}</a>` : 'Nicht angegeben'}
                    </div>
                    <div class="info-item">
                        <strong>Kategorie:</strong> <span class="badge bg-${getCategoryColor(data.category)}">${data.category}</span>
                    </div>
                    <div class="info-item">
                        <strong>Erstellt:</strong> ${formatDate(data.created_at)}
                    </div>
                    <div class="info-item">
                        <strong>Geändert:</strong> ${formatDate(data.updated_at)}
                    </div>
                </div>
            </div>
            
            ${data.notes ? `<div class="mt-3"><strong>Notizen:</strong><br>${data.notes}</div>` : ''}
        </div>
    `;
    
    // Add contacts section
    if (data.contacts && data.contacts.length > 0) {
        html += `
            <div class="popup-section">
                <h6>Kontakte (${data.contacts.length})</h6>
                <div class="contacts-list">
        `;
        
        data.contacts.forEach((contact, index) => {
            html += `
                <div class="contact-item contact-hover-item" 
                     data-contact-id="${contact.id}"
                     data-contact-index="${index}"
                     style="cursor: pointer; padding: 4px; margin: 2px 0; border-radius: 4px; transition: background-color 0.2s;"
                     onmouseover="this.style.backgroundColor='rgba(13, 110, 253, 0.1)'"
                     onmouseout="this.style.backgroundColor='transparent'">
                    <div class="contact-name">
                        <strong>${contact.full_name}</strong>
                        ${contact.is_primary ? '<span class="badge bg-primary ms-1">Haupt</span>' : ''}
                    </div>
                    <div class="contact-details">
                        ${contact.title ? `<div>${contact.title}</div>` : ''}
                        ${contact.email ? `<div><a href="mailto:${contact.email}">${contact.email}</a></div>` : ''}
                        ${contact.phone ? `<div><a href="tel:${contact.phone}">${contact.phone}</a></div>` : ''}
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    content.innerHTML = html;
    
    // Add event listeners to the newly created contact elements
    setTimeout(() => {
        const contactItems = content.querySelectorAll('.contact-hover-item');
        contactItems.forEach(item => {
            item.addEventListener('mouseenter', function(e) {
                clearTimeout(contactPopupTimeout);
                const contactIndex = parseInt(this.dataset.contactIndex);
                const contact = data.contacts[contactIndex];
                if (contact) {
                    showContactPopup(this, contact, e);
                }
            });
            item.addEventListener('mouseleave', function(e) {
                e.stopPropagation();
                hideContactPopup();
            });
        });
    }, 100);
}

function renderContactPopup(contact) {
    const popup = document.getElementById('contactPopup');
    const title = popup.querySelector('#contactPopupTitle');
    const content = popup.querySelector('#contactPopupContent');
    
    title.textContent = contact.full_name;
    
    let html = `
        <div class="popup-body">
            <div class="info-item">
                <strong>Position:</strong> ${contact.title || 'Nicht angegeben'}
            </div>
            <div class="info-item">
                <strong>Abteilung:</strong> ${contact.department || 'Nicht angegeben'}
            </div>
            <div class="info-item">
                <strong>E-Mail:</strong> ${contact.email ? `<a href="mailto:${contact.email}">${contact.email}</a>` : 'Nicht angegeben'}
            </div>
            <div class="info-item">
                <strong>Telefon:</strong> ${contact.phone ? `<a href="tel:${contact.phone}">${contact.phone}</a>` : 'Nicht angegeben'}
            </div>
            <div class="info-item">
                <strong>Mobil:</strong> ${contact.mobile ? `<a href="tel:${contact.mobile}">${contact.mobile}</a>` : 'Nicht angegeben'}
            </div>
            <div class="info-item">
                <strong>Status:</strong> ${contact.is_primary ? 'Hauptkontakt' : 'Kontakt'}
            </div>
            ${contact.notes ? `<div class="info-item"><strong>Notizen:</strong> ${contact.notes}</div>` : ''}
        </div>
    `;
    
    // Add appointments section
    if (contact.appointments && contact.appointments.length > 0) {
        html += `
            <div class="popup-section">
                <h6>Termine (${contact.appointments.length})</h6>
                <div class="appointments-list">
        `;
        
        contact.appointments.forEach(appointment => {
            const isFeature = new Date(appointment.appointment_date) > new Date();
            html += `
                <div class="appointment-item ${isFeature ? 'future' : 'past'}">
                    <div class="appointment-title">${appointment.title}</div>
                    <div class="appointment-date">${formatDate(appointment.appointment_date)}</div>
                    <div class="appointment-details">
                        ${appointment.duration_minutes} Min • ${appointment.location || 'Ort nicht angegeben'}
                    </div>
                    ${appointment.description ? `<div class="appointment-description">${appointment.description}</div>` : ''}
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    content.innerHTML = html;
}

function getCategoryColor(category) {
    switch(category) {
        case 'neu': return 'secondary';
        case 'Interesse': return 'info';
        case 'Bedarf': return 'success';
        case 'kein Bedarf': return 'danger';
        default: return 'secondary';
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('de-DE', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Button action functions
function editCustomer() {
    if (currentCustomerId) {
        window.open(`/customer/${currentCustomerId}/edit`, '_blank');
    }
}

function printCustomer() {
    if (currentCustomerId) {
        window.open(`/customer/${currentCustomerId}/print-edit`, '_blank');
    }
}

function documentsCustomer() {
    if (currentCustomerId) {
        window.open(`/customer/${currentCustomerId}/documents`, '_blank');
    }
}

function editContact() {
    if (currentContactId) {
        window.open(`/contact/${currentContactId}/edit`, '_blank');
    }
}

function printContact() {
    if (currentContactId) {
        const contact = getCurrentContactData();
        if (contact) {
            printContactData(contact);
        }
    }
}

function getCurrentContactData() {
    if (!currentContactData || !currentContactData.contacts) {
        return null;
    }
    return currentContactData.contacts.find(c => c.id === currentContactId);
}

function printContactData(contact) {
    const printWindow = window.open('', '_blank');
    const customer = currentContactData;
    
    let appointmentsHtml = '';
    if (contact.appointments && contact.appointments.length > 0) {
        appointmentsHtml = '<div class="section"><h3>Termine (' + contact.appointments.length + ')</h3>';
        
        contact.appointments.forEach(appointment => {
            const appointmentDate = new Date(appointment.appointment_date);
            const isFuture = appointmentDate > new Date();
            const dateStr = appointmentDate.toLocaleDateString('de-DE', { 
                year: 'numeric', 
                month: '2-digit', 
                day: '2-digit', 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            
            appointmentsHtml += '<div class="appointment ' + (isFuture ? 'future' : 'past') + '">';
            appointmentsHtml += '<div style="font-weight: bold;">' + appointment.title + '</div>';
            appointmentsHtml += '<div>' + dateStr + '</div>';
            appointmentsHtml += '<div>' + appointment.duration_minutes + ' Minuten • ' + (appointment.location || 'Ort nicht angegeben') + '</div>';
            
            if (appointment.description) {
                appointmentsHtml += '<div>Beschreibung: ' + appointment.description + '</div>';
            }
            if (appointment.notes) {
                appointmentsHtml += '<div>Notizen: ' + appointment.notes + '</div>';
            }
            appointmentsHtml += '</div>';
        });
        
        appointmentsHtml += '</div>';
    }
    
    const html = '<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><title>Kontakt - ' + contact.full_name + '</title><style>body { font-family: Arial, sans-serif; margin: 20px; }.header { border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }.section { margin-bottom: 20px; }.section h3 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 5px; }.info-row { margin-bottom: 8px; }.label { font-weight: bold; }.appointment { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 4px; }.future { background-color: #e3f2fd; }.past { background-color: #f5f5f5; }</style></head><body><div class="header"><h1>Kontakt-Details</h1><p>Erstellt am: ' + new Date().toLocaleDateString('de-DE') + '</p></div><div class="section"><h2>' + contact.full_name + '</h2><div class="info-row"><span class="label">Firma:</span> ' + customer.company_name + '</div>' + (contact.title ? '<div class="info-row"><span class="label">Position:</span> ' + contact.title + '</div>' : '') + (contact.department ? '<div class="info-row"><span class="label">Abteilung:</span> ' + contact.department + '</div>' : '') + (contact.email ? '<div class="info-row"><span class="label">E-Mail:</span> ' + contact.email + '</div>' : '') + (contact.phone ? '<div class="info-row"><span class="label">Telefon:</span> ' + contact.phone + '</div>' : '') + (contact.mobile ? '<div class="info-row"><span class="label">Mobil:</span> ' + contact.mobile + '</div>' : '') + (contact.is_primary ? '<div class="info-row"><span class="label">Status:</span> Hauptkontakt</div>' : '') + (contact.notes ? '<div class="info-row"><span class="label">Notizen:</span> ' + contact.notes + '</div>' : '') + '</div>' + appointmentsHtml + '<script>window.onload = function() { window.print(); };</script></body></html>';
    
    printWindow.document.write(html);
    printWindow.document.close();
}

// Initialize popup event listeners
document.addEventListener('DOMContentLoaded', function() {
    const customerPopup = document.getElementById('customerPopup');
    const contactPopup = document.getElementById('contactPopup');
    
    if (customerPopup) {
        customerPopup.addEventListener('mouseenter', function() {
            clearTimeout(popupTimeout);
        });
        customerPopup.addEventListener('mouseleave', function() {
            hideCustomerPopup();
        });
    }
    
    if (contactPopup) {
        contactPopup.addEventListener('mouseenter', function(e) {
            clearTimeout(contactPopupTimeout);
            clearTimeout(popupTimeout);
            e.stopPropagation();
        });
        contactPopup.addEventListener('mouseleave', function(e) {
            hideContactPopup();
            e.stopPropagation();
        });
        // Prevent customer popup from closing when hovering over contact popup
        contactPopup.addEventListener('mouseover', function(e) {
            e.stopPropagation();
            clearTimeout(popupTimeout);
            clearTimeout(contactPopupTimeout);
        });
        // Prevent all mouse events from propagating out of contact popup
        contactPopup.addEventListener('mousemove', function(e) {
            e.stopPropagation();
        });
        contactPopup.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // Add hover event listeners to all customer name elements
    const customerNameElements = document.querySelectorAll('.customer-name-wrapper');
    customerNameElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            clearTimeout(popupTimeout);
        });
    });
    
    // Add hover event listeners to existing contact elements
    const contactElements = document.querySelectorAll('.contact-hover-item');
    contactElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            clearTimeout(contactPopupTimeout);
        });
    });
});