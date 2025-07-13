// Customer Management Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Search functionality
    var searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            // Optional: Auto-submit search after typing stops
            // document.querySelector('form').submit();
        }, 300));
    }

    // Phone number formatting
    var phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            // Remove all non-numeric characters except +
            var value = e.target.value.replace(/[^\d+]/g, '');
            e.target.value = value;
        });
    });

    // Website URL validation
    var urlInputs = document.querySelectorAll('input[type="url"]');
    urlInputs.forEach(function(input) {
        input.addEventListener('blur', function(e) {
            var value = e.target.value.trim();
            if (value && !value.match(/^https?:\/\//)) {
                e.target.value = 'https://' + value;
            }
        });
    });

    // Table row click handlers
    var clickableRows = document.querySelectorAll('.clickable');
    clickableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            var link = row.querySelector('a');
            if (link) {
                window.location.href = link.href;
            }
        });
    });

    // Print functionality
    var printButtons = document.querySelectorAll('[data-print]');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Dynamic date/time defaults
    var dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        if (!input.value) {
            var today = new Date();
            input.value = today.toISOString().split('T')[0];
        }
    });

    var timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(function(input) {
        if (!input.value) {
            var now = new Date();
            var hours = String(now.getHours()).padStart(2, '0');
            var minutes = String(now.getMinutes()).padStart(2, '0');
            input.value = hours + ':' + minutes;
        }
    });

    // Confirmation dialogs
    var deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            var message = button.getAttribute('data-confirm') || 'Sind Sie sicher?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Loading states for forms
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Wird gespeichert...';
            }
        });
    });

    // Character counter for textareas
    var textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        var maxLength = textarea.getAttribute('maxlength');
        var counter = document.createElement('small');
        counter.className = 'text-muted';
        counter.textContent = '0/' + maxLength;
        textarea.parentNode.insertBefore(counter, textarea.nextSibling);

        textarea.addEventListener('input', function() {
            var currentLength = textarea.value.length;
            counter.textContent = currentLength + '/' + maxLength;
            
            if (currentLength > maxLength * 0.9) {
                counter.className = 'text-warning';
            } else if (currentLength === maxLength) {
                counter.className = 'text-danger';
            } else {
                counter.className = 'text-muted';
            }
        });
    });

    // Auto-save functionality (optional)
    var autoSaveForms = document.querySelectorAll('[data-auto-save]');
    autoSaveForms.forEach(function(form) {
        var inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(function(input) {
            input.addEventListener('change', debounce(function() {
                saveFormData(form);
            }, 1000));
        });
    });

    // Back button functionality
    var backButtons = document.querySelectorAll('[data-back]');
    backButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.history.back();
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+S to save forms
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            var activeForm = document.querySelector('form');
            if (activeForm) {
                activeForm.submit();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            var openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(function(modal) {
                var bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });

    // Theme toggle (if needed)
    var themeToggle = document.querySelector('[data-theme-toggle]');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            var currentTheme = document.documentElement.getAttribute('data-bs-theme');
            var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // Load saved theme
    var savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    }
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function saveFormData(form) {
    var formData = new FormData(form);
    var data = {};
    for (var [key, value] of formData.entries()) {
        data[key] = value;
    }
    localStorage.setItem('formData_' + form.id, JSON.stringify(data));
}

function loadFormData(form) {
    var savedData = localStorage.getItem('formData_' + form.id);
    if (savedData) {
        var data = JSON.parse(savedData);
        for (var key in data) {
            var input = form.querySelector('[name="' + key + '"]');
            if (input) {
                input.value = data[key];
            }
        }
    }
}

function clearFormData(form) {
    localStorage.removeItem('formData_' + form.id);
}

// Format phone numbers
function formatPhoneNumber(phoneNumber) {
    var cleaned = phoneNumber.replace(/\D/g, '');
    var match = cleaned.match(/^(\d{2})(\d{3})(\d{6})$/);
    if (match) {
        return '+' + match[1] + ' ' + match[2] + ' ' + match[3];
    }
    return phoneNumber;
}

// Validate email
function validateEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Show success message
function showSuccessMessage(message) {
    var alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show';
    alert.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
    
    var container = document.querySelector('.container');
    container.insertBefore(alert, container.firstChild);
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    }, 3000);
}

// Show error message
function showErrorMessage(message) {
    var alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
    
    var container = document.querySelector('.container');
    container.insertBefore(alert, container.firstChild);
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    }, 5000);
}

// Smart website opening function - make it global
window.openWebsite = function(url) {
    // Normalize URL - ensure it has a protocol
    let targetUrl = url;
    
    // If URL doesn't start with http:// or https://, add https:// first
    if (!targetUrl.match(/^https?:\/\//)) {
        targetUrl = 'https://' + targetUrl;
    }
    
    // Try to open with HTTPS first
    const httpsWindow = window.open(targetUrl, '_blank');
    
    // If popup blocking is detected, offer alternative
    if (!httpsWindow || httpsWindow.closed || typeof httpsWindow.closed === 'undefined') {
        // Try HTTP version immediately if HTTPS failed
        if (targetUrl.startsWith('https://')) {
            const httpUrl = targetUrl.replace('https://', 'http://');
            const httpWindow = window.open(httpUrl, '_blank');
            
            if (!httpWindow || httpWindow.closed || typeof httpWindow.closed === 'undefined') {
                // If both fail, show options
                if (confirm('Die Website konnte nicht automatisch geöffnet werden. Möchten Sie es mit HTTP (unsicher) versuchen?\n\nKlicken Sie "OK" für HTTP oder "Abbrechen" um die URL zu kopieren.')) {
                    // Force HTTP
                    window.location.href = httpUrl;
                } else {
                    // Copy URL to clipboard if possible
                    if (navigator.clipboard) {
                        navigator.clipboard.writeText(targetUrl).then(() => {
                            alert('URL wurde in die Zwischenablage kopiert: ' + targetUrl);
                        }).catch(() => {
                            alert('Bitte öffnen Sie diese URL manuell: ' + targetUrl);
                        });
                    } else {
                        alert('Bitte öffnen Sie diese URL manuell: ' + targetUrl);
                    }
                }
            }
        } else {
            alert('Die Website konnte nicht geöffnet werden. URL: ' + targetUrl);
        }
    }
};

// Export functions for global use
window.CustomerManagement = {
    showSuccessMessage: showSuccessMessage,
    showErrorMessage: showErrorMessage,
    formatPhoneNumber: formatPhoneNumber,
    validateEmail: validateEmail,
    debounce: debounce,
    openWebsite: window.openWebsite
};
