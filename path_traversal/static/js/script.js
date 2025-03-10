document.addEventListener("DOMContentLoaded", function() {
    const hintButton = document.querySelector(".hint-btn");
    const hintBox = document.getElementById("hint-box");

    if (hintButton) {
        hintButton.addEventListener("click", function(event) {
            event.preventDefault();

            // Dynamiska hintar för att leda spelaren vidare
            const hints = [
                "🔍 Not all scrolls can be found by ordinary means... Perhaps some files are hidden?",
                "📜 The scribes of old spoke of secret archives beyond what the eye can see...",
                "⚠️ Only the most skilled seekers will find the true knowledge. Look deeper.",
                "🏺 The Pharaoh’s most guarded secrets lie beyond the archives... How will you reach them?",
                "💀 The unworthy are misled by false scrolls... but the wise find the path beyond illusion."
            ];

            // Slumpa en hint
            const randomHint = hints[Math.floor(Math.random() * hints.length)];

            // Visa hint-boxen med den slumpade hinten
            hintBox.innerHTML = `<p class="alert alert-warning">${randomHint}</p>`;
            hintBox.style.display = "block";  
        });
    }
});
