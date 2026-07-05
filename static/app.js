// ===============================
// DOM Elements
// ===============================

const form = document.getElementById("sentimentForm");
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
        console.log(data);

const prediction = data.prediction.toLowerCase();

const predictionText = document.getElementById("predictionText");
const predictionIcon = document.getElementById("predictionIcon");
const reviewEcho = document.getElementById("reviewEcho");

// Update prediction text
predictionText.textContent =
    prediction.charAt(0).toUpperCase() + prediction.slice(1);

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

            alert(
`✅ ${data.message}

Positive : ${data.positive}

Neutral : ${data.neutral}

Negative : ${data.negative}`
);

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