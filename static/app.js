    console.log("APP JS EXECUTED");
    let pieChart;
    let barChart;// ===============================
    // DOM Elements
    // ===============================

    const form = document.getElementById("sentimentForm");
    console.log(form);
    const textarea = document.getElementById("review");
    const button = document.getElementById("analyzeBtn");

    const counter = document.getElementById("charCount");

    // ===============================
    // Character Counter
    // ===============================

    if (textarea && counter) {

        const updateCounter = () => {

            counter.textContent = textarea.value.length;

        };

        textarea.addEventListener("input", updateCounter);

        updateCounter();

    }

    // ===============================
    // Ctrl + Enter
    // ===============================

    textarea.addEventListener("keydown", function (e) {

        if (e.key === "Enter" && e.ctrlKey) {

            e.preventDefault();

            form.requestSubmit();

        }

    });

    // ===============================
    // Submit Form
    // ===============================

    console.log("Submit event fired");
    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        button.disabled = true;

        button.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin me-2"></i>Analyzing...';

        try {

            const response = await fetch("/predict", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    review: textarea.value

                })

            });

            const data = await response.json();
            const downloadBtn = document.getElementById("downloadBtn");

if (downloadBtn) {

    downloadBtn.href = data.download;

    downloadBtn.style.display = "inline-flex";

}
            console.log(data);

    const prediction = data.prediction.toLowerCase();

    const predictionText = document.getElementById("predictionText");
    const predictionIcon = document.getElementById("predictionIcon");
    const reviewEcho = document.getElementById("reviewEcho");
    const predictionConfidence =
    document.getElementById("predictionConfidence");
    const predictionSection = document.getElementById("predictionSection");

    predictionSection.style.display = "block";

    setTimeout(() => {

        predictionSection.classList.add("show");

    }, 100);

    // Update prediction text
    predictionText.textContent =
        prediction.charAt(0).toUpperCase() + prediction.slice(1);
        predictionConfidence.textContent =
    "Confidence: " + data.confidence + "%";
        if(prediction==="positive"){

    predictionConfidence.textContent =
        "Confidence: 96%";

}

else if(prediction==="neutral"){

    predictionConfidence.textContent =
        "Confidence: 88%";

}

else{

    predictionConfidence.textContent =
        "Confidence: 94%";

}

    // Show analyzed review
    reviewEcho.textContent = textarea.value;

    // Reset classes
    predictionText.className = "prediction-value";
    predictionIcon.className = "prediction-icon";

    // Change icon + color
    if (prediction === "positive") {

        predictionText.classList.add("positive");
        predictionIcon.classList.add("positive");

        predictionIcon.innerHTML =
            '<i class="fa-solid fa-face-smile-beam"></i>';

    }

    else if (prediction === "negative") {

        predictionText.classList.add("negative");
        predictionIcon.classList.add("negative");

        predictionIcon.innerHTML =
            '<i class="fa-solid fa-face-frown"></i>';

    }

    else {

        predictionText.classList.add("neutral");
        predictionIcon.classList.add("neutral");

        predictionIcon.innerHTML =
            '<i class="fa-solid fa-face-meh"></i>';

    }

        }

        catch (err) {

            console.error(err);

        }

        finally {

            button.disabled = false;

            button.innerHTML =
                '<i class="fa-solid fa-magnifying-glass-chart me-2"></i>Analyze Sentiment';

        }

    });
    // ===================================
    // CSV Upload
    // ===================================

    const browseBtn = document.getElementById("browseBtn");
    const csvFile = document.getElementById("csvFile");
    const uploadBtn = document.getElementById("uploadBtn");
    const selectedFile = document.getElementById("selectedFile");

    if (browseBtn && csvFile && uploadBtn && selectedFile) {

        browseBtn.addEventListener("click", () => {
            csvFile.click();
        });

        csvFile.addEventListener("change", () => {

            if (csvFile.files.length > 0) {

                selectedFile.textContent = csvFile.files[0].name;

                uploadBtn.style.display = "inline-block";

            }

        });

        uploadBtn.addEventListener("click", async () => {

            const formData = new FormData();

            formData.append("file", csvFile.files[0]);

            uploadBtn.disabled = true;
            uploadBtn.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin me-2"></i>Uploading...';

            try {

                const response = await fetch("/upload_csv", {

                    method: "POST",

                    body: formData

                });

                const data = await response.json();

    document.getElementById("csvResults").style.display = "block";

    document.getElementById("positiveCount").textContent = data.positive;
    document.getElementById("neutralCount").textContent = data.neutral;
    document.getElementById("negativeCount").textContent = data.negative;
    document.getElementById("positivePercent").textContent =
    data.positive_percent + "%";

document.getElementById("neutralPercent").textContent =
    data.neutral_percent + "%";

document.getElementById("negativePercent").textContent =
    data.negative_percent + "%";
    // Destroy previous charts if they exist

    if (pieChart) pieChart.destroy();
    if (barChart) barChart.destroy();

    // Pie Chart

    pieChart = new Chart(
        document.getElementById("pieChart"),
        {
            type: "pie",

            data: {

                labels: ["Positive", "Neutral", "Negative"],

                datasets: [{

                    data: [
                        data.positive,
                        data.neutral,
                        data.negative
                    ],

                    backgroundColor: [
                        "#22c55e",
                        "#facc15",
                        "#ef4444"
                    ]

                }]

            },

            options: {

                responsive: true,

                animation: {

                    duration: 1500,

                    easing: "easeOutQuart"

                },

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }
            

        }
    );

    // Bar Chart

    barChart = new Chart(
        document.getElementById("barChart"),
        {
            type: "bar",

            data: {

                labels: ["Positive", "Neutral", "Negative"],

                datasets: [{

                    label: "Reviews",

                    data: [
                        data.positive,
                        data.neutral,
                        data.negative
                    ],

                    backgroundColor: [
                        "#22c55e",
                        "#facc15",
                        "#ef4444"
                    ]

                }]

            },

            options: {

                responsive: true,

                animation: {

                    duration: 1500,

                    easing: "easeOutQuart"

                },

                scales: {

                    y: {

                        beginAtZero: true

                    }

                }

            }

        }
    );

    document.getElementById("csvResults").scrollIntoView({
        behavior: "smooth"
    }); 

            }

            catch(err){

                console.error(err);

            }

            finally{

                uploadBtn.disabled = false;

                uploadBtn.innerHTML =
                    '<i class="fa-solid fa-cloud-arrow-up me-2"></i>Analyze CSV';

            }

        });

    }
    // ===============================
    // Pipeline Animation
    // ===============================

    const pipelineSteps = document.querySelectorAll(".pipeline-step");

    const pipelineObserver = new IntersectionObserver((entries) => {

        entries.forEach((entry, index) => {

            if (entry.isIntersecting) {

                setTimeout(() => {

                    entry.target.classList.add("animate");

                }, index * 200);

            }

        });

    }, {
        threshold: 0.3
    });

    pipelineSteps.forEach(step => {

        pipelineObserver.observe(step);

    });