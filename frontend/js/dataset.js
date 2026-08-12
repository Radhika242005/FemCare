const message =
    document.getElementById("message");

const content =
    document.getElementById("content");


// ============================================================
// LOAD DATASET ANALYSIS
// ============================================================

async function loadDatasetAnalysis() {

    try {

        message.textContent =
            "Loading dataset analysis...";


        const response =
            await fetch(
                "https://femcare-production-2b2d.up.railway.app/api/datasets/menstrual/analysis"
            );


        const data =
            await response.json();


        console.log(
            "Dataset analysis:",
            data
        );


        if (!response.ok) {

            message.textContent =
                data.message ||
                "Unable to load dataset analysis.";

            return;

        }


        if (
            !data.analysis
        ) {

            message.textContent =
                "No dataset analysis was returned.";

            return;

        }


        message.textContent =
            "";


        const analysis =
            data.analysis;


        const user =
            analysis.user_profile || {};


        const period =
            analysis.period_log || {};


        // ====================================================
        // MAIN CONTENT
        // ====================================================

        content.innerHTML = `


            <!-- =================================================
                 DATASET OVERVIEW
            ================================================== -->

            <section class="section">

                <h2 class="section-title">
                    📊 Dataset Overview
                </h2>

                <p class="section-description">
                    General information about the users
                    and records available in the reference
                    menstrual health dataset.
                </p>


                <div class="stats-grid">

                    ${statCard(
                        "👥",
                        user.total_users,
                        "Dataset Users"
                    )}


                    ${statCard(
                        "📋",
                        period.total_period_records,
                        "Period Records"
                    )}


                    ${statCard(
                        "🎂",
                        formatValue(
                            user.average_age
                        ),
                        "Average Age"
                    )}


                    ${statCard(
                        "⚖️",
                        formatValue(
                            user.average_bmi
                        ),
                        "Average BMI"
                    )}

                </div>

            </section>


            <!-- =================================================
                 HEALTH & CYCLE STATISTICS
            ================================================== -->

            <section class="section">

                <h2 class="section-title">
                    ❤️ Health & Cycle Statistics
                </h2>

                <p class="section-description">
                    Average values calculated from the
                    health and period information contained
                    in the reference dataset.
                </p>


                <div class="stats-grid">


                    ${statCard(
                        "📅",
                        formatValue(
                            period.average_cycle_length
                        ) + " days",
                        "Average Cycle Length"
                    )}


                    ${statCard(
                        "🩸",
                        formatValue(
                            period.average_pain
                        ) + " / 10",
                        "Average Pain"
                    )}


                    ${statCard(
                        "😊",
                        formatValue(
                            period.average_mood
                        ) + " / 10",
                        "Average Mood"
                    )}


                    ${statCard(
                        "🧘",
                        formatValue(
                            period.average_stress
                        ) + " / 10",
                        "Average Stress"
                    )}


                    ${statCard(
                        "😴",
                        formatValue(
                            period.average_sleep
                        ) + " hours",
                        "Average Cycle Sleep"
                    )}


                    ${statCard(
                        "🛌",
                        formatValue(
                            user.average_sleep_hours
                        ) + " hours",
                        "Average Profile Sleep"
                    )}


                    ${statCard(
                        "⚡",
                        formatValue(
                            period.average_energy
                        ) + " / 10",
                        "Average Energy"
                    )}


                    ${statCard(
                        "🧠",
                        formatValue(
                            period.average_concentration
                        ) + " / 10",
                        "Average Concentration"
                    )}


                    ${statCard(
                        "💼",
                        formatValue(
                            period.average_work_hours_lost
                        ) + " hours",
                        "Average Work Hours Lost"
                    )}


                    ${statCard(
                        "💧",
                        formatValue(
                            user.average_water_intake
                        ) + " L",
                        "Average Water Intake"
                    )}


                    ${statCard(
                        "😰",
                        formatValue(
                            user.average_baseline_stress
                        ) + " / 10",
                        "Baseline Stress"
                    )}

                </div>

            </section>


            <!-- =================================================
                 QUICK SUMMARY
            ================================================== -->

            <section class="section">

                <h2 class="section-title">
                    🔎 Dataset Summary
                </h2>


                <div class="summary-box">


                    <div class="summary-item">

                        <div class="summary-icon">
                            📅
                        </div>

                        <div class="summary-title">
                            Cycle Length
                        </div>

                        <div class="summary-value">
                            ${
                                formatValue(
                                    period.average_cycle_length
                                )
                            } days
                        </div>

                    </div>


                    <div class="summary-item">

                        <div class="summary-icon">
                            😴
                        </div>

                        <div class="summary-title">
                            Sleep
                        </div>

                        <div class="summary-value">
                            ${
                                formatValue(
                                    period.average_sleep
                                )
                            } hrs
                        </div>

                    </div>


                    <div class="summary-item">

                        <div class="summary-icon">
                            🧘
                        </div>

                        <div class="summary-title">
                            Stress
                        </div>

                        <div class="summary-value">
                            ${
                                formatValue(
                                    period.average_stress
                                )
                            } / 10
                        </div>

                    </div>


                </div>


                <div class="notice">

                    These statistics represent patterns
                    within the FemCare reference dataset.
                    They are provided for educational and
                    wellness reference purposes and are
                    not a medical diagnosis.

                </div>

            </section>


            <!-- =================================================
                 FLOW DISTRIBUTION
            ================================================== -->

            ${createDistributionSection(
                "🩸 Flow Distribution",
                analysis.flow_distribution
            )}


            <!-- =================================================
                 DIET DISTRIBUTION
            ================================================== -->

            ${createDistributionSection(
                "🥗 Diet Quality",
                analysis.diet_distribution
            )}


            <!-- =================================================
                 EXERCISE DISTRIBUTION
            ================================================== -->

            ${createDistributionSection(
                "🏃 Exercise Frequency",
                analysis.exercise_distribution
            )}

        `;


    } catch (error) {

        console.error(
            "Dataset error:",
            error
        );


        message.textContent =
            "Unable to connect to the FemCare server.";

    }

}


// ============================================================
// STAT CARD
// ============================================================

function statCard(
    icon,
    value,
    label
) {

    return `

        <div class="stat-card">

            <div class="stat-icon">
                ${icon}
            </div>

            <div class="stat-value">
                ${value}
            </div>

            <div class="stat-label">
                ${label}
            </div>

        </div>

    `;

}


// ============================================================
// FORMAT VALUE
// ============================================================

function formatValue(
    value
) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "N/A";

    }


    const number =
        Number(value);


    if (
        !Number.isNaN(number)
    ) {

        if (
            Number.isInteger(number)
        ) {

            return String(
                number
            );

        }


        return number.toFixed(2);

    }


    return value;

}


// ============================================================
// DISTRIBUTION SECTION
// ============================================================

function createDistributionSection(
    title,
    data
) {

    if (
        !data ||
        typeof data !== "object"
    ) {

        return `

            <section class="section">

                <h2 class="section-title">
                    ${title}
                </h2>

                <p class="section-description">
                    No distribution data available.
                </p>

            </section>

        `;

    }


    const entries =
        Object.entries(
            data
        );


    if (
        entries.length === 0
    ) {

        return `

            <section class="section">

                <h2 class="section-title">
                    ${title}
                </h2>

                <p class="section-description">
                    No distribution data available.
                </p>

            </section>

        `;

    }


    let rows = "";


    entries.forEach(
        ([name, count]) => {

            rows += `

                <div class="distribution-row">

                    <span class="distribution-name">
                        ${name}
                    </span>

                    <span class="distribution-count">
                        ${count}
                    </span>

                </div>

            `;

        }
    );


    return `

        <section class="section">

            <h2 class="section-title">
                ${title}
            </h2>

            <p class="section-description">
                Number of records belonging to
                each category in the dataset.
            </p>

            <div class="distribution">

                ${rows}

            </div>

        </section>

    `;

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

loadDatasetAnalysis();