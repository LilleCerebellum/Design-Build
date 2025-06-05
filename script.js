function openEmailClient() {
    const bodytekst = "Giv mig mit data"
    const mailtoLink = `mailto:?body=${encodeURIComponent(bodytekst)}`;
    window.location.href = mailtoLink;
}

function tempLogin() {
    const tempUsername = document.getElementById("username").value;
    const tempPassword = document.getElementById("password").value;

    if (tempUsername === "admin" && tempPassword === "admin") {
        sessionStorage.setItem("username", tempUsername);
        sessionStorage.setItem("data", "Dette er dine data.");
        window.location.href = "userdata.html";
    } else {
        alert("Ugyldigt brugernavn eller adgangskode.");
    }
}

function logout() {
    sessionStorage.clear();
    window.location.href = "login.html";
}
