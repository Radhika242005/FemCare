const message = document.getElementById("message");
const profileCard = document.getElementById("profileCard");
const profileContainer = document.getElementById("profileContainer");
const referenceCard = document.getElementById("referenceCard");
const referenceContainer = document.getElementById("referenceContainer");
const resultCard = document.getElementById("resultCard");
const resultContainer = document.getElementById("resultContainer");
const medicalNotice = document.getElementById("medicalNotice");


// ============================================================
// CHECK LOGIN
// ============================================================

const storedUser = localStorage.getItem("user");

if (!storedUser) {
    window.location.href = "login.html";
}

let user;

try {
    user = JSON.parse(storedUser);
} catch (error) {
    console.error("Invalid user data:", error);
    localStorage.removeItem("user");
    window.location.href = "login.html";
}

if (!user || !user.id) {
    localStorage.removeItem("user");
    window.location.href = "login.html";
}


// ============================================================
// LOAD PCOS ANALYSIS
// ============================================================

async function loadPCOSAnalysis() {

    try {

        message.textContent = "Loading your PCOS analysis...";
        message.style.color = "#7542a2";

        const url =
            `http://127.0.0.1:5000/api/pcos/analyze/${user.id}`;

        console.log("Requesting:", url);

        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        console.log("Response status:", response.status);

        let data;

        try {
            data = await response.json();
        } catch (jsonError) {

            console.error(
                "Invalid JSON response:",
                jsonError
            );

            throw new Error(
                `Server returned an invalid response. Status: ${response.status}`
            );
        }

        console.log(
            "PCOS API response:",
            data
        );

        // ----------------------------------------------------
        // API ERROR
        // ----------------------------------------------------

        if (!response.ok) {

            message.textContent =
                data.message ||
                data.error ||
                `Unable to load PCOS analysis. HTTP ${response.status}`;

            message.style.color = "#c44c4c";

            return;
        }

        if (
            data.success === false ||
            data.success === "false"
        ) {

            message.textContent =
                data.message ||
                data.error ||
                "PCOS analysis could not be loaded.";

            message.style.color = "#c44c4c";

            return;
        }


        // ----------------------------------------------------
        // DISPLAY PROFILE
        // ----------------------------------------------------

        try {

            displayUserProfile(
                data.user_profile || {}
            );

        } catch (error) {

            console.error(
                "Profile display error:",
                error
            );
        }


        // ----------------------------------------------------
        // DISPLAY DATASET REFERENCE
        // ----------------------------------------------------

        try {

            displayReference(data);

        } catch (error) {

            console.error(
                "Reference display error:",
                error
            );

            referenceCard.style.display = "block";

            referenceContainer.innerHTML = `
                <div class="error-text">
                    Dataset reference could not be displayed.
                </div>
            `;
        }


        // ----------------------------------------------------
        // DISPLAY RESULT
        // ----------------------------------------------------

        try {

            displayResult(data);

        } catch (error) {

            console.error(
                "Result display error:",
                error
            );
        }


        // ----------------------------------------------------
        // DISPLAY SIMILAR RECORDS
        // ----------------------------------------------------

        try {

            displaySimilarRecords(
                Array.isArray(data.similar_records)
                    ? data.similar_records
                    : []
            );

        } catch (error) {

            console.error(
                "Similar records display error:",
                error
            );
        }


        // ----------------------------------------------------
        // SUCCESS
        // ----------------------------------------------------

        message.textContent = "";

    } catch (error) {

        console.error(
            "PCOS analysis error:",
            error
        );

        message.textContent =
            error.message ||
            "Unable to load PCOS analysis.";

        message.style.color = "#c44c4c";
    }
}


// ============================================================
// DISPLAY USER PROFILE
// ============================================================

function displayUserProfile(profile) {

    if (!profileCard || !profileContainer) {
        console.error(
            "Profile elements not found in HTML."
        );
        return;
    }

    profileCard.style.display = "block";

    profileContainer.innerHTML = `

        <div class="profile-item">
            <span class="label">Age</span>
            <span class="value">
                ${displayValue(profile.age)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">BMI</span>
            <span class="value">
                ${displayValue(profile.bmi)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">Exercise</span>
            <span class="value">
                ${displayValue(profile.exercise_frequency)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">Diet Quality</span>
            <span class="value">
                ${displayValue(profile.diet_quality)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">Weight Gain</span>
            <span class="value">
                ${formatBinary(profile.weight_gain)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">Hair Growth</span>
            <span class="value">
                ${formatBinary(profile.hair_growth)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">Skin Darkening</span>
            <span class="value">
                ${formatBinary(profile.skin_darkening)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">Hair Loss</span>
            <span class="value">
                ${formatBinary(profile.hair_loss)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">Pimples</span>
            <span class="value">
                ${formatBinary(profile.pimples)}
            </span>
        </div>

        <div class="profile-item">
            <span class="label">Fast Food</span>
            <span class="value">
                ${formatBinary(profile.fast_food)}
            </span>
        </div>

    `;
}


// ============================================================
// DISPLAY DATASET REFERENCE
// ============================================================

function displayReference(data) {

    if (!referenceCard || !referenceContainer) {
        console.error(
            "Reference elements not found in HTML."
        );
        return;
    }

    const reference =
        data.reference_result || {};

    referenceCard.style.display = "block";

    const datasetRecords =
        data.dataset_records ??
        reference.dataset_records ??
        "Not available";

    const similarRecords =
        data.similar_records_used ??
        reference.similar_records_used ??
        "Not available";

    const positive =
        reference.pcos_positive ??
        reference.positive ??
        "Not available";

    const negative =
        reference.pcos_negative ??
        reference.negative ??
        "Not available";

    const percentage =
        reference.positive_percentage ??
        reference.pcos_positive_percentage ??
        "Not available";


    referenceContainer.innerHTML = `

        <div class="reference-item">

            <div class="reference-number">
                ${displayValue(datasetRecords)}
            </div>

            <div class="reference-label">
                Dataset Records
            </div>

        </div>


        <div class="reference-item">

            <div class="reference-number">
                ${displayValue(similarRecords)}
            </div>

            <div class="reference-label">
                Similar Records
            </div>

        </div>


        <div class="reference-item">

            <div class="reference-number">
                ${displayValue(positive)}
            </div>

            <div class="reference-label">
                PCOS-Positive
            </div>

        </div>


        <div class="reference-item">

            <div class="reference-number">
                ${displayValue(negative)}
            </div>

            <div class="reference-label">
                PCOS-Negative
            </div>

        </div>


        <div class="reference-item">

            <div class="reference-number">
                ${formatPercentage(percentage)}
            </div>

            <div class="reference-label">
                Reference Proportion
            </div>

        </div>

    `;
}


// ============================================================
// DISPLAY RESULT
// ============================================================

function displayResult(data) {

    if (!resultCard || !resultContainer) {
        console.error(
            "Result elements not found in HTML."
        );
        return;
    }

    resultCard.style.display = "block";

    const screeningResult =
        data.screening_result ||
        data.result ||
        data.reference_result?.screening_result ||
        "No reference result available.";


    resultContainer.innerHTML = `

        <p>
            <strong>
                ${escapeHTML(String(screeningResult))}
            </strong>
        </p>

        <p>
            This result is based on a comparison
            with similar records from the PCOS
            reference dataset.
        </p>

    `;


    if (medicalNotice) {

        medicalNotice.textContent =
            data.medical_notice ||
            "This is a dataset-based reference analysis and is not a medical diagnosis.";
    }
}


// ============================================================
// DISPLAY SIMILAR RECORDS
// ============================================================

function displaySimilarRecords(records) {

    const oldCard =
        document.getElementById(
            "similarRecordsCard"
        );

    if (oldCard) {
        oldCard.remove();
    }


    if (
        !Array.isArray(records) ||
        records.length === 0
    ) {

        console.log(
            "No similar PCOS records available."
        );

        return;
    }


    const card =
        document.createElement("section");

    card.id =
        "similarRecordsCard";

    card.className =
        "card";


    let rows = "";


    records.forEach(
        function(record, index) {

            rows += `

                <tr>

                    <td>
                        ${index + 1}
                    </td>

                    <td>
                        ${displayValue(record.age)}
                    </td>

                    <td>
                        ${displayValue(record.bmi)}
                    </td>

                    <td>
                        ${formatBinary(
                            record.exercise
                        )}
                    </td>

                    <td>
                        ${formatBinary(
                            record.weight_gain
                        )}
                    </td>

                    <td>
                        ${formatBinary(
                            record.hair_growth
                        )}
                    </td>

                    <td>
                        ${formatBinary(
                            record.skin_darkening
                        )}
                    </td>

                    <td>
                        ${formatBinary(
                            record.hair_loss
                        )}
                    </td>

                    <td>
                        ${formatBinary(
                            record.pimples
                        )}
                    </td>

                    <td>
                        ${formatBinary(
                            record.fast_food
                        )}
                    </td>

                    <td>

                        <span class="${
                            Number(
                                record.pcos_outcome
                            ) === 1
                                ? "positive"
                                : "negative"
                        }">

                            ${formatPCOSOutcome(
                                record.pcos_outcome
                            )}

                        </span>

                    </td>

                </tr>

            `;
        }
    );


    card.innerHTML = `

        <h2>
            🔎 Similar Dataset Records
        </h2>


        <p class="table-description">

            These are the records from the PCOS
            reference dataset that most closely
            match the selected profile and
            lifestyle characteristics.

        </p>


        <div class="table-wrapper">

            <table>

                <thead>

                    <tr>

                        <th>#</th>

                        <th>Age</th>

                        <th>BMI</th>

                        <th>Exercise</th>

                        <th>Weight Gain</th>

                        <th>Hair Growth</th>

                        <th>Skin Darkening</th>

                        <th>Hair Loss</th>

                        <th>Pimples</th>

                        <th>Fast Food</th>

                        <th>PCOS Outcome</th>

                    </tr>

                </thead>


                <tbody>

                    ${rows}

                </tbody>

            </table>

        </div>

    `;


    const container =
        document.querySelector(
            ".container"
        );

    const navigation =
        document.querySelector(
            ".navigation"
        );


    if (!container) {
        console.error(
            "Main container not found."
        );
        return;
    }


    if (navigation) {

        container.insertBefore(
            card,
            navigation
        );

    } else {

        container.appendChild(
            card
        );
    }
}


// ============================================================
// FORMAT YES / NO
// ============================================================

function formatBinary(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "Not entered";
    }


    if (
        value === true ||
        value === "Yes" ||
        value === "yes" ||
        Number(value) === 1
    ) {
        return "Yes";
    }


    if (
        value === false ||
        value === "No" ||
        value === "no" ||
        Number(value) === 0
    ) {
        return "No";
    }


    return value;
}


// ============================================================
// FORMAT PCOS OUTCOME
// ============================================================

function formatPCOSOutcome(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "Unknown";
    }


    if (
        value === true ||
        value === "Yes" ||
        Number(value) === 1
    ) {
        return "Positive";
    }


    if (
        value === false ||
        value === "No" ||
        Number(value) === 0
    ) {
        return "Negative";
    }


    return value;
}


// ============================================================
// DISPLAY EMPTY VALUES
// ============================================================

function displayValue(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "Not available";
    }

    return value;
}


// ============================================================
// FORMAT PERCENTAGE
// ============================================================

function formatPercentage(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "Not available";
    }

    const number =
        Number(value);

    if (Number.isNaN(number)) {
        return value;
    }

    return `${number}%`;
}


// ============================================================
// BASIC HTML ESCAPE
// ============================================================

function escapeHTML(value) {

    return value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ============================================================
// DASHBOARD
// ============================================================

function goDashboard() {

    window.location.href =
        "dashboard.html";
}


// ============================================================
// START
// ============================================================

loadPCOSAnalysis();