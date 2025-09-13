document.addEventListener("DOMContentLoaded", function() {
    // Display Messages with Auto-Dismiss
    let alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.classList.add("fade");
        }, 5000); // Auto-hide after 5 seconds
    });

    // Call-to-Action Button Click Behavior
    document.querySelectorAll(".cta").forEach(button => {
        button.addEventListener("click", function() {
            window.location.href = this.getAttribute("data-url");
        });
    });
});

function toggleChat() {
        var chatBox = document.getElementById("chat-box");
        chatBox.style.display = chatBox.style.display === "none" ? "block" : "none";
    }