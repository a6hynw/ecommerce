// CSRF Token Helper for Django AJAX Requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Mobile Menu Navigation Toggle
document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    const hamburgerIcon = document.getElementById('hamburgerIcon');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('mobile-active');
            if (navLinks.classList.contains('mobile-active')) {
                hamburgerIcon.setAttribute('name', 'close-outline');
            } else {
                hamburgerIcon.setAttribute('name', 'menu-outline');
            }
        });
    }
});

// Toast Alerts Generator
function showToast(message, type = 'success') {
    // Check if toast-container exists, else create one
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const iconName = type === 'success' ? 'checkmark-circle-outline' : (type === 'error' ? 'alert-circle-outline' : 'information-circle-outline');
    
    toast.innerHTML = `
        <div class="toast-content">
            <ion-icon name="${iconName}"></ion-icon>
            <span>${message}</span>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <ion-icon name="close-outline"></ion-icon>
        </button>
    `;

    container.appendChild(toast);

    // Auto removal
    setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

// Catalog Page Add to Cart (Quick add button)
function quickAddToCart(button, productId) {
    if (button.classList.contains('disabled')) return;
    
    // Pulse animation
    button.classList.add('pulse');
    setTimeout(() => button.classList.remove('pulse'), 500);

    const csrfToken = getCookie('csrftoken');
    if (!csrfToken) {
        showToast("Please log in to add items to your cart.", "error");
        setTimeout(() => { window.location.href = "/login/"; }, 1500);
        return;
    }

    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ product_id: productId, quantity: 1 })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Server error'); });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showToast(data.message, "success");
            // Update nav badge (guard: badge only exists when user is logged in)
            const badge = document.getElementById('globalCartBadge');
            if (badge) badge.innerText = data.cart_count;
        }
    })
    .catch(error => {
        showToast(error.message, "error");
    });
}

// Product Details Page Add to Cart
function detailAddToCart(productId) {
    const input = document.getElementById('detailQty');
    const quantity = input ? parseInt(input.value) : 1;
    const csrfToken = getCookie('csrftoken');

    if (!csrfToken) {
        showToast("Please log in to add items to your cart.", "error");
        setTimeout(() => { window.location.href = "/login/"; }, 1500);
        return;
    }

    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Server error'); });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showToast(data.message, "success");
            const badge = document.getElementById('globalCartBadge');
            if (badge) badge.innerText = data.cart_count;
        }
    })
    .catch(error => {
        showToast(error.message, "error");
    });
}

// Cart Page Actions
function updateCartItemQty(itemId, change, maxStock) {
    const qtyInput = document.getElementById(`cartItemQty-${itemId}`);
    let newQty = parseInt(qtyInput.value) + change;

    if (newQty < 1) {
        showToast("Quantity cannot be less than 1. Click remove to delete item.", "error");
        return;
    }

    if (newQty > maxStock) {
        showToast(`Cannot exceed warehouse stock. Only ${maxStock} available.`, "error");
        return;
    }

    const csrfToken = getCookie('csrftoken');
    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ item_id: parseInt(itemId), quantity: newQty })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Server error'); });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            qtyInput.value = newQty;
            document.getElementById(`cartItemSubtotal-${itemId}`).innerText = `$${data.item_subtotal.toFixed(2)}`;
            document.getElementById('summarySubtotal').innerText = `$${data.cart_total.toFixed(2)}`;
            const badge = document.getElementById('globalCartBadge');
            if (badge) badge.innerText = data.cart_count;
            recalculateCartSummary();
        }
    })
    .catch(error => {
        showToast(error.message, "error");
    });
}

function removeCartItem(itemId) {
    const csrfToken = getCookie('csrftoken');
    fetch('/cart/remove/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ item_id: parseInt(itemId) })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Server error'); });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const row = document.getElementById(`cartItemRow-${itemId}`);
            row.classList.add('fade-out');
            setTimeout(() => {
                row.remove();
                document.getElementById('summarySubtotal').innerText = `$${data.cart_total.toFixed(2)}`;
                const badge = document.getElementById('globalCartBadge');
                if (badge) badge.innerText = data.cart_count;
                
                if (data.cart_count === 0) {
                    document.getElementById('cartContent').classList.add('hidden');
                    document.getElementById('cartEmptyState').classList.remove('hidden');
                } else {
                    recalculateCartSummary();
                }
            }, 500);
            showToast("Product removed from cart", "info");
        }
    })
    .catch(error => {
        showToast(error.message, "error");
    });
}

function recalculateCartSummary() {
    const subtotalEl = document.getElementById('summarySubtotal');
    if (!subtotalEl) return;

    const subtotal = parseFloat(subtotalEl.innerText.replace('$', ''));
    const tax = subtotal * 0.1;
    const total = subtotal + tax;

    document.getElementById('summaryTax').innerText = `$${tax.toFixed(2)}`;
    document.getElementById('summaryTotal').innerText = `$${total.toFixed(2)}`;
}
