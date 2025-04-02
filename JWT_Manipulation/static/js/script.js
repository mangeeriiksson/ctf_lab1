// Lägg längst ner i script.js
function animateFlagReveal() {
    const flag = document.querySelector(".flag");
    if (flag) {
        flag.style.opacity = 0;
        flag.style.transition = "opacity 2s ease-in-out";
        setTimeout(() => {
            flag.style.opacity = 1;
            flag.classList.add("glow-pulse");
        }, 300);
    }
}
