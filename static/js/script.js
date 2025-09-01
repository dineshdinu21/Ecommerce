// console.log("Script loaded ✅");

document.addEventListener("DOMContentLoaded", function () {
    function setupToggle(inputId, toggleId) {
        const passwordField = document.getElementById(inputId);
        const togglePassword = document.getElementById(toggleId);

        if (passwordField && togglePassword) {
            togglePassword.addEventListener("click", function () {
                const type = passwordField.type === "password" ? "text" : "password";
                passwordField.type = type;
                togglePassword.classList.toggle("bi-eye");
                togglePassword.classList.toggle("bi-eye-slash");
            });
        }
    }

    setupToggle("password", "togglePassword");
    setupToggle("confirm_password", "toggleConfirmPassword");
    setupToggle("reset_old_password", "toggleResetOldPassword");
    setupToggle("reset_new_password", "toggleResetNewPassword");
    setupToggle("reset_confirm_password", "toggleResetConfirmPassword");
});






// document.addEventListener("DOMContentLoaded", function () {
//     const passwordField = document.getElementById("password");
//     const togglePassword = document.getElementById("togglePassword");

//     if (passwordField && togglePassword) {
//         togglePassword.addEventListener("click", function () {
//             if (passwordField.type === "password") {
//                 passwordField.type = "text";
//                 togglePassword.textContent = "🙈"; // eye closed
//             } else {
//                 passwordField.type = "password";
//                 togglePassword.textContent = "👁️"; // eye open
//             }
//         });
//     }
// });