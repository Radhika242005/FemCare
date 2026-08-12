const API = "https://femcare-production-2b2d.up.railway.app";

console.log("🔥 FEMCARE RECOMMENDATIONS.JS LOADED 🔥");

const message =
    document.getElementById("message");

const progressCard =
    document.getElementById("progressCard");

const completedCount =
    document.getElementById("completedCount");

const remainingCount =
    document.getElementById("remainingCount");

const totalCount =
    document.getElementById("totalCount");

const progressBar =
    document.getElementById("progressBar");

const progressPercent =
    document.getElementById("progressPercent");

const streakNumber =
    document.getElementById("streakNumber");

const completedList =
    document.getElementById("completedList");

const healthCard =
    document.getElementById("healthCard");

const healthContainer =
    document.getElementById("healthContainer");

const problemCard =
    document.getElementById("problemCard");

const problemContainer =
    document.getElementById("problemContainer");

const recommendationCard =
    document.getElementById("recommendationCard");

const recommendationContainer =
    document.getElementById("recommendationContainer");

let userId = null;

let completedRecommendationIds =
    new Set();

let currentRecommendations = [];

let players = {};

let completingRecommendations =
    new Set();


// ============================================================
// ADD PAGE STYLES
// ============================================================

function addRecommendationStyles() {

    if (
        document.getElementById(
            "femcareRecommendationStyles"
        )
    ) {
        return;
    }

    const style =
        document.createElement("style");

    style.id =
        "femcareRecommendationStyles";

    style.textContent = `

        .health-grid {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(150px, 1fr));
            gap: 14px;
            margin-top: 15px;
        }

        .health-item {
            background: #faf6fc;
            border: 1px solid #eadcf0;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }

        .health-label {
            display: block;
            color: #806b88;
            font-size: 12px;
            margin-bottom: 7px;
        }

        .health-value {
            display: block;
            color: #4d285d;
            font-size: 18px;
            font-weight: 700;
        }

        .health-date {
            grid-column: 1 / -1;
            background: #f7effa;
            color: #7542a2;
            text-align: center;
            font-weight: 700;
        }

        .problem-list {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
        }

        .problem {
            background: #fff7fb;
            border: 1px solid #f0d8e8;
            color: #71395e;
            border-radius: 10px;
            padding: 12px 15px;
            font-size: 13px;
            font-weight: 600;
        }

        .pcos-reference-grid {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(180px, 1fr));
            gap: 14px;
            margin-top: 20px;
        }

        .pcos-reference-item {
            padding: 20px;
            text-align: center;
            background: #faf6fc;
            border: 1px solid #eadcf0;
            border-radius: 13px;
        }

        .pcos-reference-number {
            display: block;
            margin-bottom: 7px;
            color: #7542a2;
            font-size: 28px;
            font-weight: 700;
        }

        .pcos-reference-label {
            color: #756d79;
            font-size: 12px;
            line-height: 1.5;
        }

        .pcos-problems {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 18px;
        }

        .pcos-problem-tag {
            padding: 8px 12px;
            border-radius: 20px;
            background: #fff1f8;
            border: 1px solid #f0d8e8;
            color: #71395e;
            font-size: 11px;
            font-weight: 700;
        }

        .medical-notice {
            margin-top: 18px;
            padding: 14px 16px;
            border: 1px solid #eadfbc;
            border-radius: 10px;
            background: #fffaf0;
            color: #655a42;
            font-size: 12px;
            line-height: 1.6;
        }

        .recommendation-grid {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(290px, 1fr));
            gap: 24px;
            align-items: start;
        }

        .recommendation {
            width: 100%;
            min-width: 0;
            overflow: hidden;
            background: #ffffff;
            border: 1px solid #eadcf0;
            border-radius: 18px;
            padding: 20px;
            box-shadow:
                0 8px 24px rgba(75, 43, 88, 0.08);
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        .recommendation:hover {
            transform: translateY(-3px);
            box-shadow:
                0 12px 30px rgba(75, 43, 88, 0.13);
        }

        .recommendation h3 {
            margin: 0 0 10px;
            color: #4b2b58;
            font-size: 21px;
            line-height: 1.3;
        }

        .recommendation .type {
            display: inline-block;
            padding: 6px 12px;
            margin-bottom: 12px;
            border-radius: 20px;
            background: #f0e3f7;
            color: #714486;
            font-size: 11px;
            font-weight: 700;
        }

        .recommendation .problem-name {
            margin-bottom: 10px;
            color: #9a5c8e;
            font-size: 13px;
            font-weight: 700;
        }

        .recommendation .description {
            min-height: 55px;
            margin-bottom: 16px;
            color: #6f6872;
            font-size: 14px;
            line-height: 1.6;
        }

        .video-container {
            position: relative;
            width: 100%;
            aspect-ratio: 16 / 9;
            margin-top: 12px;
            overflow: hidden;
            border-radius: 13px;
            background: #eee;
        }

        .video-container iframe {
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            border: 0 !important;
            border-radius: 13px;
        }

        .watch-message {
            margin-top: 10px;
            color: #777;
            font-size: 11px;
            line-height: 1.5;
        }

        .complete-button {
            width: 100%;
            margin-top: 14px;
            padding: 12px 15px;
            border: none;
            border-radius: 10px;
            background:
                linear-gradient(
                    90deg,
                    #7542a2,
                    #d94aa0
                );
            color: white;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition:
                transform 0.15s ease,
                opacity 0.15s ease;
        }

        .complete-button:hover {
            transform: translateY(-1px);
            opacity: 0.94;
        }

        .complete-button:disabled {
            cursor: default;
            opacity: 0.75;
            transform: none;
        }

        .complete-button.completed {
            background: #e6f5eb;
            color: #287a45;
            border: 1px solid #c7e8d1;
        }

        .completed-list {
            margin-top: 18px;
        }

        .completed-title {
            margin-bottom: 10px;
            color: #4b2b58;
            font-weight: 700;
        }

        .completed-item {
            display: inline-block;
            margin: 4px 6px 4px 0;
            padding: 7px 12px;
            border-radius: 20px;
            background: #e9f7ee;
            color: #287a45;
            font-size: 11px;
            font-weight: 600;
        }

        .empty {
            padding: 30px;
            text-align: center;
            border: 1px dashed #dbc9e2;
            border-radius: 14px;
            background: #fcf9fd;
            color: #756d79;
        }

        @media (max-width: 700px) {

            .recommendation-grid {
                grid-template-columns: 1fr;
            }

            .recommendation {
                padding: 16px;
            }

            .recommendation h3 {
                font-size: 19px;
            }

        }

    `;

    document.head.appendChild(style);
}


// ============================================================
// GET USER ID
// ============================================================

function getUserId() {

    const storedUser =
        localStorage.getItem("user");

    if (!storedUser) {

        if (message) {

            message.textContent =
                "User session not found.";

        }

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

        return null;
    }
}


userId = getUserId();


// ============================================================
// HELPERS
// ============================================================

function hasValue(value) {

    return !(
        value === null ||
        value === undefined ||
        value === ""
    );
}


function displayValue(value) {

    if (!hasValue(value)) {

        return "Not available";

    }

    return value;
}


function formatNumber(value) {

    if (!hasValue(value)) {

        return "0";

    }

    const number =
        Number(value);

    if (Number.isNaN(number)) {

        return value;

    }

    if (Number.isInteger(number)) {

        return String(number);

    }

    return number.toFixed(1);
}


function formatDate(value) {

    if (!value) {

        return "Not available";

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
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );
}


// ============================================================
// FIND LATEST HEALTH LOG
// ============================================================

function findLatestHealthLog(data) {

    if (!data) {

        return null;

    }

    if (data.latest_health_log) {

        return data.latest_health_log;

    }

    if (data.latest_log) {

        return data.latest_log;

    }

    if (data.health_log) {

        return data.health_log;

    }

    if (data.health_data) {

        return data.health_data;

    }

    if (
        Array.isArray(data.health_logs) &&
        data.health_logs.length > 0
    ) {

        return data.health_logs[0];

    }

    if (
        Array.isArray(data.logs) &&
        data.logs.length > 0
    ) {

        return data.logs[0];

    }

    return null;
}


// ============================================================
// LOAD COMPLETED RECOMMENDATIONS
// ============================================================

async function loadCompletedRecommendations() {

    if (!userId) {

        return;

    }

    try {

        const response =
            await fetch(
                `${API}/api/recommendations/completed/${userId}`
            );

        const data =
            await response.json();

        console.log(
            "Completed recommendations:",
            data
        );

        if (!response.ok) {

            throw new Error(
                data.message ||
                `Completed API returned ${response.status}`
            );

        }

        if (
            data.success &&
            Array.isArray(
                data.completed_recommendation_ids
            )
        ) {

            completedRecommendationIds =
                new Set(
                    data.completed_recommendation_ids
                        .map(Number)
                );

        } else {

            completedRecommendationIds =
                new Set();

        }

    } catch (error) {

        console.error(
            "COMPLETED LOAD ERROR:",
            error
        );

        completedRecommendationIds =
            new Set();

    }
}


// ============================================================
// LOAD STREAK
// ============================================================

async function loadStreak() {

    if (!userId) {

        return;

    }

    try {

        const response =
            await fetch(
                `${API}/api/recommendations/streak/${userId}`
            );

        const data =
            await response.json();

        console.log(
            "Streak response:",
            data
        );

        if (
            response.ok &&
            data.success &&
            streakNumber
        ) {

            streakNumber.textContent =
                data.streak || 0;

        }

    } catch (error) {

        console.error(
            "STREAK ERROR:",
            error
        );

        if (streakNumber) {

            streakNumber.textContent =
                "0";

        }

    }
}


// ============================================================
// UPDATE PROGRESS
// ============================================================

function updateProgress() {

    const total =
        currentRecommendations.length;

    const completed =
        currentRecommendations.filter(
            recommendation =>
                completedRecommendationIds.has(
                    Number(recommendation.id)
                )
        ).length;

    const remaining =
        Math.max(
            total - completed,
            0
        );

    const percentage =
        total > 0
            ? Math.round(
                (completed / total) * 100
            )
            : 0;

    if (completedCount) {

        completedCount.textContent =
            completed;

    }

    if (remainingCount) {

        remainingCount.textContent =
            remaining;

    }

    if (totalCount) {

        totalCount.textContent =
            total;

    }

    if (progressBar) {

        progressBar.style.width =
            `${percentage}%`;

    }

    if (progressPercent) {

        progressPercent.textContent =
            `${percentage}% Complete`;

    }

    if (completedList) {

        completedList.innerHTML = "";

        const completed =
            currentRecommendations.filter(
                recommendation =>
                    completedRecommendationIds.has(
                        Number(recommendation.id)
                    )
            );

        if (completed.length > 0) {

            const title =
                document.createElement("div");

            title.className =
                "completed-title";

            title.textContent =
                "✓ Completed Practices";

            completedList.appendChild(
                title
            );

            completed.forEach(
                recommendation => {

                    const item =
                        document.createElement(
                            "div"
                        );

                    item.className =
                        "completed-item";

                    item.textContent =
                        `✓ ${recommendation.practice_name}`;

                    completedList.appendChild(
                        item
                    );

                }
            );

        }

    }

    if (progressCard) {

        progressCard.style.display =
            "block";

    }
}


// ============================================================
// YOUTUBE VIDEO ID
// ============================================================

function getYouTubeVideoId(url) {

    if (!url) {

        return null;

    }

    let cleanUrl =
        String(url).trim();

    const markdownMatch =
        cleanUrl.match(
            /^\[.*?\]\((.*?)\)$/
        );

    if (markdownMatch) {

        cleanUrl =
            markdownMatch[1];

    }

    try {

        const parsed =
            new URL(cleanUrl);

        const host =
            parsed.hostname
                .toLowerCase()
                .replace("www.", "");

        if (host === "youtube.com") {

            if (
                parsed.pathname ===
                "/watch"
            ) {

                return parsed.searchParams.get(
                    "v"
                );

            }

            if (
                parsed.pathname.startsWith(
                    "/embed/"
                )
            ) {

                return parsed.pathname
                    .split("/embed/")[1]
                    .split("/")[0];

            }

            if (
                parsed.pathname.startsWith(
                    "/shorts/"
                )
            ) {

                return parsed.pathname
                    .split("/shorts/")[1]
                    .split("/")[0];

            }

        }

        if (host === "youtu.be") {

            return parsed.pathname
                .substring(1)
                .split("/")[0];

        }

    } catch (error) {

        console.error(
            "YouTube URL error:",
            error
        );

    }

    return null;
}


// ============================================================
// LOAD YOUTUBE API
// ============================================================

function loadYouTubeAPI() {

    return new Promise(
        resolve => {

            if (
                window.YT &&
                window.YT.Player
            ) {

                resolve();

                return;

            }

            const existing =
                document.getElementById(
                    "youtube-api-script"
                );

            if (existing) {

                const oldReady =
                    window.onYouTubeIframeAPIReady;

                window.onYouTubeIframeAPIReady =
                    function() {

                        if (oldReady) {

                            oldReady();

                        }

                        resolve();

                    };

                return;

            }

            const script =
                document.createElement(
                    "script"
                );

            script.id =
                "youtube-api-script";

            script.src =
                "https://www.youtube.com/iframe_api";

            window.onYouTubeIframeAPIReady =
                function() {

                    resolve();

                };

            document.head.appendChild(
                script
            );

            setTimeout(
                resolve,
                8000
            );

        }
    );

}


// ============================================================
// CREATE YOUTUBE PLAYER
// ============================================================

function createYouTubePlayer(
    elementId,
    videoId,
    recommendationId,
    button
) {

    if (
        !videoId ||
        !window.YT ||
        !window.YT.Player
    ) {

        return;

    }

    if (players[recommendationId]) {

        try {

            players[
                recommendationId
            ].destroy();

        } catch (error) {

            console.error(
                "Player destroy error:",
                error
            );

        }

    }

    players[recommendationId] =
        new YT.Player(
            elementId,
            {

                videoId:
                    videoId,

                playerVars: {

                    rel: 0,

                    modestbranding: 1,

                    playsinline: 1,

                    enablejsapi: 1

                },

                events: {

                    onReady:
                        function(event) {

                            console.log(
                                "YouTube player ready:",
                                recommendationId
                            );

                        },

                    onStateChange:
                        function(event) {

                            if (
                                event.data ===
                                YT.PlayerState.ENDED
                            ) {

                                console.log(
                                    "🔥 VIDEO COMPLETED:",
                                    recommendationId
                                );

                                autoCompleteRecommendation(
                                    recommendationId,
                                    button
                                );

                            }

                        },

                    onError:
                        function(event) {

                            console.error(
                                "YouTube player error:",
                                recommendationId,
                                event.data
                            );

                        }

                }

            }
        );

}


// ============================================================
// AUTO COMPLETE VIDEO
// ============================================================

async function autoCompleteRecommendation(
    recommendationId,
    button
) {

    if (!userId) {

        return;

    }

    recommendationId =
        Number(recommendationId);

    if (
        completedRecommendationIds.has(
            recommendationId
        )
    ) {

        updateButtonToCompleted(
            button
        );

        updateProgress();

        return;

    }

    if (
        completingRecommendations.has(
            recommendationId
        )
    ) {

        return;

    }

    completingRecommendations.add(
        recommendationId
    );

    if (button) {

        button.disabled =
            true;

        button.textContent =
            "Saving completion...";

    }

    try {

        const response =
            await fetch(
                `${API}/api/recommendations/complete`,
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
                                Number(userId),

                            recommendation_id:
                                recommendationId

                        })

                }
            );

        const data =
            await response.json();

        console.log(
            "AUTO COMPLETE RESPONSE:",
            data
        );

        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.message ||
                "Unable to save completion."
            );

        }

        completedRecommendationIds.add(
            recommendationId
        );

        updateButtonToCompleted(
            button
        );

        updateProgress();

        await loadStreak();

    } catch (error) {

        console.error(
            "AUTO COMPLETION ERROR:",
            error
        );

        if (button) {

            button.disabled =
                false;

            button.textContent =
                "✓ Mark as Completed";

        }

        alert(
            "The video finished, but FemCare could not save the completion."
        );

    } finally {

        completingRecommendations.delete(
            recommendationId
        );

    }
}


// ============================================================
// BUTTON STATES
// ============================================================

function updateButtonToCompleted(button) {

    if (!button) {

        return;

    }

    button.disabled =
        false;

    button.textContent =
        "✓ Completed";

    button.classList.add(
        "completed"
    );

}


function updateButtonToIncomplete(button) {

    if (!button) {

        return;

    }

    button.disabled =
        false;

    button.textContent =
        "✓ Mark as Completed";

    button.classList.remove(
        "completed"
    );

}


// ============================================================
// TOGGLE COMPLETION
// ============================================================

async function toggleCompletion(
    recommendationId,
    button
) {

    if (!userId) {

        alert(
            "User session not found."
        );

        return;

    }

    recommendationId =
        Number(recommendationId);

    const currentlyCompleted =
        completedRecommendationIds.has(
            recommendationId
        );

    if (button) {

        button.disabled =
            true;

    }

    try {

        if (currentlyCompleted) {

            const response =
                await fetch(
                    `${API}/api/recommendations/complete`,
                    {

                        method:
                            "DELETE",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify({

                                user_id:
                                    Number(userId),

                                recommendation_id:
                                    recommendationId

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
                    "Unable to remove completion."
                );

            }

            completedRecommendationIds.delete(
                recommendationId
            );

            updateButtonToIncomplete(
                button
            );

        } else {

            const response =
                await fetch(
                    `${API}/api/recommendations/complete`,
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
                                    Number(userId),

                                recommendation_id:
                                    recommendationId

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
                    "Unable to mark recommendation as completed."
                );

            }

            completedRecommendationIds.add(
                recommendationId
            );

            updateButtonToCompleted(
                button
            );

        }

        updateProgress();

        await loadStreak();

    } catch (error) {

        console.error(
            "COMPLETION ERROR:",
            error
        );

        alert(
            error.message ||
            "Unable to update completion."
        );

    } finally {

        if (
            completedRecommendationIds.has(
                recommendationId
            )
        ) {

            updateButtonToCompleted(
                button
            );

        } else if (button) {

            updateButtonToIncomplete(
                button
            );

        }

    }

}


// ============================================================
// DISPLAY HEALTH LOG
// ============================================================

function displayHealthLog(log) {

    if (!healthContainer) {

        return;

    }

    if (!log) {

        healthContainer.innerHTML = `

            <div class="empty">

                <h3>
                    No Health Log Available
                </h3>

                <p>
                    Record your health information
                    to receive personalized recommendations.
                </p>

            </div>

        `;

        if (healthCard) {

            healthCard.style.display =
                "block";

        }

        return;

    }

    const sleep =
        log.sleep_hours ??
        log.sleep ??
        log.average_sleep;

    const water =
        log.water_intake_liters ??
        log.water_intake ??
        log.water;

    const stress =
        log.stress_score ??
        log.stress;

    const exercise =
        log.exercise_minutes ??
        log.exercise;

    const date =
        log.log_date ??
        log.date ??
        log.created_at;

    healthContainer.innerHTML = `

        <div class="health-grid">

            <div class="health-item health-date">

                📅 Recorded:
                ${formatDate(date)}

            </div>


            <div class="health-item">

                <span class="health-label">
                    😴 Sleep
                </span>

                <span class="health-value">
                    ${displayValue(sleep)}
                    hrs
                </span>

            </div>


            <div class="health-item">

                <span class="health-label">
                    💧 Water
                </span>

                <span class="health-value">
                    ${displayValue(water)}
                    L
                </span>

            </div>


            <div class="health-item">

                <span class="health-label">
                    🧘 Stress
                </span>

                <span class="health-value">
                    ${displayValue(stress)}
                    /10
                </span>

            </div>


            <div class="health-item">

                <span class="health-label">
                    🏃 Exercise
                </span>

                <span class="health-value">
                    ${displayValue(exercise)}
                    min
                </span>

            </div>

        </div>

    `;

    if (healthCard) {

        healthCard.style.display =
            "block";

    }

}


// ============================================================
// DISPLAY PCOS REFERENCE ANALYSIS
// ============================================================

function displayPCOSReference(data) {

    const card =
        document.getElementById(
            "pcosReferenceCard"
        );

    const container =
        document.getElementById(
            "pcosReferenceContainer"
        );

    const notice =
        document.getElementById(
            "medicalNotice"
        );

    if (!card || !container) {

        console.warn(
            "PCOS reference HTML elements not found."
        );

        return;

    }

    const reference =
        data.pcos_reference || {};

    const positive =
        reference.pcos_positive ??
        0;

    const negative =
        reference.pcos_negative ??
        0;

    const percentage =
        reference.positive_percentage ??
        0;

    const similarRecords =
        reference.similar_records ??
        0;

    container.innerHTML = `

        <div class="pcos-reference-item">

            <span class="pcos-reference-number">
                ${positive}
            </span>

            <span class="pcos-reference-label">
                PCOS Positive Reference Records
            </span>

        </div>


        <div class="pcos-reference-item">

            <span class="pcos-reference-number">
                ${negative}
            </span>

            <span class="pcos-reference-label">
                PCOS Negative Reference Records
            </span>

        </div>


        <div class="pcos-reference-item">

            <span class="pcos-reference-number">
                ${percentage}%
            </span>

            <span class="pcos-reference-label">
                Positive Reference Percentage
            </span>

        </div>


        <div class="pcos-reference-item">

            <span class="pcos-reference-number">
                ${similarRecords}
            </span>

            <span class="pcos-reference-label">
                Similar Dataset Records
            </span>

        </div>

    `;


    const pcosProblems =
        Array.isArray(
            data.pcos_problems
        )
            ? data.pcos_problems
            : [];


    if (
        pcosProblems.length > 0
    ) {

        const problemsContainer =
            document.createElement(
                "div"
            );

        problemsContainer.className =
            "pcos-problems";


        pcosProblems.forEach(
            problem => {

                const tag =
                    document.createElement(
                        "span"
                    );

                tag.className =
                    "pcos-problem-tag";

                tag.textContent =
                    problem;

                problemsContainer.appendChild(
                    tag
                );

            }
        );


        container.appendChild(
            problemsContainer
        );

    }


    if (notice) {

        notice.textContent =
            data.medical_notice ||
            "PCOS-related information is based on reference dataset patterns and is not a medical diagnosis.";

    }


    card.style.display =
        "block";
}


// ============================================================
// DISPLAY PROBLEMS
// ============================================================

function displayProblems(problems) {

    if (
        !problemCard ||
        !problemContainer
    ) {

        return;

    }

    if (
        !Array.isArray(problems) ||
        problems.length === 0
    ) {

        problemCard.style.display =
            "none";

        return;

    }

    problemContainer.innerHTML =
        "";

    problems.forEach(
        problem => {

            const element =
                document.createElement(
                    "div"
                );

            element.className =
                "problem";

            element.textContent =
                problem;

            problemContainer.appendChild(
                element
            );

        }
    );

    problemCard.style.display =
        "block";
}


// ============================================================
// CREATE RECOMMENDATION CARD
// ============================================================

function createRecommendationCard(
    recommendation
) {

    const card =
        document.createElement(
            "div"
        );

    card.className =
        "recommendation";


    const title =
        document.createElement(
            "h3"
        );

    title.textContent =
        recommendation.practice_name ||
        recommendation.title ||
        "Recommended Practice";

    card.appendChild(
        title
    );


    const type =
        document.createElement(
            "div"
        );

    type.className =
        "type";

    type.textContent =
        recommendation.practice_type ||
        recommendation.type ||
        "Wellness";

    card.appendChild(
        type
    );


    const problem =
        document.createElement(
            "div"
        );

    problem.className =
        "problem-name";

    problem.textContent =
        `For: ${
            recommendation.problem ||
            "General Wellness"
        }`;

    card.appendChild(
        problem
    );


    const description =
        document.createElement(
            "div"
        );

    description.className =
        "description";

    description.textContent =
        recommendation.description ||
        "Follow this practice as part of your wellness routine.";

    card.appendChild(
        description
    );


    const videoUrl =
        recommendation.video_url ||
        recommendation.video ||
        recommendation.youtube_url;


    const videoId =
        getYouTubeVideoId(
            videoUrl
        );


    const recommendationId =
        Number(
            recommendation.id ||
            recommendation.recommendation_id
        );


    if (videoId) {

        const videoContainer =
            document.createElement(
                "div"
            );

        videoContainer.className =
            "video-container";


        const playerId =
            `youtube-player-${recommendationId}`;


        const player =
            document.createElement(
                "div"
            );

        player.id =
            playerId;


        videoContainer.appendChild(
            player
        );


        card.appendChild(
            videoContainer
        );


        const watchMessage =
            document.createElement(
                "div"
            );

        watchMessage.className =
            "watch-message";

        watchMessage.textContent =
            "▶ Watch the video until the end. FemCare will automatically mark it as completed.";

        card.appendChild(
            watchMessage
        );


        const completionButton =
            createCompletionButton(
                recommendationId
            );

        card.appendChild(
            completionButton
        );


        setTimeout(
            function() {

                createYouTubePlayer(
                    playerId,
                    videoId,
                    recommendationId,
                    completionButton
                );

            },
            500
        );

    } else {

        const noVideo =
            document.createElement(
                "div"
            );

        noVideo.className =
            "watch-message";

        noVideo.textContent =
            "No video is available for this recommendation.";

        card.appendChild(
            noVideo
        );


        const completionButton =
            createCompletionButton(
                recommendationId
            );

        card.appendChild(
            completionButton
        );

    }


    return card;
}


// ============================================================
// CREATE COMPLETION BUTTON
// ============================================================

function createCompletionButton(
    recommendationId
) {

    const button =
        document.createElement(
            "button"
        );

    button.className =
        "complete-button";


    if (
        completedRecommendationIds.has(
            recommendationId
        )
    ) {

        updateButtonToCompleted(
            button
        );

    } else {

        button.textContent =
            "✓ Mark as Completed";

    }


    button.addEventListener(
        "click",
        function() {

            toggleCompletion(
                recommendationId,
                button
            );

        }
    );


    return button;
}


// ============================================================
// LOAD RECOMMENDATIONS
// ============================================================

async function loadRecommendations() {

    if (!userId) {

        return;

    }

    try {

        if (message) {

            message.textContent =
                "Loading your personalized recommendations...";

        }


        console.log(
            "Loading recommendations for user:",
            userId
        );


        const response =
            await fetch(
                `${API}/api/recommendations/user/${userId}`
            );


        const data =
            await response.json();


        console.log(
            "RECOMMENDATION API RESPONSE:",
            data
        );


        if (!response.ok) {

            throw new Error(
                data.message ||
                `Recommendation API returned ${response.status}`
            );

        }


        if (
            data.success === false
        ) {

            throw new Error(
                data.message ||
                "Recommendation API failed."
            );

        }


        if (message) {

            message.textContent =
                "";

        }


        // ====================================================
        // HEALTH LOG
        // ====================================================

        const latestLog =
            findLatestHealthLog(
                data
            );


        displayHealthLog(
            latestLog
        );


        // ====================================================
        // PCOS REFERENCE ANALYSIS
        // ====================================================

        displayPCOSReference(
            data
        );


        // ====================================================
        // PROBLEMS
        // ====================================================

        const problems =
            Array.isArray(
                data.problems
            )
                ? data.problems
                : [];


        displayProblems(
            problems
        );


        // ====================================================
        // RECOMMENDATIONS
        // ====================================================

        const recommendations =
            Array.isArray(
                data.recommendations
            )
                ? data.recommendations
                : [];


        currentRecommendations =
            recommendations;


        updateProgress();


        if (
            !recommendationContainer
        ) {

            return;

        }


        recommendationContainer.innerHTML =
            "";


        if (
            recommendations.length === 0
        ) {

            recommendationContainer.innerHTML = `

                <div class="empty">

                    <h3>
                        🌿 No Recommendations Yet
                    </h3>

                    <p>
                        Record your health information
                        to receive personalized wellness
                        recommendations.
                    </p>

                </div>

            `;


            if (
                recommendationCard
            ) {

                recommendationCard.style.display =
                    "block";

            }


            return;

        }


        await loadYouTubeAPI();


        const grid =
            document.createElement(
                "div"
            );


        grid.className =
            "recommendation-grid";


        recommendations.forEach(
            recommendation => {

                const card =
                    createRecommendationCard(
                        recommendation
                    );


                grid.appendChild(
                    card
                );

            }
        );


        recommendationContainer.appendChild(
            grid
        );


        if (
            recommendationCard
        ) {

            recommendationCard.style.display =
                "block";

        }


        updateProgress();


        await loadStreak();


    } catch (error) {

        console.error(
            "RECOMMENDATION ERROR:",
            error
        );


        if (message) {

            message.textContent =
                "Unable to load recommendations.";

        }


        if (
            recommendationContainer
        ) {

            recommendationContainer.innerHTML = `

                <div class="empty">

                    <h3>
                        Unable to Load Recommendations
                    </h3>

                    <p>
                        ${error.message}
                    </p>

                    <p>
                        Please make sure the FemCare
                        server is running.
                    </p>

                </div>

            `;

        }


        if (
            recommendationCard
        ) {

            recommendationCard.style.display =
                "block";

        }

    }

}


// ============================================================
// NAVIGATION
// ============================================================

function goTrends() {

    window.location.href =
        "trends.html";

}


function goHealthTrends() {

    window.location.href =
        "trends.html";

}


function goDashboard() {

    window.location.href =
        "dashboard.html";

}


// ============================================================
// START
// ============================================================

async function startPage() {

    addRecommendationStyles();


    if (!userId) {

        if (message) {

            message.textContent =
                "Please login to view recommendations.";

        }

        return;

    }


    await loadCompletedRecommendations();


    await loadRecommendations();


    await loadStreak();

}


startPage();