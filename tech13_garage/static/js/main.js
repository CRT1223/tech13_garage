// TECH13 Garage Main JavaScript

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Smooth scrolling for anchor links
    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault();
        var target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    // Add to cart functionality
    window.addToCart = function(itemId, itemType) {
        var quantity = 1;
        
        // If we're on product detail page, get quantity from input
        if (itemType === 'product' && $('#quantity').length) {
            quantity = parseInt($('#quantity').val()) || 1;
        }

        $.ajax({
            url: '/add_to_cart',
            method: 'POST',
            data: {
                [itemType + '_id']: itemId,
                quantity: quantity
            },
            beforeSend: function() {
                // Show loading state
                $('button[onclick*="addToCart"]').prop('disabled', true).html('<span class="loading"></span> Adding...');
            },
            success: function(response) {
                if (response.success) {
                    showNotification(response.message, 'success');
                    updateCartCount();
                } else {
                    showNotification(response.message, 'error');
                }
            },
            error: function() {
                showNotification('Error adding item to cart', 'error');
            },
            complete: function() {
                // Reset button state
                $('button[onclick*="addToCart"]').prop('disabled', false).html('<i class="fas fa-cart-plus"></i>');
            }
        });
    };

    // Update cart quantity
    window.updateQuantity = function(cartId, change) {
        var quantityInput = $('#qty-' + cartId);
        var currentValue = parseInt(quantityInput.val());
        var newValue = currentValue + change;
        
        if (newValue >= 1) {
            quantityInput.val(newValue);
            
            $.ajax({
                url: '/update_cart_quantity',
                method: 'POST',
                data: {
                    cart_id: cartId,
                    quantity: newValue
                },
                success: function(response) {
                    if (response.success) {
                        location.reload(); // Refresh to show updated totals
                    } else {
                        showNotification('Error updating quantity', 'error');
                    }
                },
                error: function() {
                    showNotification('Error updating quantity', 'error');
                }
            });
        }
    };

    // Show notification
    function showNotification(message, type) {
        var alertClass = type === 'error' ? 'alert-danger' : 'alert-success';
        var icon = type === 'error' ? 'fas fa-exclamation-circle' : 'fas fa-check-circle';
        
        var alert = $('<div class="alert ' + alertClass + ' alert-dismissible fade show position-fixed" style="top: 100px; right: 20px; z-index: 9999;">' +
            '<i class="' + icon + ' me-2"></i>' + message +
            '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
            '</div>');
        
        $('body').append(alert);
        
        // Auto remove after 3 seconds
        setTimeout(function() {
            alert.alert('close');
        }, 3000);
    }

    // Update cart count (if cart count element exists)
    function updateCartCount() {
        // This would typically make an AJAX call to get the current cart count
        // For now, we'll just show a visual feedback
        $('.cart-count').addClass('pulse');
        setTimeout(function() {
            $('.cart-count').removeClass('pulse');
        }, 1000);
    }

    // Form validation
    $('form').on('submit', function(e) {
        var form = $(this);
        var isValid = true;
        
        // Check required fields
        form.find('[required]').each(function() {
            if (!$(this).val()) {
                $(this).addClass('is-invalid');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        // Email validation
        form.find('input[type="email"]').each(function() {
            var email = $(this).val();
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (email && !emailRegex.test(email)) {
                $(this).addClass('is-invalid');
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('Please fill in all required fields correctly', 'error');
        }
    });

    // Remove validation classes on input
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid');
    });

    // Search functionality
    $('#search-form').on('submit', function(e) {
        var searchTerm = $('#search-input').val().trim();
        if (!searchTerm) {
            e.preventDefault();
            showNotification('Please enter a search term', 'error');
        }
    });

    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Add animation classes on scroll
    $(window).on('scroll', function() {
        $('.fade-in').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            
            if (elementBottom > viewportTop && elementTop < viewportBottom) {
                $(this).addClass('animated');
            }
        });
    });

    // Mobile menu close on link click
    $('.navbar-nav .nav-link').on('click', function() {
        if ($(window).width() < 992) {
            $('.navbar-collapse').collapse('hide');
        }
    });

    // Back to top button
    var backToTop = $('<button class="btn btn-primary position-fixed" style="bottom: 20px; right: 20px; z-index: 1000; display: none; border-radius: 50%; width: 50px; height: 50px;"><i class="fas fa-arrow-up"></i></button>');
    $('body').append(backToTop);
    
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 300) {
            backToTop.fadeIn();
        } else {
            backToTop.fadeOut();
        }
    });
    
    backToTop.on('click', function() {
        $('html, body').animate({scrollTop: 0}, 800);
    });
});

// Utility functions
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toFixed(2);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Add pulse animation class
$('<style>.pulse { animation: pulse 0.5s ease-in-out; } @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }</style>').appendTo('head');
