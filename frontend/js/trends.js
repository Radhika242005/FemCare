const API = "https://femcare-production-2b2d.up.railway.app";

console.log("🔥 FEMCARE TRENDS.JS LOADED 🔥");

// ============================================================
// GET USER
// ============================================================

function getUserId() {

    const storedUser =
        localStorage.getItem("user");

    if (!storedUser) {

        window.location.href =
            "login.html";

        return null;
    }

    try {

        const user =
            JSON.parse(storedUser);

        return (
            user.id ||
            user.user_id ||
            user.userId
        );

    } catch (error) {

        console.error(
            "User parsing error:",
            error
        );

        localStorage.removeItem("user");

        window.location.href =
            "login.html";

        return null;
    }
}


const userId =
    getUserId();


// ============================================================
// ELEMENTS
// ============================================================

const message =
    document.getElementById("message");

const healthLogForm =
    document.getElementById("healthLogForm");

const logMessage =
    document.getElementById("logMessage");

const trendCard =
    document.getElementById("trendCard");

const trendContainer =
    document.getElementById("trendContainer");

const lifestyleCard =
    document.getElementById("lifestyleCard");

const lifestyleContainer =
    document.getElementById("lifestyleContainer");

const symptomCard =
    document.getElementById("symptomCard");

const symptomContainer =
    document.getElementById("symptomContainer");

const historicalCard =
    document.getElementById("historicalCard");

const sleepChart =
    document.getElementById("sleepChart");

const waterChart =
    document.getElementById("waterChart");

const stressChart =
    document.getElementById("stressChart");

const exerciseChart =
    document.getElementById("exerciseChart");


// ============================================================
// DISPLAY VALUE
// ============================================================

function displayValue(
    value,
    suffix = ""
) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "N/A";
    }

    return `${value}${suffix}`;
}


// ============================================================
// FORMAT DATE
// ============================================================

function formatDate(dateValue) {

    if (!dateValue) {

        return "N/A";
    }

    const date =
        new Date(dateValue);

    if (
        isNaN(
            date.getTime()
        )
    ) {

        return dateValue;
    }

    return date.toLocaleDateString(
        "en-GB",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );
}


// ============================================================
// FORMAT SHORT DATE
// ============================================================

function formatShortDate(dateValue) {

    if (!dateValue) {

        return "N/A";
    }

    const date =
        new Date(dateValue);

    if (
        isNaN(
            date.getTime()
        )
    ) {

        return dateValue;
    }

    return date.toLocaleDateString(
        "en-GB",
        {
            day: "2-digit",
            month: "short"
        }
    );
}


// ============================================================
// NUMBER
// ============================================================

function toNumber(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return null;
    }

    const number =
        Number(value);

    return Number.isFinite(number)
        ? number
        : null;
}


// ============================================================
// AVERAGE
// ============================================================

function calculateAverage(
    logs,
    field
) {

    const values =
        logs
            .map(
                log =>
                    toNumber(
                        log[field]
                    )
            )
            .filter(
                value =>
                    value !== null
            );

    if (
        values.length === 0
    ) {

        return null;
    }

    const total =
        values.reduce(
            (
                sum,
                value
            ) =>
                sum + value,
            0
        );

    return (
        total /
        values.length
    );
}


// ============================================================
// TOTAL
// ============================================================

function calculateTotal(
    logs,
    field
) {

    const values =
        logs
            .map(
                log =>
                    toNumber(
                        log[field]
                    )
            )
            .filter(
                value =>
                    value !== null
            );

    return values.reduce(
        (
            sum,
            value
        ) =>
            sum + value,
        0
    );
}


// ============================================================
// TREND
// ============================================================

function calculateTrend(
    logs,
    field
) {

    if (
        logs.length < 2
    ) {

        return {

            label:
                "Not enough data",

            description:
                "More health logs are needed to calculate a trend."
        };
    }


    const sortedLogs =
        [...logs].sort(
            (
                a,
                b
            ) =>
                new Date(
                    a.log_date
                ) -
                new Date(
                    b.log_date
                )
        );


    const values =
        sortedLogs
            .map(
                log =>
                    toNumber(
                        log[field]
                    )
            )
            .filter(
                value =>
                    value !== null
            );


    if (
        values.length < 2
    ) {

        return {

            label:
                "Not enough data",

            description:
                "More valid records are needed to calculate a trend."
        };
    }


    // ========================================================
    // COUNT CHANGES
    // ========================================================

    let increases = 0;

    let decreases = 0;


    for (
        let i = 1;
        i < values.length;
        i++
    ) {

        if (
            values[i] >
            values[i - 1]
        ) {

            increases++;

        } else if (
            values[i] <
            values[i - 1]
        ) {

            decreases++;
        }
    }


    // ========================================================
    // STABLE
    // ========================================================

    if (
        increases === 0 &&
        decreases === 0
    ) {

        return {

            label:
                "Stable",

            description:
                "Your recorded values have remained relatively stable."
        };
    }


    // ========================================================
    // ONLY INCREASING
    // ========================================================

    if (
        increases > 0 &&
        decreases === 0
    ) {

        return {

            label:
                "Improving",

            description:
                "Your recorded values have consistently increased over the recorded logs."
        };
    }


    // ========================================================
    // ONLY DECREASING
    // ========================================================

    if (
        decreases > 0 &&
        increases === 0
    ) {

        return {

            label:
                "Decreasing",

            description:
                "Your recorded values have consistently decreased over the recorded logs."
        };
    }


    // ========================================================
    // BOTH INCREASE AND DECREASE
    // ========================================================

    return {

        label:
            "Fluctuating",

        description:
            "Your recorded values have increased and decreased across the recorded logs."
    };
}


// ============================================================
// LOAD HEALTH LOGS
// ============================================================

async function loadHealthLogs() {

    if (!userId) {

        return;
    }

    try {

        if (message) {

            message.textContent =
                "Loading your health information...";

            message.style.color =
                "#756d79";
        }


        console.log(
            "Loading health logs for user:",
            userId
        );


        const response =
            await fetch(
                `${API}/api/health-logs/user/${userId}`
            );


        console.log(
            "Health log status:",
            response.status
        );


        if (!response.ok) {

            throw new Error(
                `Health log API returned ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "HEALTH LOG API RESPONSE:",
            data
        );


        if (!data.success) {

            throw new Error(
                data.message ||
                "Unable to load health logs."
            );
        }


        /*
         * API returns:
         *
         * {
         *     success: true,
         *     count: 4,
         *     logs: [...]
         * }
         *
         * Therefore use data.logs.
         */

        const logs =
            Array.isArray(
                data.logs
            )
                ? data.logs
                : [];


        if (
            logs.length === 0
        ) {

            showNoData();

            return;
        }


        if (message) {

            message.textContent = "";
        }


        // ====================================================
        // CALCULATIONS
        // ====================================================

        const averageSleep =
            calculateAverage(
                logs,
                "sleep_hours"
            );


        const averageWater =
            calculateAverage(
                logs,
                "water_intake_liters"
            );


        const averageStress =
            calculateAverage(
                logs,
                "stress_score"
            );


        const totalExercise =
            calculateTotal(
                logs,
                "exercise_minutes"
            );


        // ====================================================
        // DISPLAY OVERVIEW
        // ====================================================

        displayHealthOverview(
            logs,
            averageSleep,
            averageWater,
            averageStress,
            totalExercise
        );


        // ====================================================
        // DISPLAY TRENDS
        // ====================================================

        displayTrendAnalysis(
            logs
        );


        // ====================================================
        // DISPLAY HISTORY
        // ====================================================

        displayHistoryCharts(
            logs
        );


    } catch (error) {

        console.error(
            "HEALTH ANALYTICS ERROR:",
            error
        );


        if (message) {

            message.textContent =
                "Unable to load health analytics.";

            message.style.color =
                "red";
        }
    }
}


// ============================================================
// DISPLAY HEALTH OVERVIEW
// ============================================================

function displayHealthOverview(
    logs,
    averageSleep,
    averageWater,
    averageStress,
    totalExercise
) {

    if (
        !trendCard ||
        !trendContainer
    ) {

        return;
    }


    trendCard.style.display =
        "block";


    trendContainer.innerHTML = `

        <div class="trend-item">

            <div class="trend-icon">
                😴
            </div>

            <div class="trend-label">
                Average Sleep
            </div>

            <div class="trend-value">

                ${
                    averageSleep !== null
                        ? averageSleep.toFixed(2)
                        : "N/A"
                }

                ${
                    averageSleep !== null
                        ? " hrs"
                        : ""
                }

            </div>

        </div>


        <div class="trend-item">

            <div class="trend-icon">
                💧
            </div>

            <div class="trend-label">
                Average Water
            </div>

            <div class="trend-value">

                ${
                    averageWater !== null
                        ? averageWater.toFixed(2)
                        : "N/A"
                }

                ${
                    averageWater !== null
                        ? " L"
                        : ""
                }

            </div>

        </div>


        <div class="trend-item">

            <div class="trend-icon">
                🧘
            </div>

            <div class="trend-label">
                Average Stress
            </div>

            <div class="trend-value">

                ${
                    averageStress !== null
                        ? averageStress.toFixed(2)
                        : "N/A"
                }

                ${
                    averageStress !== null
                        ? " / 10"
                        : ""
                }

            </div>

        </div>


        <div class="trend-item">

            <div class="trend-icon">
                🏃
            </div>

            <div class="trend-label">
                Total Exercise
            </div>

            <div class="trend-value">

                ${totalExercise}
                min

            </div>

        </div>


        <div class="trend-item">

            <div class="trend-icon">
                📅
            </div>

            <div class="trend-label">
                Health Logs
            </div>

            <div class="trend-value">

                ${logs.length}

            </div>

        </div>

    `;
}


// ============================================================
// DISPLAY TREND ANALYSIS
// ============================================================

function displayTrendAnalysis(
    logs
) {

    const sleepTrend =
        calculateTrend(
            logs,
            "sleep_hours"
        );


    const waterTrend =
        calculateTrend(
            logs,
            "water_intake_liters"
        );


    const stressTrend =
        calculateTrend(
            logs,
            "stress_score"
        );


    const exerciseTrend =
        calculateTrend(
            logs,
            "exercise_minutes"
        );


    const trendSection =
        document.getElementById(
            "trendAnalysis"
        );


    if (!trendSection) {

        return;
    }


    trendSection.innerHTML = `

        <div class="trend-analysis-grid">


            <div class="analysis-item">

                <h3>
                    😴 Sleep Trend
                </h3>

                <div class="analysis-value">
                    ${sleepTrend.label}
                </div>

                <p>
                    ${sleepTrend.description}
                </p>

            </div>


            <div class="analysis-item">

                <h3>
                    💧 Water Trend
                </h3>

                <div class="analysis-value">
                    ${waterTrend.label}
                </div>

                <p>
                    ${waterTrend.description}
                </p>

            </div>


            <div class="analysis-item">

                <h3>
                    🧘 Stress Trend
                </h3>

                <div class="analysis-value">
                    ${stressTrend.label}
                </div>

                <p>
                    ${stressTrend.description}
                </p>

            </div>


            <div class="analysis-item">

                <h3>
                    🏃 Exercise Trend
                </h3>

                <div class="analysis-value">
                    ${exerciseTrend.label}
                </div>

                <p>
                    ${exerciseTrend.description}
                </p>

            </div>


        </div>

    `;
}


// ============================================================
// DISPLAY HISTORY CHARTS
// ============================================================

function displayHistoryCharts(
    logs
) {

    if (!historicalCard) {

        return;
    }


    historicalCard.style.display =
        "block";


    const sortedLogs =
        [...logs].sort(
            (
                a,
                b
            ) =>
                new Date(
                    a.log_date
                ) -
                new Date(
                    b.log_date
                )
        );


    createChart(
        sleepChart,
        sortedLogs,
        "sleep_hours",
        "hrs"
    );


    createChart(
        waterChart,
        sortedLogs,
        "water_intake_liters",
        "L"
    );


    createChart(
        stressChart,
        sortedLogs,
        "stress_score",
        "/10"
    );


    createChart(
        exerciseChart,
        sortedLogs,
        "exercise_minutes",
        "min"
    );
}


// ============================================================
// CREATE BAR CHART
// ============================================================

function createChart(
    container,
    logs,
    field,
    unit
) {

    if (!container) {

        return;
    }


    container.innerHTML =
        "";


    const values =
        logs
            .map(
                log => ({

                    date:
                        log.log_date,

                    value:
                        toNumber(
                            log[field]
                        )

                })
            )
            .filter(
                item =>
                    item.value !== null
            );


    if (
        values.length === 0
    ) {

        container.innerHTML = `

            <div class="no-chart-data">
                No data available
            </div>

        `;

        return;
    }


    const maxValue =
        Math.max(
            ...values.map(
                item =>
                    item.value
            ),
            1
        );


    values.forEach(
        item => {

            const chartBar =
                document.createElement(
                    "div"
                );


            chartBar.className =
                "chart-bar";


            const barValue =
                document.createElement(
                    "div"
                );


            barValue.className =
                "bar-value";


            barValue.textContent =
                `${item.value} ${unit}`;


            const bar =
                document.createElement(
                    "div"
                );


            bar.className =
                "bar";


            const height =
                Math.max(
                    5,
                    (
                        item.value /
                        maxValue
                    ) * 190
                );


            bar.style.height =
                `${height}px`;


            const barDate =
                document.createElement(
                    "div"
                );


            barDate.className =
                "bar-date";


            barDate.textContent =
                formatShortDate(
                    item.date
                );


            chartBar.appendChild(
                barValue
            );


            chartBar.appendChild(
                bar
            );


            chartBar.appendChild(
                barDate
            );


            container.appendChild(
                chartBar
            );

        }
    );
}


// ============================================================
// NO DATA
// ============================================================

function showNoData() {

    if (message) {

        message.textContent =
            "No health log data available.";

        message.style.color =
            "#666";
    }


    if (trendCard) {

        trendCard.style.display =
            "none";
    }


    if (lifestyleCard) {

        lifestyleCard.style.display =
            "none";
    }


    if (symptomCard) {

        symptomCard.style.display =
            "none";
    }


    if (historicalCard) {

        historicalCard.style.display =
            "none";
    }


    const trendSection =
        document.getElementById(
            "trendAnalysis"
        );


    if (trendSection) {

        trendSection.innerHTML = `

            <div class="analysis-item">

                <h3>
                    📊 Health Trends
                </h3>

                <p>
                    Continue recording health information
                    to generate meaningful trend analysis.
                </p>

            </div>

        `;
    }
}


// ============================================================
// SAVE HEALTH LOG
// ============================================================

if (healthLogForm) {

    healthLogForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            if (!userId) {

                return;
            }


            const logDate =
                document.getElementById(
                    "logDate"
                ).value;


            const sleepHours =
                document.getElementById(
                    "sleepHours"
                ).value;


            const waterIntake =
                document.getElementById(
                    "waterIntake"
                ).value;


            const stressScore =
                document.getElementById(
                    "stressScore"
                ).value;


            const exerciseMinutes =
                document.getElementById(
                    "exerciseMinutes"
                ).value;


            if (!logDate) {

                showLogMessage(
                    "Please select a date.",
                    "red"
                );

                return;
            }


            try {

                const response =
                    await fetch(
                        `${API}/api/health-logs`,
                        {

                            method:
                                "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify({

                                    user_id:
                                        Number(
                                            userId
                                        ),

                                    log_date:
                                        logDate,

                                    sleep_hours:
                                        sleepHours ||
                                        null,

                                    water_intake_liters:
                                        waterIntake ||
                                        null,

                                    stress_score:
                                        stressScore ||
                                        null,

                                    exercise_minutes:
                                        exerciseMinutes ||
                                        null

                                })

                        }
                    );


                const data =
                    await response.json();


                if (
                    !response.ok ||
                    !data.success
                ) {

                    throw new Error(
                        data.message ||
                        "Unable to save health log."
                    );
                }


                showLogMessage(
                    "Health log saved successfully!",
                    "green"
                );


                healthLogForm.reset();


                await loadHealthLogs();


            } catch (error) {

                console.error(
                    "SAVE HEALTH LOG ERROR:",
                    error
                );


                showLogMessage(
                    error.message ||
                    "Unable to save health log.",
                    "red"
                );
            }

        }
    );
}


// ============================================================
// LOG MESSAGE
// ============================================================

function showLogMessage(
    text,
    color
) {

    if (!logMessage) {

        return;
    }


    logMessage.textContent =
        text;


    logMessage.style.color =
        color;
}


// ============================================================
// NAVIGATION
// ============================================================

function goRecommendations() {

    window.location.href =
        "recommendations.html";
}


function goDashboard() {

    window.location.href =
        "dashboard.html";
}


// ============================================================
// INITIAL LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        loadHealthLogs();

    }
);