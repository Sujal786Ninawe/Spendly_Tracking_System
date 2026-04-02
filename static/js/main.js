// main.js — students will add JavaScript here as features are built

// Video Modal for "See how it works"
(function() {
    const modal = document.getElementById('videoModal');
    const btn = document.getElementById('howItWorksBtn');
    const closeBtn = document.getElementById('modalClose');
    const video = document.getElementById('modalVideo');
    const videoSrc = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    if (!modal || !btn) return;

    // Open modal
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        video.src = videoSrc;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    // Close modal function
    function closeModal() {
        video.src = '';
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Close on X button
    closeBtn.addEventListener('click', closeModal);

    // Close on overlay click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();
