const hamburger = document.querySelector('.hamburger');
        const menu = document.querySelector('.menu');
        const overlay = document.querySelector('.overlay');
    
        // Toggle menu visibility
        hamburger.addEventListener('click', () => {
          menu.classList.toggle('open');
          overlay.classList.toggle('active');
        });
    
        // Close menu when clicking on the overlay
        overlay.addEventListener('click', () => {
          menu.classList.remove('open');
          overlay.classList.remove('active');
        });