// main.js - Custom JavaScript for DocShare fluidity
document.addEventListener("DOMContentLoaded", function() {
    // Add fade-in effect to elements with the 'fade-in' class on scroll
    const faders = document.querySelectorAll('.fade-in');

    const appearOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const appearOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, appearOptions);

    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });

    // Automatically make immediately visible elements appear
    setTimeout(() => {
        faders.forEach(fader => {
            const rect = fader.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                fader.classList.add('visible');
            }
        });
    }, 100);
});