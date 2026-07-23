// ========== CART MANAGEMENT ==========

// Get or create cart ID
function getCartId() {
    let cartId = localStorage.getItem('cartId');
    if (!cartId) {
        fetch('/api/carts/', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                localStorage.setItem('cartId', data.id);
                updateCartCount(data.id);
            })
            .catch(err => console.error('Error creating cart:', err));
        return null;
    }
    return cartId;
}

// Update cart count in navbar
function updateCartCount(cartId) {
    fetch(`/api/carts/${cartId}/`)
        .then(res => res.json())
        .then(data => {
            const badge = document.querySelector('.cart-count');
            if (badge) {
                const count = data.item_count || 0;
                badge.textContent = count;
                badge.style.display = count > 0 ? 'inline-block' : 'none';
            }
        })
        .catch(err => console.error('Error updating cart count:', err));
}

// Add item to cart
function addToCart(productId, quantity = 1) {
    const cartId = localStorage.getItem('cartId');
    if (!cartId) {
        fetch('/api/carts/', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                localStorage.setItem('cartId', data.id);
                return addToCart(productId, quantity);
            })
            .catch(err => console.error('Error creating cart:', err));
        return;
    }

    fetch(`/api/carts/${cartId}/add_item/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: parseInt(productId), quantity: quantity })
    })
    .then(res => res.json())
    .then(() => {
        updateCartCount(cartId);
        showToast('Added to cart successfully!', 'success');
    })
    .catch(err => console.error('Error adding to cart:', err));
}

// Remove item from cart
function removeFromCart(itemId) {
    const cartId = localStorage.getItem('cartId');
    if (!cartId) return;

    fetch(`/api/carts/${cartId}/items/${itemId}/`, {
        method: 'DELETE'
    })
    .then(() => {
        updateCartCount(cartId);
        showToast('Item removed from cart', 'info');
        if (window.location.pathname.includes('/cart/')) {
            location.reload();
        }
    })
    .catch(err => console.error('Error removing item:', err));
}

// Update cart item quantity
function updateCartItem(itemId, quantity) {
    const cartId = localStorage.getItem('cartId');
    if (!cartId) return;

    fetch(`/api/carts/${cartId}/items/${itemId}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity: parseInt(quantity) })
    })
    .then(res => res.json())
    .then(() => {
        updateCartCount(cartId);
        if (window.location.pathname.includes('/cart/')) {
            location.reload();
        }
    })
    .catch(err => console.error('Error updating item:', err));
}

// ========== TOAST NOTIFICATIONS ==========

function showToast(message, type = 'success') {
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        info: '#17a2b8',
        warning: '#ffc107'
    };
    
    const toast = document.createElement('div');
    toast.className = 'position-fixed bottom-0 end-0 p-3';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="p-3 rounded shadow" style="background-color: ${colors[type] || '#28a745'}; color: white; max-width: 350px;">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'} me-2"></i>${message}
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// ========== GUEST CHECKOUT MODAL ==========

function showGuestCheckoutModal(redirectUrl) {
    const modal = new bootstrap.Modal(document.getElementById('guestCheckoutModal'));
    const guestBtn = document.getElementById('guestCheckoutBtn');
    if (guestBtn) {
        guestBtn.href = redirectUrl || '/checkout/';
    }
    modal.show();
}

// ========== INITIALIZE ==========

document.addEventListener('DOMContentLoaded', function() {
    // Load cart count on page load
    const cartId = localStorage.getItem('cartId');
    if (cartId) {
        updateCartCount(cartId);
    }

    // Add to cart buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const quantity = parseInt(document.getElementById('quantity')?.value || 1);
            addToCart(productId, quantity);
        });
    });

    // Checkout button - show guest modal
    const checkoutBtn = document.getElementById('checkoutBtn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const token = localStorage.getItem('token');
            if (token) {
                window.location.href = '/checkout/';
            } else {
                showGuestCheckoutModal('/checkout/');
            }
        });
    }
});