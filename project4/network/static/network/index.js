document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', event => {

        // Find what was clicked on
        const element = event.target;
    
        // Check if the user clicked on the edit button and do your magic
        if (element.className === 'edit-post') {
            element.style.display = 'none'
            element.parentElement.querySelector('.posted').style.display = 'none';
            element.parentElement.querySelector('.like-post').style.display = 'none';
            element.parentElement.querySelector('.edit-form').style.display = 'block';
        }
    });
});
