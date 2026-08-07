// Initialize dataLayer for GTM
window.dataLayer = window.dataLayer || [];

document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.site-header');
  const mobileMenu = document.querySelector('.mobile-menu');
  const mobileOverlay = document.querySelector('.mobile-overlay');
  const menuToggle = document.querySelector('.menu-toggle');
  const menuClose = document.querySelector('.menu-close');
  const mobileLinks = document.querySelectorAll('.mobile-link');
  const revealElements = document.querySelectorAll('.reveal');
  const heroBg = document.querySelector('.hero-bg');

  // Header scroll behavior
  let lastScroll = 0;
  const handleScroll = () => {
    const currentScroll = window.scrollY;
    
    if (currentScroll > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
  };
  
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  // Mobile menu
  const openMenu = () => {
    mobileMenu.classList.add('open');
    mobileOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  
  const closeMenu = () => {
    mobileMenu.classList.remove('open');
    mobileOverlay.classList.remove('open');
    document.body.style.overflow = '';
  };
  
  menuToggle.addEventListener('click', openMenu);
  menuClose.addEventListener('click', closeMenu);
  mobileOverlay.addEventListener('click', closeMenu);
  mobileLinks.forEach(link => link.addEventListener('click', closeMenu));

  // Scroll reveal with IntersectionObserver
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        revealObserver.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    rootMargin: '0px 0px -80px 0px',
    threshold: 0.1
  });
  
  revealElements.forEach(el => revealObserver.observe(el));

  // Hero parallax (throttled with rAF)
  if (heroBg) {
    let ticking = false;
    const updateParallax = () => {
      const scrolled = window.scrollY;
      const rate = scrolled * 0.4;
      if (rate < window.innerHeight) {
        heroBg.style.transform = `translateY(${rate}px) scale(1.1)`;
      }
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    }, { passive: true });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        const headerOffset = 110;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.scrollY - headerOffset;
        
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // CTA click tracking for GTM
  const ctaButtons = document.querySelectorAll('.cta-track');
  ctaButtons.forEach(button => {
    button.addEventListener('click', () => {
      const location = button.getAttribute('data-cta-location') || 'unknown';
      const text = button.getAttribute('data-cta-text') || 'unknown';
      const href = button.getAttribute('href') || '';
      
      window.dataLayer.push({
        event: 'cta_click',
        cta_location: location,
        cta_text: text,
        cta_url: href
      });
    });
  });

  // Image lazy load fade-in
  const images = document.querySelectorAll('img');
  images.forEach(img => {
    if (img.complete) {
      img.classList.add('loaded');
    } else {
      img.addEventListener('load', () => img.classList.add('loaded'));
    }
  });

  // Counter animation for highlights
  const counters = document.querySelectorAll('[data-counter]');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = entry.target;
        const end = parseInt(target.getAttribute('data-counter'));
        const duration = 2000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const ease = 1 - Math.pow(1 - progress, 3);
          target.textContent = Math.floor(ease * end);
          
          if (progress < 1) {
            requestAnimationFrame(animate);
          }
        };
        
        requestAnimationFrame(animate);
        counterObserver.unobserve(target);
      }
    });
  }, { threshold: 0.5 });
  
  counters.forEach(counter => counterObserver.observe(counter));
});
