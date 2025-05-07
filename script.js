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

function addNavbar() {
    const username = sessionStorage.getItem("username");
    let navbarHTML = `
        <div class="navbar">
            <div class="dropdown">
                <button class="dropbtn">Menu</button>
                <div class="dropdown-content">
                    <a href="index.html">Hjem</a>
                    <a href="sendmail.html">Send mail</a>
                </div>
            </div>
    `;
    if (username) {
        navbarHTML += `<button class="login-btn" onclick="logout()">Log ud</button>`;
    } else {
        navbarHTML += `<button class="login-btn" onclick="location.href='login.html'">Log ind</button>`;
    }
    navbarHTML += `</div>`;
    document.body.insertAdjacentHTML('afterbegin', navbarHTML);
}

function logout() {
    sessionStorage.clear();
    window.location.href = "login.html";
}
