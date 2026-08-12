const forgotPasswordForm =
    document.getElementById(
        "forgotPasswordForm"
    );


const message =
    document.getElementById(
        "message"
    );


const resetButton =
    document.getElementById(
        "resetButton"
    );


// ============================================================
// FORM SUBMIT
// ============================================================

forgotPasswordForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const email =
            document.getElementById(
                "email"
            ).value.trim().toLowerCase();


        const newPassword =
            document.getElementById(
                "newPassword"
            ).value;


        const confirmPassword =
            document.getElementById(
                "confirmPassword"
            ).value;


        // ====================================================
        // VALIDATION
        // ====================================================

        if (!email) {

            showMessage(
                "Please enter your email address.",
                "red"
            );

            return;
        }


        if (newPassword.length < 6) {

            showMessage(
                "Password must contain at least 6 characters.",
                "red"
            );

            return;
        }


        if (newPassword !== confirmPassword) {

            showMessage(
                "Passwords do not match.",
                "red"
            );

            return;
        }


        // ====================================================
        // DISABLE BUTTON
        // ====================================================

        resetButton.disabled = true;

        resetButton.style.opacity = "0.6";

        resetButton.style.cursor = "not-allowed";


        showMessage(
            "Changing your password...",
            "#7542a2"
        );


        // ====================================================
        // SEND REQUEST
        // ====================================================

        try {

            const response =
                await fetch(
                    "http://127.0.0.1:5000/api/auth/forgot-password",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                email:
                                    email,

                                new_password:
                                    newPassword,

                                confirm_password:
                                    confirmPassword

                            })
                    }
                );


            const data =
                await response.json();


            console.log(
                "Forgot password response:",
                data
            );


            // =================================================
            // SUCCESS
            // =================================================

            if (response.ok) {

                showMessage(
                    "Password changed successfully! Redirecting to login...",
                    "green"
                );


                forgotPasswordForm.reset();


                setTimeout(
                    function () {

                        window.location.href =
                            "login.html";

                    },
                    1500
                );


                return;
            }


            // =================================================
            // ERROR
            // =================================================

            showMessage(
                data.message ||
                "Unable to change password.",
                "red"
            );


            resetButton.disabled = false;

            resetButton.style.opacity = "1";

            resetButton.style.cursor = "pointer";


        } catch (error) {

            console.error(
                "Forgot password error:",
                error
            );


            showMessage(
                "Unable to connect to the FemCare server.",
                "red"
            );


            resetButton.disabled = false;

            resetButton.style.opacity = "1";

            resetButton.style.cursor = "pointer";

        }

    }
);


// ============================================================
// MESSAGE
// ============================================================

function showMessage(
    text,
    color
) {

    message.textContent = text;

    message.style.color = color;

}