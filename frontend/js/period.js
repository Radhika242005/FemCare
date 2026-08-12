const periodForm =
    document.getElementById("periodForm");

const message =
    document.getElementById("message");

const resultCard =
    document.getElementById("resultCard");

const saveButton =
    document.getElementById("saveButton");


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
        "User data error:",
        error
    );

    localStorage.removeItem("user");

    window.location.href =
        "login.html";

}


const userId =
    user.id ||
    user.user_id ||
    user.userId;


if (!userId) {

    localStorage.removeItem("user");

    window.location.href =
        "login.html";

}


// ============================================================
// SAVE PERIOD DATA
// ============================================================

periodForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        // ----------------------------------------------------
        // GET VALUES
        // ----------------------------------------------------

        const startDate =
            document.getElementById(
                "startDate"
            ).value;


        const cycleLength =
            document.getElementById(
                "cycleLength"
            ).value;


        const flowLevel =
            document.getElementById(
                "flowLevel"
            ).value;


        const painLevel =
            document.getElementById(
                "painLevel"
            ).value;


        const pmsSymptoms =
            document.getElementById(
                "pmsSymptoms"
            ).value;


        const moodScore =
            document.getElementById(
                "moodScore"
            ).value;


        const stressScore =
            document.getElementById(
                "stressScore"
            ).value;


        const sleepHours =
            document.getElementById(
                "sleepHours"
            ).value;


        const energyLevel =
            document.getElementById(
                "energyLevel"
            ).value;


        const concentrationScore =
            document.getElementById(
                "concentrationScore"
            ).value;


        const workHoursLost =
            document.getElementById(
                "workHoursLost"
            ).value;


        const preparedBeforePeriod =
            document.getElementById(
                "preparedBeforePeriod"
            ).value;


        // ----------------------------------------------------
        // VALIDATION
        // ----------------------------------------------------

        if (!startDate) {

            showMessage(
                "Please select the period start date.",
                "red"
            );

            return;

        }


        // ----------------------------------------------------
        // CREATE DATA
        // ----------------------------------------------------

        const periodData = {

            user_id:
                userId,

            start_date:
                startDate,

            cycle_length_days:
                cycleLength || null,

            flow_level:
                flowLevel || null,

            pain_level:
                painLevel || null,

            pms_symptoms:
                pmsSymptoms || null,

            mood_score:
                moodScore || null,

            stress_score_cycle:
                stressScore || null,

            sleep_hours_cycle:
                sleepHours || null,

            energy_level:
                energyLevel || null,

            concentration_score:
                concentrationScore || null,

            work_hours_lost:
                workHoursLost || null,

            prepared_before_period:
                preparedBeforePeriod === ""
                    ? null
                    : Number(
                        preparedBeforePeriod
                    )

        };


        console.log(
            "Sending period data:",
            periodData
        );


        // ----------------------------------------------------
        // UI
        // ----------------------------------------------------

        showMessage(
            "Saving your period data...",
            "#7542a2"
        );


        saveButton.disabled =
            true;

        saveButton.textContent =
            "Saving...";


        try {


            // ------------------------------------------------
            // SEND TO FLASK
            // ------------------------------------------------

            const response =
                await fetch(
                    "https://femcare-production-2b2d.up.railway.app/api/periods",
                    {

                        method:
                            "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(
                                periodData
                            )

                    }
                );


            // ------------------------------------------------
            // READ RESPONSE
            // ------------------------------------------------

            const data =
                await response.json();


            console.log(
                "Server response:",
                data
            );


            // ------------------------------------------------
            // ERROR
            // ------------------------------------------------

            if (!response.ok) {

                showMessage(
                    data.message ||
                    "Unable to save period data.",
                    "red"
                );

                return;

            }


            // ------------------------------------------------
            // SUCCESS
            // ------------------------------------------------

            showMessage(
                "✓ Period data saved successfully!",
                "green"
            );


            displaySavedResult(
                data,
                periodData
            );


            // Clear form after successful save

            periodForm.reset();


        } catch (error) {

            console.error(
                "Period request error:",
                error
            );


            showMessage(
                "Unable to connect to the FemCare server.",
                "red"
            );


        } finally {

            saveButton.disabled =
                false;

            saveButton.textContent =
                "Save Period Data";

        }

    }
);


// ============================================================
// DISPLAY SAVED RESULT
// ============================================================

function displaySavedResult(
    data,
    periodData
) {


    /*
       The backend may return the cycle information
       using different property names.

       These fallbacks allow the page to work with
       your existing response as well as a response
       containing the newly created record.
    */


    const record =
        data.period ||
        data.record ||
        data.data ||
        data;


    // --------------------------------------------------------
    // CYCLE NUMBER
    // --------------------------------------------------------

    const cycleNumber =
        record.cycle_number ||
        data.cycle_number ||
        record.cycleNumber ||
        "-";


    document.getElementById(
        "cycleNumber"
    ).textContent =
        cycleNumber;


    // --------------------------------------------------------
    // START DATE
    // --------------------------------------------------------

    document.getElementById(
        "resultStartDate"
    ).textContent =
        formatDate(
            record.start_date ||
            periodData.start_date
        );


    // --------------------------------------------------------
    // FLOW
    // --------------------------------------------------------

    document.getElementById(
        "resultFlow"
    ).textContent =
        record.flow_level ||
        periodData.flow_level ||
        "Not entered";


    // --------------------------------------------------------
    // CYCLE LENGTH
    // --------------------------------------------------------

    document.getElementById(
        "resultCycleLength"
    ).textContent =
        formatWithUnit(
            record.cycle_length_days ||
            periodData.cycle_length_days,
            "days"
        );


    // --------------------------------------------------------
    // PAIN
    // --------------------------------------------------------

    document.getElementById(
        "resultPain"
    ).textContent =
        formatScore(
            record.pain_level ??
            periodData.pain_level
        );


    // --------------------------------------------------------
    // MOOD
    // --------------------------------------------------------

    document.getElementById(
        "resultMood"
    ).textContent =
        formatScore(
            record.mood_score ??
            periodData.mood_score
        );


    // --------------------------------------------------------
    // STRESS
    // --------------------------------------------------------

    document.getElementById(
        "resultStress"
    ).textContent =
        formatScore(
            record.stress_score_cycle ??
            periodData.stress_score_cycle
        );


    // --------------------------------------------------------
    // SLEEP
    // --------------------------------------------------------

    document.getElementById(
        "resultSleep"
    ).textContent =
        formatWithUnit(
            record.sleep_hours_cycle ??
            periodData.sleep_hours_cycle,
            "hrs"
        );


    // --------------------------------------------------------
    // ENERGY
    // --------------------------------------------------------

    document.getElementById(
        "resultEnergy"
    ).textContent =
        formatScore(
            record.energy_level ??
            periodData.energy_level
        );


    // --------------------------------------------------------
    // CONCENTRATION
    // --------------------------------------------------------

    document.getElementById(
        "resultConcentration"
    ).textContent =
        formatScore(
            record.concentration_score ??
            periodData.concentration_score
        );


    // --------------------------------------------------------
    // WORK HOURS
    // --------------------------------------------------------

    document.getElementById(
        "resultWorkHours"
    ).textContent =
        formatWithUnit(
            record.work_hours_lost ??
            periodData.work_hours_lost,
            "hrs"
        );


    // --------------------------------------------------------
    // PREPARED
    // --------------------------------------------------------

    document.getElementById(
        "resultPrepared"
    ).textContent =
        formatPrepared(
            record.prepared_before_period ??
            periodData.prepared_before_period
        );


    // --------------------------------------------------------
    // SHOW RESULT
    // --------------------------------------------------------

    resultCard.style.display =
        "block";


    resultCard.scrollIntoView({
        behavior:
            "smooth",

        block:
            "start"
    });

}


// ============================================================
// FORMAT SCORE
// ============================================================

function formatScore(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "Not entered";

    }


    return `${value}/10`;

}


// ============================================================
// FORMAT WITH UNIT
// ============================================================

function formatWithUnit(
    value,
    unit
) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "Not entered";

    }


    return `${value} ${unit}`;

}


// ============================================================
// FORMAT PREPARED
// ============================================================

function formatPrepared(
    value
) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "Not entered";

    }


    if (
        value === 1 ||
        value === "1" ||
        value === true
    ) {

        return "Yes";

    }


    if (
        value === 0 ||
        value === "0" ||
        value === false
    ) {

        return "No";

    }


    return value;

}


// ============================================================
// FORMAT DATE
// ============================================================

function formatDate(
    value
) {

    if (!value) {

        return "Not entered";

    }


    const date =
        new Date(value);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return value;

    }


    return date.toLocaleDateString(
        "en-IN",
        {
            day:
                "2-digit",

            month:
                "short",

            year:
                "numeric"
        }
    );

}


// ============================================================
// MESSAGE
// ============================================================

function showMessage(
    text,
    color
) {

    message.textContent =
        text;

    message.style.color =
        color;

}


// ============================================================
// DASHBOARD
// ============================================================

function goDashboard() {

    window.location.href =
        "dashboard.html";

}