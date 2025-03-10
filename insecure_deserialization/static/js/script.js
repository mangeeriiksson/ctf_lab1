// 🌟 Fade-in-effekt för hela sidan vid laddning
document.addEventListener("DOMContentLoaded", function() {
    document.body.classList.add("fade-in");

    // 🚀 Starta hieroglyf-animationen efter 1 sek
    setTimeout(() => {
        let hieroglyphs = document.querySelectorAll(".hieroglyphs");
        hieroglyphs.forEach((glyph) => {
            glyph.style.opacity = "1";
            glyph.style.transform = "scale(1)";
        });
    }, 1000);
});

// ✨ Knapp-glödande effekt vid hovring
let buttons = document.querySelectorAll(".glowing-button");
buttons.forEach((btn) => {
    btn.addEventListener("mouseenter", function () {
        this.style.boxShadow = "0 0 20px gold, 0 0 30px rgba(255, 215, 0, 0.6)";
    });

    btn.addEventListener("mouseleave", function () {
        this.style.boxShadow = "0 0 5px goldenrod";
    });
});

// 📜 Gör så att ledtrådar sakta rullar fram vid klick
let hintBtn = document.querySelector(".hint-btn");
if (hintBtn) {
    hintBtn.addEventListener("click", function (event) {
        event.preventDefault();
        let hintBox = document.querySelector(".hint-box");
        if (hintBox) {
            hintBox.style.display = "block";
            hintBox.style.animation = "fadeInEffect 1s ease-in-out forwards";
        }
    });
}

// 🎭 Skapa en mystisk blinkande effekt på varningstext
let warningText = document.querySelector(".warning");
if (warningText) {
    setInterval(() => {
        warningText.style.opacity = (warningText.style.opacity == "1") ? "0.5" : "1";
    }, 800);
}
