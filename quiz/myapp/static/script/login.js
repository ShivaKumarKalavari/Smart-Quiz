function switchRole(role) {
    const formTitle = document.getElementById("form-title");
    const roleInput = document.getElementById("role");

    if (role === "admin") {
        formTitle.innerText = "Admin Login";
        roleInput.value = "admin";
    } else {
        formTitle.innerText = "Participant Login";
        roleInput.value = "participant";
    }
}