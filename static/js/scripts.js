document.addEventListener('DOMContentLoaded', function () {
    // Update cart count in navbar
    function updateCartCount() {
        fetch('/api/cart/count')
            .then(response => response.json())
            .then(data => {
                document.getElementById('cart-count').textContent = data.count;
            })
            .catch(error => console.error('Error:', error));
    }

    // Initialize cart count
    updateCartCount();

    // Quantity input controls
    document.querySelectorAll('.quantity-control').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const input = this.parentNode.querySelector('.quantity-input');
            let value = parseInt(input.value);

            if (this.classList.contains('quantity-up')) {
                value = isNaN(value) ? 1 : value + 1;
            } else if (this.classList.contains('quantity-down') && value > 1) {
                value = value - 1;
            }

            input.value = value;
        });
    });

    // Product search functionality
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            const query = this.querySelector('input[name="q"]').value.trim();
            if (!query) {
                e.preventDefault();
            }
        });
    }

    // Flash messages auto-hide
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // Image zoom for product page
    const productImage = document.querySelector('.product-img');
    if (productImage) {
        productImage.addEventListener('click', function () {
            this.classList.toggle('zoomed');
        });
    }

    // Form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function (e) {
            let valid = true;
            this.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    valid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                const firstInvalid = this.querySelector('.is-invalid');
                firstInvalid.focus();
            }
        });
    });
});

// API call to update cart
function updateCart(productId, quantity) {
    fetch('/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCartCount();
                if (data.message) {
                    showFlashMessage(data.message, 'success');
                }
            } else {
                showFlashMessage(data.message || 'Error updating cart', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showFlashMessage('Network error', 'danger');
        });
}

// Show flash message
function showFlashMessage(message, type) {
    const flashContainer = document.createElement('div');
    flashContainer.className = `alert alert-${type} alert-dismissible fade show`;
    flashContainer.role = 'alert';
    flashContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const mainContainer = document.querySelector('.container') || document.body;
    mainContainer.prepend(flashContainer);

    setTimeout(() => {
        flashContainer.style.opacity = '0';
        setTimeout(() => flashContainer.remove(), 500);
    }, 5000);
}