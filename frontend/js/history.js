const message =
    document.getElementById("message");

const historyContainer =
    document.getElementById("historyContainer");

const trendContainer =
    document.getElementById("trendContainer");

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

// ============================================================
// LOAD PERIOD HISTORY
// ============================================================

async function loadHistory() {

    try {

        message.textContent =
            "Loading history...";

        const response =
            await fetch(
                `https://femcare-production-2b2d.up.railway.app/api/periods/history/${user.id}`
            );

        const data =
            await response.json();

        console.log(
            "History response:",
            data
        );

        if (!response.ok) {

            message.textContent =
                data.message ||
                "Unable to load history.";

            return;
        }

        const history =
            Array.isArray(data.history)
                ? data.history
                : [];

        message.textContent = "";

        // ----------------------------------------------------
        // NO HISTORY
        // ----------------------------------------------------

        if (history.length === 0) {

            historyContainer.innerHTML = `

                <div class="empty">

                    <h3>
                        No period history yet.
                    </h3>

                    <p>
                        Add your first period record.
                    </p>

                </div>

            `;

            trendContainer.innerHTML =
                "";

            return;
        }

        // ----------------------------------------------------
        // DISPLAY HISTORY
        // ----------------------------------------------------

        historyContainer.innerHTML =
            history.map(
                cycle => {

                    return `

                    <div class="cycle-card">

                        <h2 class="cycle-title">
                            Cycle ${displayValue(
                                cycle.cycle_number
                            )}
                        </h2>

                        <div class="data-grid">

                            <div class="data-item">

                                <span class="label">
                                    Start Date
                                </span>

                                <span class="value">
                                    ${formatDate(
                                        cycle.start_date
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Cycle Length
                                </span>

                                <span class="value">
                                    ${displayValue(
                                        cycle.cycle_length_days
                                    )}
                                    ${
                                        hasValue(
                                            cycle.cycle_length_days
                                        )
                                            ? " days"
                                            : ""
                                    }
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Previous Cycle Length
                                </span>

                                <span class="value">
                                    ${formatOptionalNumber(
                                        cycle.prev_cycle_length
                                    )}
                                    ${
                                        hasValue(
                                            cycle.prev_cycle_length
                                        )
                                            ? " days"
                                            : ""
                                    }
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Cycle Phase
                                </span>

                                <span class="value">
                                    ${displayValue(
                                        cycle.cycle_phase
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Flow
                                </span>

                                <span class="value">
                                    ${displayValue(
                                        cycle.flow_level
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Pain
                                </span>

                                <span class="value">
                                    ${formatScore(
                                        cycle.pain_level
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    PMS Symptoms
                                </span>

                                <span class="value">
                                    ${displayValue(
                                        cycle.pms_symptoms
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Mood
                                </span>

                                <span class="value">
                                    ${formatScore(
                                        cycle.mood_score
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Stress
                                </span>

                                <span class="value">
                                    ${formatScore(
                                        cycle.stress_score_cycle
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Sleep
                                </span>

                                <span class="value">
                                    ${
                                        hasValue(
                                            cycle.sleep_hours_cycle
                                        )
                                            ? `${formatOptionalNumber(
                                                cycle.sleep_hours_cycle
                                            )} hours`
                                            : "Not entered"
                                    }
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Energy
                                </span>

                                <span class="value">
                                    ${formatScore(
                                        cycle.energy_level
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Concentration
                                </span>

                                <span class="value">
                                    ${formatScore(
                                        cycle.concentration_score
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Work/Study Hours Lost
                                </span>

                                <span class="value">
                                    ${
                                        hasValue(
                                            cycle.work_hours_lost
                                        )
                                            ? `${formatOptionalNumber(
                                                cycle.work_hours_lost
                                            )} hours`
                                            : "Not entered"
                                    }
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Prepared Before Period
                                </span>

                                <span class="value">
                                    ${formatPrepared(
                                        cycle.prepared_before_period
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Overall Health Score
                                </span>

                                <span class="value">
                                    ${formatScore(
                                        cycle.overall_health_score
                                    )}
                                </span>

                            </div>


                            <div class="data-item">

                                <span class="label">
                                    Log Consistency
                                </span>

                                <span class="value">
                                    ${
                                        hasValue(
                                            cycle.log_consistency_score
                                        )
                                            ? `${formatOptionalNumber(
                                                cycle.log_consistency_score
                                            )}/100`
                                            : "Not entered"
                                    }
                                </span>

                            </div>

                        </div>

                    </div>

                    `;

                }
            ).join("");


        // ----------------------------------------------------
        // LOAD PERIOD TRENDS
        // ----------------------------------------------------

        await loadTrends();

    } catch (error) {

        console.error(
            "History error:",
            error
        );

        message.textContent =
            "Unable to connect to the FemCare server.";

    }

}

// ============================================================
// LOAD PERIOD TRENDS
// ============================================================

async function loadTrends() {

    try {

        const response =
            await fetch(
                `https://femcare-production-2b2d.up.railway.app/api/periods/trend/${user.id}`
            );

        const data =
            await response.json();

        console.log(
            "Trend response:",
            data
        );

        if (!response.ok) {

            trendContainer.innerHTML = `

                <div class="trend-card">

                    <h2>
                        📊 Health Trends
                    </h2>

                    <p>
                        ${
                            data.message ||
                            "Unable to load health trends."
                        }
                    </p>

                </div>

            `;

            return;
        }

        // ====================================================
        // LESS THAN TWO CYCLES
        // ====================================================

        if (!data.trend_available) {

            trendContainer.innerHTML = `

                <div class="trend-card">

                    <div class="trend-header">

                        <h2>
                            📊 Health Trends
                        </h2>

                        <p>
                            Comparison of your recent period cycles
                        </p>

                    </div>


                    <div class="trend-message">

                        <h3>
                            More history is needed
                        </h3>

                        <p>
                            ${
                                data.message ||
                                "At least two cycles are required for trend analysis."
                            }
                        </p>

                        <p>
                            Continue recording your period information.
                            Once you have at least two cycles,
                            FemCare can compare your previous and latest cycle.
                        </p>

                    </div>

                </div>

            `;

            return;
        }

        // ====================================================
        // TWO OR MORE CYCLES AVAILABLE
        // ====================================================

        const latest =
            data.latest_cycle;

        const previous =
            data.previous_cycle;

        const trend =
            data.trend || {};

        trendContainer.innerHTML = `

            <div class="trend-card">

                <div class="trend-header">

                    <h2>
                        📊 Health Trends
                    </h2>

                    <p>
                        Comparison of your recent period cycles
                    </p>

                </div>


                <div class="cycle-comparison">

                    <div class="comparison-box">

                        <span>
                            Previous Cycle
                        </span>

                        <strong>
                            Cycle ${displayValue(
                                previous.cycle_number
                            )}
                        </strong>

                        <small>
                            ${formatDate(
                                previous.start_date
                            )}
                        </small>

                    </div>


                    <div class="arrow">
                        →
                    </div>


                    <div class="comparison-box">

                        <span>
                            Latest Cycle
                        </span>

                        <strong>
                            Cycle ${displayValue(
                                latest.cycle_number
                            )}
                        </strong>

                        <small>
                            ${formatDate(
                                latest.start_date
                            )}
                        </small>

                    </div>

                </div>


                <div class="trend-grid">

                    ${createTrendCard(
                        "😴",
                        "Sleep",
                        previous.sleep_hours_cycle,
                        latest.sleep_hours_cycle,
                        trend.sleep,
                        "hours"
                    )}


                    ${createTrendCard(
                        "⚡",
                        "Energy",
                        previous.energy_level,
                        latest.energy_level,
                        trend.energy,
                        "/10"
                    )}


                    ${createTrendCard(
                        "🩸",
                        "Pain",
                        previous.pain_level,
                        latest.pain_level,
                        trend.pain,
                        "/10",
                        true
                    )}


                    ${createTrendCard(
                        "😌",
                        "Mood",
                        previous.mood_score,
                        latest.mood_score,
                        trend.mood,
                        "/10"
                    )}


                    ${createTrendCard(
                        "🧠",
                        "Concentration",
                        previous.concentration_score,
                        latest.concentration_score,
                        trend.concentration,
                        "/10"
                    )}


                    ${createTrendCard(
                        "😰",
                        "Stress",
                        previous.stress_score_cycle,
                        latest.stress_score_cycle,
                        trend.stress,
                        "/10",
                        true
                    )}


                    ${createTrendCard(
                        "📅",
                        "Cycle Length",
                        previous.cycle_length_days,
                        latest.cycle_length_days,
                        trend.cycle_length,
                        "days"
                    )}

                </div>


                <div class="trend-summary">

                    <h3>
                        Your Recent Changes
                    </h3>

                    ${createSummary(trend)}

                </div>

            </div>

        `;

    } catch (error) {

        console.error(
            "Trend error:",
            error
        );

        trendContainer.innerHTML = `

            <div class="trend-card">

                <h2>
                    📊 Health Trends
                </h2>

                <p>
                    Unable to load health trends.
                </p>

            </div>

        `;

    }

}

// ============================================================
// CREATE TREND CARD
// ============================================================

function createTrendCard(
    icon,
    title,
    previousValue,
    latestValue,
    trendData,
    unit,
    lowerIsBetter = false
) {

    const previousExists =
        hasValue(previousValue);

    const latestExists =
        hasValue(latestValue);

    const previous =
        previousExists
            ? Number(previousValue)
            : null;

    const latest =
        latestExists
            ? Number(latestValue)
            : null;

    const hasBothValues =
        previous !== null &&
        latest !== null &&
        !Number.isNaN(previous) &&
        !Number.isNaN(latest);

    const change =
        trendData &&
        trendData.change !== null &&
        trendData.change !== undefined &&
        trendData.change !== ""
            ? Number(trendData.change)
            : null;

    let status =
        "unchanged";

    let statusText =
        "Not enough data";

    let symbol =
        "→";

    // --------------------------------------------------------
    // BOTH VALUES AVAILABLE
    // --------------------------------------------------------

    if (hasBothValues) {

        if (lowerIsBetter) {

            if (change < 0) {

                status =
                    "improved";

                statusText =
                    "Improved";

                symbol =
                    "↓";

            } else if (change > 0) {

                status =
                    "increased";

                statusText =
                    "Increased";

                symbol =
                    "↑";

            } else {

                status =
                    "unchanged";

                statusText =
                    "Unchanged";

                symbol =
                    "→";
            }

        } else {

            if (change > 0) {

                status =
                    "improved";

                statusText =
                    "Improved";

                symbol =
                    "↑";

            } else if (change < 0) {

                status =
                    "decreased";

                statusText =
                    "Decreased";

                symbol =
                    "↓";

            } else {

                status =
                    "unchanged";

                statusText =
                    "Unchanged";

                symbol =
                    "→";
            }
        }

    }

    const previousDisplay =
        previous !== null &&
        !Number.isNaN(previous)
            ? `${formatNumber(previous)} ${unit}`
            : "N/A";

    const latestDisplay =
        latest !== null &&
        !Number.isNaN(latest)
            ? `${formatNumber(latest)} ${unit}`
            : "N/A";

    let changeDisplay =
        "";

    if (
        hasBothValues &&
        change !== null &&
        !Number.isNaN(change) &&
        change !== 0
    ) {

        changeDisplay =
            `(${change > 0 ? "+" : ""}${formatNumber(change)})`;
    }

    return `

        <div class="trend-item">

            <div class="trend-icon">
                ${icon}
            </div>

            <div class="trend-title">
                ${title}
            </div>

            <div class="trend-values">

                <span>
                    ${previousDisplay}
                </span>

                <strong>
                    →
                </strong>

                <span>
                    ${latestDisplay}
                </span>

            </div>

            <div class="trend-status ${status}">

                <span class="trend-symbol">
                    ${symbol}
                </span>

                ${statusText}

                ${changeDisplay}

            </div>

        </div>

    `;
}

// ============================================================
// CREATE SUMMARY
// ============================================================

function createSummary(trend) {

    const items = [];

    // --------------------------------------------------------
    // SLEEP
    // --------------------------------------------------------

    if (
        trend.sleep &&
        trend.sleep.change !== null &&
        trend.sleep.change !== undefined
    ) {

        if (trend.sleep.change > 0) {

            items.push(
                "Your sleep has improved."
            );

        } else if (
            trend.sleep.change < 0
        ) {

            items.push(
                "Your sleep has decreased."
            );

        } else {

            items.push(
                "Your sleep is unchanged."
            );

        }
    }

    // --------------------------------------------------------
    // ENERGY
    // --------------------------------------------------------

    if (
        trend.energy &&
        trend.energy.change !== null &&
        trend.energy.change !== undefined
    ) {

        if (trend.energy.change > 0) {

            items.push(
                "Your energy level has improved."
            );

        } else if (
            trend.energy.change < 0
        ) {

            items.push(
                "Your energy level has decreased."
            );

        } else {

            items.push(
                "Your energy level is unchanged."
            );
        }
    }

    // --------------------------------------------------------
    // PAIN
    // --------------------------------------------------------

    if (
        trend.pain &&
        trend.pain.change !== null &&
        trend.pain.change !== undefined
    ) {

        if (trend.pain.change < 0) {

            items.push(
                "Your period pain has decreased."
            );

        } else if (
            trend.pain.change > 0
        ) {

            items.push(
                "Your period pain has increased."
            );

        } else {

            items.push(
                "Your period pain is unchanged."
            );
        }
    }

    // --------------------------------------------------------
    // STRESS
    // --------------------------------------------------------

    if (
        trend.stress &&
        trend.stress.change !== null &&
        trend.stress.change !== undefined
    ) {

        if (trend.stress.change < 0) {

            items.push(
                "Your stress level has decreased."
            );

        } else if (
            trend.stress.change > 0
        ) {

            items.push(
                "Your stress level has increased."
            );

        } else {

            items.push(
                "Your stress level is unchanged."
            );
        }
    }

    // --------------------------------------------------------
    // MOOD
    // --------------------------------------------------------

    if (
        trend.mood &&
        trend.mood.change !== null &&
        trend.mood.change !== undefined
    ) {

        if (trend.mood.change > 0) {

            items.push(
                "Your mood score has improved."
            );

        } else if (
            trend.mood.change < 0
        ) {

            items.push(
                "Your mood score has decreased."
            );

        } else {

            items.push(
                "Your mood score is unchanged."
            );
        }
    }

    // --------------------------------------------------------
    // CONCENTRATION
    // --------------------------------------------------------

    if (
        trend.concentration &&
        trend.concentration.change !== null &&
        trend.concentration.change !== undefined
    ) {

        if (
            trend.concentration.change > 0
        ) {

            items.push(
                "Your concentration level has improved."
            );

        } else if (
            trend.concentration.change < 0
        ) {

            items.push(
                "Your concentration level has decreased."
            );

        } else {

            items.push(
                "Your concentration level is unchanged."
            );
        }
    }

    // --------------------------------------------------------
    // CYCLE LENGTH
    // --------------------------------------------------------

    if (
        trend.cycle_length &&
        trend.cycle_length.change !== null &&
        trend.cycle_length.change !== undefined
    ) {

        if (
            trend.cycle_length.change > 0
        ) {

            items.push(
                "Your cycle length has increased."
            );

        } else if (
            trend.cycle_length.change < 0
        ) {

            items.push(
                "Your cycle length has decreased."
            );

        } else {

            items.push(
                "Your cycle length is unchanged."
            );
        }
    }

    // --------------------------------------------------------
    // NO SUMMARY
    // --------------------------------------------------------

    if (items.length === 0) {

        return `

            <p>
                Continue recording your cycles
                to identify meaningful changes.
            </p>

        `;

    }

    return `

        <ul>

            ${
                items
                    .map(
                        item =>
                            `<li>${item}</li>`
                    )
                    .join("")
            }

        </ul>

    `;
}

// ============================================================
// CHECK VALUE
// ============================================================

function hasValue(value) {

    return !(
        value === null ||
        value === undefined ||
        value === ""
    );

}

// ============================================================
// DISPLAY NULL VALUES
// ============================================================

function displayValue(value) {

    if (!hasValue(value)) {

        return "Not entered";

    }

    return value;

}

// ============================================================
// FORMAT SCORE
// ============================================================

function formatScore(value) {

    if (!hasValue(value)) {

        return "Not entered";

    }

    const number =
        Number(value);

    if (Number.isNaN(number)) {

        return displayValue(value);

    }

    return `${formatNumber(number)}/10`;

}

// ============================================================
// FORMAT OPTIONAL NUMBER
// ============================================================

function formatOptionalNumber(value) {

    if (!hasValue(value)) {

        return "Not entered";

    }

    const number =
        Number(value);

    if (Number.isNaN(number)) {

        return displayValue(value);

    }

    return formatNumber(number);

}

// ============================================================
// FORMAT PREPARED VALUE
// ============================================================

function formatPrepared(value) {

    if (!hasValue(value)) {

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

    return displayValue(value);

}

// ============================================================
// FORMAT NUMBER
// ============================================================

function formatNumber(value) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(
            Number(value)
        )
    ) {

        return "N/A";

    }

    const number =
        Number(value);

    if (
        Number.isInteger(number)
    ) {

        return String(number);

    }

    return number.toFixed(1);

}

// ============================================================
// FORMAT DATE
// ============================================================

function formatDate(dateString) {

    if (!dateString) {

        return "Not entered";

    }

    const date =
        new Date(dateString);

    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return "Not entered";

    }

    return date.toLocaleDateString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );

}

// ============================================================
// NAVIGATION
// ============================================================

function goPeriod() {

    window.location.href =
        "period.html";

}

function goDashboard() {

    window.location.href =
        "dashboard.html";

}

// ============================================================
// START
// ============================================================

loadHistory();