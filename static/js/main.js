/**
 * main.js — DocShare
 * Animations fluides et interactions UI
 */

document.addEventListener("DOMContentLoaded", function () {

    // ═══════════════════════════════════════════════════════
    // 1. FADE-IN au défilement (Intersection Observer)
    // ═══════════════════════════════════════════════════════
    const faders = document.querySelectorAll('.fade-in');

    if (faders.length > 0) {
        const appearOptions = {
            threshold: 0.08,
            rootMargin: "0px 0px -40px 0px"
        };

        const appearOnScroll = new IntersectionObserver(function (entries, observer) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, appearOptions);

        faders.forEach(fader => appearOnScroll.observe(fader));

        // Afficher immédiatement les éléments déjà visibles au chargement
        setTimeout(() => {
            faders.forEach(fader => {
                const rect = fader.getBoundingClientRect();
                if (rect.top < window.innerHeight) {
                    fader.classList.add('visible');
                }
            });
        }, 80);
    }

    // ═══════════════════════════════════════════════════════
    // 2. Fermeture automatique des alertes après 5 secondes
    // ═══════════════════════════════════════════════════════
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            // Utiliser Bootstrap's dismiss si disponible
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // ═══════════════════════════════════════════════════════
    // 3. Animation des cartes de documents au survol
    // ═══════════════════════════════════════════════════════
    const docCards = document.querySelectorAll('.doc-card');
    docCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transition = 'transform 0.25s ease, box-shadow 0.25s ease';
        });
    });

    // ═══════════════════════════════════════════════════════
    // 4. Bouton de recherche — animation au focus
    // ═══════════════════════════════════════════════════════
    const searchInput = document.querySelector('#search-input');
    const searchBox   = document.querySelector('.search-box');

    if (searchInput && searchBox) {
        searchInput.addEventListener('focus', () => {
            searchBox.style.boxShadow = '0 8px 40px rgba(21,101,192,0.25)';
            searchBox.style.transform = 'scale(1.01)';
            searchBox.style.transition = 'all 0.2s ease';
        });
        searchInput.addEventListener('blur', () => {
            searchBox.style.boxShadow = '0 8px 30px rgba(0,0,0,0.15)';
            searchBox.style.transform = 'scale(1)';
        });
    }

    // ═══════════════════════════════════════════════════════
    // 5. Navbar — changement de style au défilement
    // ═══════════════════════════════════════════════════════
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 20) {
                navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.12)';
            } else {
                navbar.style.boxShadow = '0 1px 4px rgba(0,0,0,0.08)';
            }
        }, { passive: true });
    }

});