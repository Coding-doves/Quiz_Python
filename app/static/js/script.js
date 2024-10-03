// Make header background blur when scrolling
window.addEventListener('scroll', function() {
    let header = document.getElementById('menu');
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
  
// generate random position
function randomMovement() {
  return Math.floor(Math.random() * 90) + 5 + '%';
}

/* bubbles moves randomly on background
function bubbleMovement() {
  const bubbles = document.querySelectorAll('.bubbles1, .bubbles2, .bubbles3');
  bubbles.forEach(bubble => {
    bubble.style.left = randomMovement();
    bubble.style.top = randomMovement();
  })
}

bubbleMovement();

// Move every 2 seconds
setInterval(bubbleMovement, 2000);
*/
