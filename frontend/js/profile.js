const profileForm =
    document.getElementById("profileForm");

const message =
    document.getElementById("message");


// ============================================================
// CHECK LOGIN
// ============================================================

const storedUser =
    localStorage.getItem("user");

if (!storedUser) {

    window.location.href =
        "login.html";

}

let user;

try {

    user =
        JSON.parse(storedUser);

} catch (error) {

    console.error(
        "Invalid user data:",
        error
    );

    localStorage.removeItem("user");

    window.location.href =
        "login.html";
}


// ============================================================
// GET USER ID
// ============================================================

const userId =
    user.id ||
    user.user_id ||
    user.userId;

if (!userId) {

    showMessage(
        "Unable to identify the logged-in user.",
        "red"
    );

    throw new Error(
        "User ID not found."
    );
}


// ============================================================
// LOAD PROFILE
// ============================================================

async function loadProfile() {

    try {

        showMessage(
            "Loading your health profile...",
            "#666"
        );


        const response =
            await fetch(
                `https://femcare-production-2b2d.up.railway.app/api/users/profile/${userId}`
            );


        const data =
            await response.json();


        console.log(
            "Profile response:",
            data
        );


        if (!response.ok) {

            showMessage(
                data.message ||
                "Unable to load profile.",
                "red"
            );

            return;
        }


        // ====================================================
        // PROFILE EXISTS
        // ====================================================

        if (
            data.profile_exists &&
            data.profile
        ) {

            fillProfileForm(
                data.profile
            );

            showMessage(
                "Your saved profile has been loaded.",
                "green"
            );

        }


        // ====================================================
        // NO PROFILE
        // ====================================================

        else {

            showMessage(
                "No saved profile found. Please enter your information.",
                "#666"
            );

        }


    } catch (error) {

        console.error(
            "Load profile error:",
            error
        );


        showMessage(
            "Unable to connect to the FemCare server.",
            "red"
        );

    }

}


// ============================================================
// FILL PROFILE FORM
// ============================================================

function fillProfileForm(profile) {

    setValue(
        "age",
        profile.age
    );


    setValue(
        "bmi",
        profile.bmi
    );


    setValue(
        "dietQuality",
        profile.diet_quality
    );


    setValue(
        "exerciseFrequency",
        profile.exercise_frequency
    );


    setValue(
        "sleepHours",
        profile.sleep_hours
    );


    setValue(
        "caffeineIntake",
        profile.caffeine_intake
    );


    setValue(
        "waterIntake",
        profile.water_intake_liters
    );


    setValue(
        "alcoholConsumption",
        profile.alcohol_consumption
    );


    setValue(
        "smokingStatus",
        profile.smoking_status
    );


    setValue(
        "birthControl",
        profile.birth_control_use
    );


    setValue(
        "pcosDiagnosed",
        profile.pcos_diagnosed
    );


    setValue(
        "stressScore",
        profile.stress_score_baseline
    );


    // ========================================================
    // PCOS SYMPTOMS
    // ========================================================

    setValue(
        "weightGain",
        profile.weight_gain
    );


    setValue(
        "hairGrowth",
        profile.hair_growth
    );


    setValue(
        "skinDarkening",
        profile.skin_darkening
    );


    setValue(
        "hairLoss",
        profile.hair_loss
    );


    setValue(
        "pimples",
        profile.pimples
    );


    setValue(
        "fastFood",
        profile.fast_food
    );

}


// ============================================================
// SET FORM VALUE
// ============================================================

function setValue(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        console.warn(
            "Element not found:",
            elementId
        );

        return;
    }


    if (
        value === null ||
        value === undefined
    ) {

        element.value = "";

        return;
    }


    element.value =
        value;

}


// ============================================================
// SAVE / UPDATE PROFILE
// ============================================================

profileForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // ====================================================
        // COLLECT PROFILE DATA
        // ====================================================

        const profileData = {

            user_id:
                Number(userId),

            age:
                document.getElementById(
                    "age"
                ).value || null,

            bmi:
                document.getElementById(
                    "bmi"
                ).value || null,

            diet_quality:
                document.getElementById(
                    "dietQuality"
                ).value || null,

            exercise_frequency:
                document.getElementById(
                    "exerciseFrequency"
                ).value || null,

            sleep_hours:
                document.getElementById(
                    "sleepHours"
                ).value || null,

            caffeine_intake:
                document.getElementById(
                    "caffeineIntake"
                ).value || null,

            water_intake_liters:
                document.getElementById(
                    "waterIntake"
                ).value || null,

            alcohol_consumption:
                document.getElementById(
                    "alcoholConsumption"
                ).value || null,

            smoking_status:
                document.getElementById(
                    "smokingStatus"
                ).value || null,

            birth_control_use:
                document.getElementById(
                    "birthControl"
                ).value || null,

            pcos_diagnosed:
                document.getElementById(
                    "pcosDiagnosed"
                ).value || null,

            stress_score_baseline:
                document.getElementById(
                    "stressScore"
                ).value || null,


            // =================================================
            // PCOS SYMPTOMS
            // =================================================

            weight_gain:
                document.getElementById(
                    "weightGain"
                ).value || null,

            hair_growth:
                document.getElementById(
                    "hairGrowth"
                ).value || null,

            skin_darkening:
                document.getElementById(
                    "skinDarkening"
                ).value || null,

            hair_loss:
                document.getElementById(
                    "hairLoss"
                ).value || null,

            pimples:
                document.getElementById(
                    "pimples"
                ).value || null,

            fast_food:
                document.getElementById(
                    "fastFood"
                ).value || null

        };


        console.log(
            "Saving profile:",
            profileData
        );


        // ====================================================
        // SEND TO BACKEND
        // ====================================================

        try {

            showMessage(
                "Saving profile...",
                "#666"
            );


            const response =
                await fetch(
                    "https://femcare-production-2b2d.up.railway.app/api/users/profile",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                profileData
                            )
                    }
                );


            const data =
                await response.json();


            console.log(
                "Save profile response:",
                data
            );


            // =================================================
            // SUCCESS
            // =================================================

            if (response.ok) {

                showMessage(
                    data.message ||
                    "Health profile saved successfully.",
                    "green"
                );


                setTimeout(
                    function () {

                        window.location.href =
                            "dashboard.html";

                    },
                    1000
                );

            }


            // =================================================
            // ERROR
            // =================================================

            else {

                showMessage(
                    data.message ||
                    "Unable to save profile.",
                    "red"
                );

            }


        } catch (error) {

            console.error(
                "Save profile error:",
                error
            );


            showMessage(
                "Unable to connect to the FemCare server.",
                "red"
            );

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

    if (!message) {

        return;

    }

    message.textContent =
        text;

    message.style.color =
        color;

}


// ============================================================
// START
// ============================================================

loadProfile();