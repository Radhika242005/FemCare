const registerForm =
    document.getElementById("registerForm");

const message =
    document.getElementById("message");

const registerButton =
    document.getElementById("registerButton");

const API =
    "http://127.0.0.1:5000";


registerForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const name =
            document.getElementById("name")
                .value
                .trim();

        const email =
            document.getElementById("email")
                .value
                .trim();

        const password =
            document.getElementById("password")
                .value;

        const confirmPassword =
            document.getElementById("confirmPassword")
                .value;


        message.textContent = "";
        message.style.color = "";


        if (!name) {

            message.textContent =
                "Please enter your full name.";

            message.style.color = "red";

            return;
        }


        if (!email) {

            message.textContent =
                "Please enter your email.";

            message.style.color = "red";

            return;
        }


        if (password.length < 6) {

            message.textContent =
                "Password must contain at least 6 characters.";

            message.style.color = "red";

            return;
        }


        if (password !== confirmPassword) {

            message.textContent =
                "Passwords do not match.";

            message.style.color = "red";

            return;
        }


        registerButton.disabled = true;

        registerButton.textContent =
            "Creating Account...";

        message.textContent =
            "Creating your FemCare account...";

        message.style.color = "#555";


        try {

            const response =
                await fetch(
                    `${API}/api/auth/register`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            name: name,

                            email: email,

                            password: password

                        })
                    }
                );


            const data =
                await response.json();


            console.log(
                "Register response:",
                data
            );


            if (!response.ok) {

                message.textContent =
                    data.message ||
                    "Unable to create account.";

                message.style.color = "red";

                registerButton.disabled = false;

                registerButton.textContent =
                    "Register";

                return;
            }


            if (data.success === false) {

                message.textContent =
                    data.message ||
                    "Registration failed.";

                message.style.color = "red";

                registerButton.disabled = false;

                registerButton.textContent =
                    "Register";

                return;
            }


            message.textContent =
                data.message ||
                "Account created successfully.";

            message.style.color = "green";


            registerButton.textContent =
                "Registered";


            setTimeout(
                function () {

                    window.location.href =
                        "login.html";

                },
                1000
            );


        } catch (error) {

            console.error(
                "Registration error:",
                error
            );


            message.textContent =
                "Unable to connect to the server.";

            message.style.color = "red";


            registerButton.disabled = false;

            registerButton.textContent =
                "Register";

        }

    }
);