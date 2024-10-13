document.addEventListener('DOMContentLoaded', function () {
    // Show modal when "Add to Cart" button is clicked
    document.querySelectorAll('.add-to-cart-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            const productId = button.getAttribute('data-product');
            const modal = document.getElementById('modal-' + productId);
            modal.classList.remove('hidden');
        });
    });

    // Close modal when "Cancel" button is clicked
    document.querySelectorAll('.modal-close').forEach(function (button) {
        button.addEventListener('click', function () {
            const modal = button.closest('.modal');
            modal.classList.add('hidden');
        });
    });

    // Handle the form submission for adding to cart
    document.querySelectorAll('form[id^="add-to-cart-form-"]').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submission

            const productId = form.id.split('-').pop(); // Extract product ID from form ID
            const formData = new FormData(form);

            // Create an object to hold measurement data
            const measurements = {
                shirt_length: formData.get('shirt_length'),
                body_chest: formData.get('body_chest'),
                back_shoulder: formData.get('back_shoulder'),
                sleeve: formData.get('sleeve'),
                round_sleeve: formData.get('round_sleeve'),
                round_mouth: formData.get('round_mouth'),
                trouser_length: formData.get('trouser_length'),
                thigh_laps: formData.get('thigh_laps'),
                knee: formData.get('knee'),
                trouser_mouth: formData.get('trouser_mouth'),
                half_length: formData.get('half_length'),
                full_length: formData.get('full_length'),
                cap_size: formData.get('cap_size'),
            };

            // Send the request to the server
            fetch('/update_item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    productId: productId,
                    action: 'add',
                    measurements: measurements
                })
            })
            .then(response => response.json())
            .then(data => {
                Swal.fire({
                    toast: true,
                    icon: 'success',
                    position: 'bottom-end',
                    title: 'Success!',
                    text: 'Product added to cart successfully',
                    showConfirmButton: false,
                    timer: 5000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.onmouseenter = Swal.stopTimer;
                        toast.onmouseleave = Swal.resumeTimer;
                    }
                });

                // Close the modal after the product is added to the cart
                const modal = form.closest('.modal');
                modal.classList.add('hidden');

                // Update the cart item count (you'll need to have an element with id="cart-items" in your page)
                document.getElementById('cart-items').textContent = data.cartItems;
            })
            .catch((error) => {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong! Please try again later.'
                });
            });
        });
    });
});


document.querySelectorAll('.delete-item-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        const productId = button.getAttribute('data-product');
        
        fetch('/delete_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,  // Ensure you have the CSRF token in your script
            },
            body: JSON.stringify({ 'productId': productId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                Swal.fire({
                    toast: true,
                    icon: 'success',
                    position: 'bottom-end',
                    title: 'Item removed',
                    showConfirmButton: false,
                    timer: 3000,
                });

                // Optionally refresh the cart or update the UI
                document.getElementById('cart-items').textContent = data.cartItems;

                // Optionally remove the item row from the UI
                
                const itemRow = document.getElementById('item-row-' + productId);
                if (itemRow) {
                    itemRow.remove();
                }
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch((error) => console.error('Error:', error));
    });
});
