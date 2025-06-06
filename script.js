function openEmailClient() {
    const username = sessionStorage.getItem("username") || "[Dit navn]";
    const bodytekst = `Hej!\n\nJeg ønsker at få tilsendt mine tandlægejournaler digitalt.\n\nJeg giver hermed samtykke til at modtage mine journaler på denne mail.\n\nVenlig hilsen\n${username}`;
    const mailtoLink = `mailto:?subject=Anmodning om journal&body=${encodeURIComponent(bodytekst)}`;
    window.location.href = mailtoLink;
}

// --- SESSIONBESKYTTELSE TIL ALLE SIDER ---
function checkSessionOrRedirect() {
    const username = sessionStorage.getItem("username");
    if (!username) {
        alert("Du er ikke logget ind!");
        window.location.href = "login.html";
    }
}

// --- DYNAMISK NAVBAR ---
function setNavbarButtons() {
    const navButtons = document.getElementById('nav-buttons');
    if (!navButtons) return;
    const username = sessionStorage.getItem('username');
    if (username) {
        navButtons.innerHTML = '<button class="login-btn" onclick="logout()">Log ud</button>';
    } else {
        navButtons.innerHTML = '<button class="login-btn" onclick="location.href=\'login.html\'">Log in</button> <button class="signup-btn" onclick="location.href=\'signup.html\'">Opret bruger</button>';
    }
}

// --- FORBEDRET LOGIN ---
function tempLogin() {
    const tempUsername = document.getElementById("username").value.trim();
    const tempPassword = document.getElementById("password").value.trim();
    if (tempUsername.length < 3) {
        alert("Brugernavn skal være mindst 3 tegn.");
        return;
    }
    if (tempUsername === "admin" && tempPassword === "admin") {
        sessionStorage.setItem("username", tempUsername);
        // Opret tom fil-liste hvis ikke eksisterer
        if (!localStorage.getItem(tempUsername + "_files")) {
            localStorage.setItem(tempUsername + "_files", JSON.stringify([]));
        }
        window.location.href = "userdata.html";
    } else {
        alert("Ugyldigt brugernavn eller adgangskode.");
    }
}

// --- LOG UD ---
function logout() {
    sessionStorage.clear();
    window.location.href = "login.html";
}

// --- UPLOAD FUNKTION (kun frontend/demo) ---
function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput || fileInput.files.length === 0) {
        alert("Vælg en fil først.");
        return;
    }
    const file = fileInput.files[0];
    if (file.type !== "application/pdf") {
        alert("Kun PDF-filer er tilladt.");
        return;
    }
    // Gem filnavn i localStorage (pr. bruger)
    const username = sessionStorage.getItem("username");
    if (!username) {
        alert("Du er ikke logget ind!");
        window.location.href = "login.html";
        return;
    }
    let files = JSON.parse(localStorage.getItem(username + "_files") || "[]");
    files.push(file.name);
    localStorage.setItem(username + "_files", JSON.stringify(files));
    alert("Filen er uploadet!");
    window.location.href = "userdata.html";
}

// --- VISNING AF JOURNALER ---
function showUserFiles() {
    const username = sessionStorage.getItem("username");
    if (!username) return;
    const files = JSON.parse(localStorage.getItem(username + "_files") || "[]");
    const tableBody = document.getElementById("user-journals-list");
    if (!tableBody) return;
    tableBody.innerHTML = "";
    if (files.length === 0) {
        tableBody.innerHTML = '<tr><td>Ingen journaler uploaded endnu.</td></tr>';
    } else {
        files.forEach((file, idx) => {
            tableBody.innerHTML += `<tr><td>${file} <button onclick="deleteFile(${idx})" style="margin-left:20px;">Slet</button></td></tr>`;
        });
    }
}

// --- SLET FUNKTION ---
function deleteFile(idx) {
    const username = sessionStorage.getItem("username");
    if (!username) return;
    let files = JSON.parse(localStorage.getItem(username + "_files") || "[]");
    if (idx >= 0 && idx < files.length) {
        if (confirm("Er du sikker på at du vil slette denne journal?")) {
            files.splice(idx, 1);
            localStorage.setItem(username + "_files", JSON.stringify(files));
            showUserFiles();
        }
    }
}

// --- INITIERING PÅ HVER SIDE ---
document.addEventListener("DOMContentLoaded", function() {
    // Navbar på alle sider
    setNavbarButtons();
    // Sessionbeskyttelse på sider med data
    if (window.location.pathname.includes("userdata.html") || window.location.pathname.includes("Upload.html")) {
        checkSessionOrRedirect();
    }
    // Vis brugerfiler på userdata.html
    if (window.location.pathname.includes("userdata.html")) {
        showUserFiles();
    }
    // --- UPLOAD.html forbedring: brug uploadFile fra script.js og sessionbeskyttelse ---
    if (window.location.pathname.includes("Upload.html")) {
        const uploadBtn = document.querySelector('button[onclick^="uploadFile"]');
        if (uploadBtn) {
            uploadBtn.onclick = uploadFile;
        }
    }
});
