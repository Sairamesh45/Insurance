// Handle form submission and display insurance prediction
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded successfully');
    
    const form = document.querySelector('form');
    console.log('Form found:', form);
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            console.log('Form submission intercepted');
            e.preventDefault(); // Prevent default form submission
            e.stopPropagation(); // Stop event bubbling
            
            // Get form data
            const formData = new FormData(form);
            console.log('Form data collected:', formData);
            
            // Show loading message
            showMessage('Calculating your insurance prediction...', 'loading');
            
            try {
                // Send POST request to backend
                const response = await fetch('http://localhost:8000/submit/', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                console.log('Response received:', result);
                
                if (result.error) {
                    showMessage(`Error: ${result.error}`, 'error');
                } else if (result.prediction !== undefined) {
                    showMessage(`Your estimated insurance charge: $${result.prediction}`, 'success');
                } else {
                    // Handle case where prediction might be in a different format
                    console.log('Full result object:', result);
                    showMessage(`Your estimated insurance charge: $${JSON.stringify(result)}`, 'success');
                }
                
            } catch (error) {
                console.error('Network error:', error);
                showMessage(`Network error: ${error.message}`, 'error');
            }
            
            return false; // Extra prevention of form submission
        });
    } else {
        console.error('Form not found!');
    }
});

// Function to display messages
function showMessage(message, type) {
    // Remove existing message if any
    const existingMessage = document.querySelector('.prediction-result');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create new message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `prediction-result ${type}`;
    messageDiv.innerHTML = message;
    
    // Add styles based on type
    messageDiv.style.padding = '15px';
    messageDiv.style.margin = '20px 0';
    messageDiv.style.borderRadius = '5px';
    messageDiv.style.textAlign = 'center';
    messageDiv.style.fontSize = '18px';
    messageDiv.style.fontWeight = 'bold';
    
    if (type === 'success') {
        messageDiv.style.backgroundColor = '#d4edda';
        messageDiv.style.color = '#155724';
        messageDiv.style.border = '1px solid #c3e6cb';
    } else if (type === 'error') {
        messageDiv.style.backgroundColor = '#f8d7da';
        messageDiv.style.color = '#721c24';
        messageDiv.style.border = '1px solid #f5c6cb';
    } else if (type === 'loading') {
        messageDiv.style.backgroundColor = '#d1ecf1';
        messageDiv.style.color = '#0c5460';
        messageDiv.style.border = '1px solid #bee5eb';
    }
    
    // Insert message after the form
    const form = document.querySelector('form');
    if (form && form.parentNode) {
        form.parentNode.insertBefore(messageDiv, form.nextSibling);
    }
}
