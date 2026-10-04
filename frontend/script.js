const API_URL = "http://127.0.0.1:8000/ask";
const EVALUATION_API_URL = "http://127.0.0.1:8000/evaluation";


document.addEventListener("DOMContentLoaded", () => {

    const questionInput =
        document.getElementById("questionInput");

    const askButton =
        document.getElementById("askButton");

    const loading =
        document.getElementById("loading");

    const loadingStatus =
        document.getElementById("loadingStatus");

    const loadingStep1 =
        document.getElementById("loadingStep1");

    const loadingStep2 =
        document.getElementById("loadingStep2");

    const loadingStep3 =
        document.getElementById("loadingStep3");

    const loadingStep4 =
        document.getElementById("loadingStep4");

    const resultSection =
        document.getElementById("resultSection");

    const emptyState =
        document.getElementById("emptyState");

    const answerElement =
        document.getElementById("answer");

    const copyButton =
        document.getElementById("copyButton");

    const sourcesContainer =
        document.getElementById("sources");

    const responseTime =
        document.getElementById("responseTime");

    const sourcesRetrieved =
        document.getElementById("sourcesRetrieved");

    const finalResults =
        document.getElementById("finalResults");

    const modelName =
        document.getElementById("modelName");

    const precisionScore =
        document.getElementById("precisionScore");

    const recallScore =
        document.getElementById("recallScore");

    const mrrScore =
        document.getElementById("mrrScore");

    const retrievalAccuracy =
        document.getElementById("retrievalAccuracy");


    if (!questionInput || !askButton) {

        console.error(
            "GitContext-AI: Required HTML elements not found."
        );

        return;
    }


    function updateLoadingStep(
        stepNumber,
        message
    ) {

        if (loadingStatus) {

            loadingStatus.textContent =
                message;
        }


        const steps = [
            loadingStep1,
            loadingStep2,
            loadingStep3,
            loadingStep4
        ];


        steps.forEach(
            (step, index) => {

                if (!step) {
                    return;
                }


                const icon =
                    step.querySelector(
                        ".step-check"
                    );


                if (index < stepNumber) {

                    step.classList.add(
                        "completed"
                    );

                    step.classList.remove(
                        "active"
                    );


                    if (icon) {

                        icon.textContent =
                            "✓";
                    }

                }

                else if (
                    index === stepNumber
                ) {

                    step.classList.add(
                        "active"
                    );

                    step.classList.remove(
                        "completed"
                    );


                    if (icon) {

                        icon.textContent =
                            "●";
                    }

                }

                else {

                    step.classList.remove(
                        "active"
                    );

                    step.classList.remove(
                        "completed"
                    );


                    if (icon) {

                        icon.textContent =
                            "○";
                    }
                }
            }
        );
    }


    async function askGitContext() {

        const question =
            questionInput.value.trim();


        if (!question) {

            questionInput.focus();

            return;
        }


        loading.classList.remove(
            "hidden"
        );

        resultSection.classList.add(
            "hidden"
        );

        emptyState.classList.add(
            "hidden"
        );


        askButton.disabled = true;


        askButton.innerHTML = `
            <span>Analyzing...</span>
            <span class="arrow">◌</span>
        `;


        updateLoadingStep(
            0,
            "Searching your repository..."
        );


        try {

            console.log(
                "Sending question:",
                question
            );


            await delay(300);


            updateLoadingStep(
                1,
                "Finding the most relevant code..."
            );


            await delay(300);


            const response =
                await fetch(
                    API_URL,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            question: question
                        })
                    }
                );


            console.log(
                "API response status:",
                response.status
            );


            if (!response.ok) {

                let errorMessage =
                    "Unable to process your request.";


                try {

                    const errorData =
                        await response.json();


                    if (
                        errorData.detail &&
                        typeof errorData.detail ===
                        "object"
                    ) {

                        errorMessage =
                            errorData.detail.message ||
                            errorMessage;
                    }

                    else if (
                        typeof errorData.detail ===
                        "string"
                    ) {

                        errorMessage =
                            errorData.detail;
                    }

                }

                catch (error) {

                    console.log(
                        "Could not parse error response."
                    );
                }


                throw new Error(
                    errorMessage
                );
            }


            updateLoadingStep(
                2,
                "Reranking code for relevance..."
            );


            await delay(300);


            const data =
                await response.json();


            console.log(
                "API response:",
                data
            );


            updateLoadingStep(
                3,
                "Generating your Gemini answer..."
            );


            await delay(300);


            /* =========================================
               AI ANSWER
               ========================================= */

            if (
                typeof marked !== "undefined"
            ) {

                answerElement.innerHTML =
                    marked.parse(
                        data.answer ||
                        "No answer generated."
                    );

            }

            else {

                answerElement.textContent =
                    data.answer ||
                    "No answer generated.";
            }


            /* =========================================
               SOURCE CITATIONS
               ========================================= */

            renderSources(
                data.sources || []
            );


            /* =========================================
               QUERY INSIGHTS
               ========================================= */

            renderMetrics(
                data.metrics
            );


            /* =========================================
               RETRIEVAL QUALITY
               ========================================= */

            await loadEvaluationMetrics();


            updateLoadingStep(
                4,
                "Answer generated successfully!"
            );


            await delay(400);


            loading.classList.add(
                "hidden"
            );


            resultSection.classList.remove(
                "hidden"
            );


            resultSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

        catch (error) {

            console.error(
                "GitContext-AI Error:",
                error
            );


            loading.classList.add(
                "hidden"
            );


            resultSection.classList.remove(
                "hidden"
            );


            answerElement.textContent =
                "⚠️ " +
                (
                    error.message ||
                    "Unable to connect to GitContext-AI backend."
                );


            renderSources([]);


            renderMetrics(null);


            renderEvaluationMetrics(null);

        }

        finally {

            askButton.disabled = false;


            askButton.innerHTML = `
                <span>Ask GitContext</span>
                <span class="arrow">→</span>
            `;
        }
    }


    /* =========================================
       QUERY METRICS
       ========================================= */

    function renderMetrics(metrics) {

        if (!metrics) {

            if (responseTime) {
                responseTime.textContent = "--";
            }

            if (sourcesRetrieved) {
                sourcesRetrieved.textContent = "--";
            }

            if (finalResults) {
                finalResults.textContent = "--";
            }

            if (modelName) {
                modelName.textContent = "--";
            }

            return;
        }


        if (responseTime) {

            const seconds =
                Number(
                    metrics.response_time_seconds
                );


            if (!Number.isNaN(seconds)) {

                responseTime.textContent =
                    `${seconds.toFixed(2)}s`;

            }

            else {

                responseTime.textContent =
                    "--";
            }
        }


        if (sourcesRetrieved) {

            sourcesRetrieved.textContent =
                metrics.sources_retrieved ??
                "--";
        }


        if (finalResults) {

            finalResults.textContent =
                metrics.final_results ??
                "--";
        }


        if (modelName) {

            modelName.textContent =
                formatModelName(
                    metrics.model
                );
        }
    }


    /* =========================================
       RETRIEVAL EVALUATION API
       ========================================= */

    async function loadEvaluationMetrics() {

        try {

            console.log(
                "Loading retrieval evaluation..."
            );


            const response =
                await fetch(
                    EVALUATION_API_URL
                );


            if (!response.ok) {

                throw new Error(
                    "Evaluation API failed."
                );
            }


            const data =
                await response.json();


            console.log(
                "Evaluation response:",
                data
            );


            if (
                data.status !==
                "success"
            ) {

                throw new Error(
                    "Evaluation returned an unsuccessful status."
                );
            }


            renderEvaluationMetrics(
                data.evaluation
            );

        }

        catch (error) {

            console.error(
                "Evaluation error:",
                error
            );


            renderEvaluationMetrics(
                null
            );
        }
    }


    /* =========================================
       RENDER RETRIEVAL QUALITY
       ========================================= */

    function renderEvaluationMetrics(
        metrics
    ) {

        if (!metrics) {

            if (precisionScore) {
                precisionScore.textContent =
                    "--";
            }

            if (recallScore) {
                recallScore.textContent =
                    "--";
            }

            if (mrrScore) {
                mrrScore.textContent =
                    "--";
            }

            if (retrievalAccuracy) {
                retrievalAccuracy.textContent =
                    "--";
            }

            return;
        }


        if (precisionScore) {

            precisionScore.textContent =
                formatPercentage(
                    metrics.precision_at_3
                );
        }


        if (recallScore) {

            recallScore.textContent =
                formatPercentage(
                    metrics.recall_at_3
                );
        }


        if (mrrScore) {

            mrrScore.textContent =
                formatPercentage(
                    metrics.mrr
                );
        }


        if (retrievalAccuracy) {

            retrievalAccuracy.textContent =
                formatPercentage(
                    metrics.retrieval_accuracy
                );
        }
    }


    /* =========================================
       FORMAT PERCENTAGE
       ========================================= */

    function formatPercentage(
        value
    ) {

        const number =
            Number(value);


        if (Number.isNaN(number)) {
            return "--";
        }


        return `${Math.round(number * 100)}%`;
    }


    /* =========================================
       MODEL NAME FORMATTER
       ========================================= */

    function formatModelName(model) {

        if (!model) {
            return "--";
        }


        const modelText =
            String(model);


        if (
            modelText ===
            "gemini-3.5-flash-lite"
        ) {

            return "Gemini 3.5 Flash Lite";
        }


        if (
            modelText.startsWith(
                "gemini-"
            )
        ) {

            return modelText
                .replace(
                    /^gemini-/,
                    "Gemini "
                )
                .replace(
                    /-/g,
                    " "
                );
        }


        return modelText;
    }


    /* =========================================
       RENDER SOURCES
       ========================================= */

    function renderSources(sources) {

        sourcesContainer.innerHTML = "";


        if (
            !sources ||
            sources.length === 0
        ) {

            sourcesContainer.innerHTML = `
                <div class="source-item">

                    <div class="file-icon">
                        &lt;/&gt;
                    </div>

                    <div class="source-info">

                        <div class="source-file">
                            No source information available
                        </div>

                        <div class="source-meta">
                            No retrieved code context
                        </div>

                    </div>

                </div>
            `;

            return;
        }


        sources.forEach(
            (source) => {

                const sourceItem =
                    document.createElement(
                        "div"
                    );


                sourceItem.className =
                    "source-item";


                const filePath =
                    source.file_path ||
                    "Unknown file";


                const startLine =
                    source.start_line ??
                    "-";


                const endLine =
                    source.end_line ??
                    "-";


                const name =
                    source.name ||
                    "Unknown element";


                const elementType =
                    source.element_type ||
                    "code";


                const score =
                    typeof source.rerank_score ===
                    "number"
                        ? source.rerank_score.toFixed(2)
                        : "N/A";


                const content =
                    source.content ||
                    "No code available.";


                const cleanPath =
                    cleanFilePath(
                        filePath
                    );


                sourceItem.innerHTML = `
                    <div class="file-icon">
                        &lt;/&gt;
                    </div>

                    <div class="source-info">

                        <div class="source-file">
                            ${escapeHtml(cleanPath)}
                        </div>

                        <div class="source-meta">
                            Lines ${startLine}–${endLine}
                            · ${escapeHtml(elementType)}
                            · ${escapeHtml(name)}
                        </div>

                    </div>

                    <div class="source-actions">

                        <div class="source-score">
                            Score ${score}
                        </div>

                        <button
                            class="view-code-button"
                            type="button"
                        >
                            View Code
                        </button>

                    </div>

                    <div class="code-preview hidden">

                        <div class="code-preview-header">

                            <span>
                                Retrieved Code
                            </span>

                            <span>
                                Lines ${startLine}–${endLine}
                            </span>

                        </div>

                        <pre><code>${escapeHtml(content)}</code></pre>

                    </div>
                `;


                const viewButton =
                    sourceItem.querySelector(
                        ".view-code-button"
                    );


                const codePreview =
                    sourceItem.querySelector(
                        ".code-preview"
                    );


                if (
                    viewButton &&
                    codePreview
                ) {

                    viewButton.addEventListener(
                        "click",
                        () => {

                            codePreview.classList.toggle(
                                "hidden"
                            );


                            if (
                                codePreview.classList.contains(
                                    "hidden"
                                )
                            ) {

                                viewButton.textContent =
                                    "View Code";

                            }

                            else {

                                viewButton.textContent =
                                    "Hide Code";
                            }
                        }
                    );
                }


                sourcesContainer.appendChild(
                    sourceItem
                );

            }
        );
    }


    /* =========================================
       CLEAN FILE PATH
       ========================================= */

    function cleanFilePath(filePath) {

        let path =
            String(filePath);


        path =
            path.replace(
                /\\/g,
                "/"
            );


        const marker =
            "GitContext-AI/";


        const index =
            path.indexOf(
                marker
            );


        if (index !== -1) {

            path =
                path.substring(
                    index +
                    marker.length
                );
        }


        return path;
    }


    /* =========================================
       ESCAPE HTML
       ========================================= */

    function escapeHtml(value) {

        return String(value)
            .replace(
                /&/g,
                "&amp;"
            )
            .replace(
                /</g,
                "&lt;"
            )
            .replace(
                />/g,
                "&gt;"
            )
            .replace(
                /"/g,
                "&quot;"
            )
            .replace(
                /'/g,
                "&#039;"
            );
    }


    /* =========================================
       DELAY
       ========================================= */

    function delay(milliseconds) {

        return new Promise(
            (resolve) => {

                setTimeout(
                    resolve,
                    milliseconds
                );

            }
        );
    }


    /* =========================================
       ASK BUTTON
       ========================================= */

    askButton.addEventListener(
        "click",
        askGitContext
    );


    /* =========================================
       CTRL + ENTER
       ========================================= */

    questionInput.addEventListener(
        "keydown",
        (event) => {

            if (
                event.ctrlKey &&
                event.key === "Enter"
            ) {

                event.preventDefault();

                askGitContext();
            }

        }
    );


    /* =========================================
       EXAMPLE QUESTIONS
       ========================================= */

    const exampleButtons =
        document.querySelectorAll(
            ".example-questions button"
        );


    exampleButtons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                () => {

                    questionInput.value =
                        button.textContent.trim();


                    questionInput.focus();

                }
            );

        }
    );


    /* =========================================
       COPY ANSWER
       ========================================= */

    if (copyButton) {

        copyButton.addEventListener(
            "click",
            async () => {

                const answer =
                    answerElement.textContent;


                if (!answer) {
                    return;
                }


                try {

                    await navigator.clipboard.writeText(
                        answer
                    );


                    copyButton.textContent =
                        "Copied ✓";


                    setTimeout(
                        () => {

                            copyButton.textContent =
                                "Copy";

                        },
                        1500
                    );

                }

                catch (error) {

                    console.error(
                        "Copy failed:",
                        error
                    );
                }

            }
        );
    }


    console.log(
        "GitContext-AI frontend initialized successfully."
    );

});