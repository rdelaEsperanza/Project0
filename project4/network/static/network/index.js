document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', event => {

        // Find what was clicked on
        const element = event.target;
    
        // Check if the user clicked on a hide button
        if (element.className === 'edit-post') {
            element.style.display = 'none'
            element.parentElement.querySelector('p.posted').style.display = 'none';
            element.parentElement.querySelector('.edit-form').style.display = 'block';
        }
    });
});
