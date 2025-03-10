function showHint() {
    alert("Not all scrolls can be found by ordinary means... Perhaps some files are hidden?");
}

document.addEventListener("DOMContentLoaded", function() {
    const hintButton = document.querySelector(".btn-warning");
    if (hintButton) {
        hintButton.addEventListener("click", function(event) {
            event.preventDefault();
            showHint();
        });
    }
});