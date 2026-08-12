const loginForm =
    document.getElementById("loginForm");

const message =
    document.getElementById("message");

loginForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const email =
            document.getElementById("email").value.trim();

        const password =
            document.getElementById("password").value;

        if (!email || !password) {

            showMessage(
                "Please enter email and password.",
                "red"
            );

            return;
        }

        try {

            const response =
                await fetch(
                    "https://femcare-production-2b2d.up.railway.app/api/auth/login",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            email: email,
                            password: password
                        })
                    }
                );

            const data =
                await response.json();

            console.log(
                "Login response:",
                data
            );

            if (!response.ok) {

                showMessage(
                    data.message ||
                    "Invalid email or password.",
                    "red"
                );

                return;
            }

            const loggedInUser =
                data.user ||
                data.profile ||
                data;

            if (
                !loggedInUser.id &&
                !loggedInUser.user_id
            ) {

                showMessage(
                    "Login succeeded but user ID was not returned.",
                    "red"
                );

                return;
            }

            const user = {

                id:
                    loggedInUser.id ||
                    loggedInUser.user_id,

                name:
                    loggedInUser.name ||
                    "",

                email:
                    loggedInUser.email ||
                    email

            };

            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );

            showMessage(
                "Login successful.",
                "green"
            );

            setTimeout(
                function () {

                    window.location.href =
                        "dashboard.html";

                },
                500
            );

        } catch (error) {

            console.error(
                "Login error:",
                error
            );

            showMessage(
                "Unable to connect to the server.",
                "red"
            );

        }

    }
);


function showMessage(
    text,
    color
) {

    message.textContent =
        text;

    message.style.color =
        color;

}