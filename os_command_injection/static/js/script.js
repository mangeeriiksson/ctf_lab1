document.addEventListener("DOMContentLoaded", function() {
    const hintButton = document.querySelector(".hint-btn");
    const hintBox = document.getElementById("hint-box");

    if (hintButton && hintBox) {
        hintButton.addEventListener("click", function(event) {
            event.preventDefault();
            hintBox.style.display = "block";  // Visar hint-boxen
        });
    }
});
