// LuxCart Custom JS Functions

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Initialize & Auto-Dismiss Toast Notifications
    const toastElements = document.querySelectorAll('.toast');
    if (toastElements.length > 0) {
        toastElements.forEach(function(toastEl) {
            // Set delay to 4000ms (4 seconds)
            setTimeout(function() {
                // Use Bootstrap's fade class to fade out cleanly
                toastEl.classList.remove('show');
                toastEl.classList.add('hide');
                // Remove from DOM after transition completes
                setTimeout(function() {
                    toastEl.remove();
                }, 500);
            }, 4000);
        });
    }

    // 2. Bootstrap 5 Form Custom Validation
    const validationForms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(validationForms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // 3. Smooth Scroll to Anchors (e.g. Shop Now button to products list)
    const smoothLinks = document.querySelectorAll('a[href^="#"]');
    smoothLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                const headerOffset = 100;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // 4. Shrink Navbar on Scroll
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.padding = '0.6rem 0';
                navbar.style.boxShadow = '0 10px 15px -3px rgba(0,0,0,0.08)';
            } else {
                navbar.style.padding = '1rem 0';
                navbar.style.boxShadow = '0 2px 4px rgba(0,0,0,0.02)';
            }
        });
    }
});
