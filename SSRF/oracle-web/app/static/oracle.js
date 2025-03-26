// oracle.js – used internally by the Oracle admin panel

async function fetchProphecy() {
    try {
        const res = await fetch('/admin/scrolls/73/prophecy');
        const text = await res.text();
        document.getElementById('prophecy').innerText = text;
    } catch (e) {
        document.getElementById('prophecy').innerText = '⚠️ Failed to retrieve scroll.';
    }
}

window.onload = fetchProphecy;
