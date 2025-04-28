function openEmailClient() {
    const mailtoLink = `mailto:?body=${encodeURIComponent('xxx')}`;
    window.location.href = mailtoLink;
}


function tempLogin () {
    const tempUsername = document.getElementById("username")
    const tempPassword = document.getElementById("password")

    if (tempUsername == "admin" && tempPassword == "admin")
        
}
