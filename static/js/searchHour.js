document.addEventListener('DOMContentLoaded', function() {
    const imagePreviewButtons = document.querySelectorAll('.image-preview-button');
    
    imagePreviewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const imageUrl = this.getAttribute('data-image-url');
            const signId = this.getAttribute('data-sign-id');
            
            if (imageUrl) {
                const modal = document.createElement('div');
                modal.classList.add('image-modal');
                modal.innerHTML = `
                    <div class="modal-content">
                        <span class="close">&times;</span>
                        <img class="image-preview" src="${imageUrl}" alt="Image Preview" />
                    </div>
                `;

                document.body.appendChild(modal);

                modal.querySelector('.close').addEventListener('click', function() {
                    modal.style.display = 'none';
                    modal.remove();
                });
                
                modal.style.display = 'block';
            }
        });
    });
});