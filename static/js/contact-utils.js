// Contact Form and Notification System
// Reusable JavaScript utilities for forms and notifications

class NotificationSystem {
    constructor() {
        this.notificationContainer = null;
        this.init();
    }

    init() {
        // Create notification container if it doesn't exist
        if (!document.getElementById('notification-container')) {
            this.notificationContainer = document.createElement('div');
            this.notificationContainer.id = 'notification-container';
            this.notificationContainer.className = 'fixed top-4 right-4 z-50 space-y-2';
            document.body.appendChild(this.notificationContainer);
        } else {
            this.notificationContainer = document.getElementById('notification-container');
        }
    }

    show(type, message, duration = 5000) {
        // Remove existing notifications of the same type
        const existingNotifications = this.notificationContainer.querySelectorAll(`.notification-${type}`);
        existingNotifications.forEach(n => this.remove(n));

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} p-4 rounded-lg shadow-lg max-w-md transform transition-all duration-300 translate-x-full`;
        
        if (type === 'success') {
            notification.classList.add('bg-green-500', 'text-white');
            notification.innerHTML = `
                <div class="flex items-center">
                    <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    <span class="flex-grow">${message}</span>
                    <button class="ml-4 text-white hover:text-gray-200 flex-shrink-0" onclick="notificationSystem.remove(this.parentElement.parentElement)">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                    </button>
                </div>
            `;
        } else if (type === 'error') {
            notification.classList.add('bg-red-500', 'text-white');
            notification.innerHTML = `
                <div class="flex items-center">
                    <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                    </svg>
                    <span class="flex-grow">${message}</span>
                    <button class="ml-4 text-white hover:text-gray-200 flex-shrink-0" onclick="notificationSystem.remove(this.parentElement.parentElement)">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                    </button>
                </div>
            `;
        } else if (type === 'info') {
            notification.classList.add('bg-blue-500', 'text-white');
            notification.innerHTML = `
                <div class="flex items-center">
                    <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                    </svg>
                    <span class="flex-grow">${message}</span>
                    <button class="ml-4 text-white hover:text-gray-200 flex-shrink-0" onclick="notificationSystem.remove(this.parentElement.parentElement)">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                    </button>
                </div>
            `;
        }

        // Add to container
        this.notificationContainer.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove after duration
        if (duration > 0) {
            setTimeout(() => {
                this.remove(notification);
            }, duration);
        }

        return notification;
    }

    remove(notification) {
        if (notification && notification.parentElement) {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.parentElement.removeChild(notification);
                }
            }, 300);
        }
    }

    success(message, duration = 5000) {
        return this.show('success', message, duration);
    }

    error(message, duration = 7000) {
        return this.show('error', message, duration);
    }

    info(message, duration = 4000) {
        return this.show('info', message, duration);
    }
}

class ContactFormHandler {
    constructor(formId, options = {}) {
        this.formId = formId;
        this.options = {
            endpoint: '/contact',
            loadingText: 'Sending...',
            successMessage: 'Thank you for your message! We\'ll get back to you within 24 hours.',
            errorMessage: 'Sorry, there was an error sending your message. Please try again or contact us directly.',
            resetOnSuccess: true,
            ...options
        };
        this.form = null;
        this.submitButton = null;
        this.originalButtonText = '';
        this.init();
    }

    init() {
        this.form = document.getElementById(this.formId);
        if (!this.form) {
            console.error(`Contact form with ID "${this.formId}" not found`);
            return;
        }

        this.submitButton = this.form.querySelector('button[type="submit"]');
        if (this.submitButton) {
            this.originalButtonText = this.submitButton.textContent;
        }

        this.form.addEventListener('submit', this.handleSubmit.bind(this));
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.submitButton) return;

        // Set loading state
        this.setLoadingState(true);
        
        try {
            const formData = this.extractFormData();
            
            const response = await fetch(this.options.endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                notificationSystem.success(result.message || this.options.successMessage);
                if (this.options.resetOnSuccess) {
                    this.form.reset();
                }
            } else {
                notificationSystem.error(result.message || this.options.errorMessage);
            }
            
        } catch (error) {
            console.error('Error submitting form:', error);
            notificationSystem.error(this.options.errorMessage);
        } finally {
            this.setLoadingState(false);
        }
    }

    extractFormData() {
        const formData = new FormData(this.form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value || null;
        }
        
        return data;
    }

    setLoadingState(isLoading) {
        if (!this.submitButton) return;

        if (isLoading) {
            this.submitButton.disabled = true;
            this.submitButton.textContent = this.options.loadingText;
            this.submitButton.classList.add('opacity-75');
        } else {
            this.submitButton.disabled = false;
            this.submitButton.textContent = this.originalButtonText;
            this.submitButton.classList.remove('opacity-75');
        }
    }
}

// Initialize global notification system
let notificationSystem;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    notificationSystem = new NotificationSystem();
    
    // Auto-initialize contact forms with the default ID
    if (document.getElementById('contactForm')) {
        new ContactFormHandler('contactForm');
    }
});

// Global utility functions for backwards compatibility
function showNotification(type, message, duration = 5000) {
    if (notificationSystem) {
        return notificationSystem.show(type, message, duration);
    }
}

// Animation utilities
class AnimationUtils {
    static fadeInOnScroll(selector, options = {}) {
        const defaultOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observerOptions = { ...defaultOptions, ...options };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, observerOptions);

        document.querySelectorAll(selector).forEach(element => {
            observer.observe(element);
        });
    }
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        NotificationSystem,
        ContactFormHandler,
        AnimationUtils,
        showNotification
    };
}