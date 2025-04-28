function openEmailClient() {
    const bodytekst = "Giv mig mit data"
    const mailtoLink = `mailto:?body=${encodeURIComponent(bodytekst)}`;
    window.location.href = mailtoLink;
}


function tempLogin () {
    const tempUsername = document.getElementById("username")
    const tempPassword = document.getElementById("password")

    if (tempUsername == "admin" && tempPassword == "admin"){
        console.log(sessionStorage.setItem("admin"))
        console.log(sessionStorage.getItem(idk))
        
    }
        
}
