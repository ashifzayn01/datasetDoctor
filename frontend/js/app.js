
const API_BASE_URL = "https://dataset-doctor-api-72p5.onrender.com";

// DOM elements
const apiStatus = document.getElementById("apiStatus");

const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const browseButton = document.getElementById("browseButton");
const selectedFileText = document.getElementById("selectedFile");
const uploadButton = document.getElementById("uploadButton");
const uploadMessage = document.getElementById("uploadMessage");

const totalRows = document.getElementById("totalRows");
const totalColumns = document.getElementById("totalColumns");
const missingValues = document.getElementById("missingValues");
const duplicateRows = document.getElementById("duplicateRows");
const qualityResults = document.getElementById("qualityResults");

const targetColumn = document.getElementById("targetColumn");
const taskType = document.getElementById("taskType");
const runExperimentButton = document.getElementById("runExperimentButton");

// Currently selected CSV file
let currentFile = null;

const MAX_FILE_SIZE = 10 * 1024 * 1024;


// Check backend connection
async function checkAPIStatus() {

    if (!apiStatus) {
        console.error("API status element not found in HTML.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error("Backend is not responding.");
        }

        apiStatus.textContent = "Connected";

    } catch (error) {

        apiStatus.textContent = "Disconnected";
        console.error("API connection error:", error);
    }
}


// Validate selected CSV file
function validateFile(file) {

    if (!file) {
        return "Please select a file.";
    }

    if (!file.name.toLowerCase().endsWith(".csv")) {
        return "Only CSV files are allowed.";
    }

    if (file.size > MAX_FILE_SIZE) {
        return "File size must be 10 MB or less.";
    }

    return null;
}


// Reset previous experiment results when selecting a new file
function resetExperimentUI() {

    targetColumn.innerHTML =
        '<option value="">Upload a dataset first</option>';

    targetColumn.disabled = true;
    taskType.disabled = true;
    runExperimentButton.disabled = true;

    const resultsContainer =
        document.getElementById("experimentResults");

    resultsContainer.textContent =
        "Upload and analyze a dataset to run an experiment.";
}


// Handle file selection
function handleFileSelection(file) {

    resetExperimentUI();

    uploadMessage.textContent = "";

    const error = validateFile(file);

    if (error) {
        currentFile = null;
        selectedFileText.textContent = error;
        uploadButton.disabled = true;
        return;
    }

    currentFile = file;

    selectedFileText.textContent = `Selected: ${file.name}`;

    uploadButton.disabled = false;
}


// Browse button
browseButton.addEventListener("click", () => {
    fileInput.click();
});


// File input change
fileInput.addEventListener("change", (event) => {

    const file = event.target.files[0];

    handleFileSelection(file);
});


// Drag and drop
uploadArea.addEventListener("dragover", (event) => {

    event.preventDefault();

    uploadArea.classList.add("drag-over");
});


uploadArea.addEventListener("dragleave", () => {

    uploadArea.classList.remove("drag-over");
});


uploadArea.addEventListener("drop", (event) => {

    event.preventDefault();

    uploadArea.classList.remove("drag-over");

    const file = event.dataTransfer.files[0];

    handleFileSelection(file);
});


// Display dataset overview
function updateDatasetOverview(data) {

    totalRows.textContent = data.rows;
    totalColumns.textContent = data.columns;

    const missingCount = Object.values(
        data.profile.missing_values || {}
    ).reduce((sum, value) => sum + Number(value), 0);

    missingValues.textContent = missingCount;

    duplicateRows.textContent =
        data.profile.duplicate_rows ?? 0;
}


// Display quality report
function displayQualityReport(report) {

    qualityResults.replaceChildren();

    const heading = document.createElement("h3");

    heading.textContent =
        `Total issues found: ${report.total_issues ?? 0}`;

    qualityResults.appendChild(heading);

    const details = document.createElement("pre");

    details.textContent = JSON.stringify(
        report.issues ?? report,
        null,
        2
    );

    qualityResults.appendChild(details);
}


// Populate target column dropdown
function populateTargetColumns(columns) {

    targetColumn.innerHTML =
        '<option value="">Select target column</option>';

    // Check whether columns are available
    if (!Array.isArray(columns) || columns.length === 0) {

        targetColumn.disabled = true;
        taskType.disabled = true;
        runExperimentButton.disabled = true;

        return;
    }

    columns.forEach((column) => {

        const option = document.createElement("option");

        option.value = column;
        option.textContent = column;

        targetColumn.appendChild(option);
    });

    targetColumn.disabled = false;
    taskType.disabled = false;
    runExperimentButton.disabled = false;
}


// Upload CSV to FastAPI
async function uploadDataset() {

    if (!currentFile) {
        uploadMessage.textContent =
            "Please select a CSV file first.";
        return;
    }

    const formData = new FormData();

    formData.append("file", currentFile);

    uploadButton.disabled = true;
    uploadButton.textContent = "Uploading...";
    uploadMessage.textContent = "";

    try {

        const response = await fetch(
            `${API_BASE_URL}/api/datasets/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Upload failed.");
        }

        updateDatasetOverview(data);

        displayQualityReport(data.quality_report);

        populateTargetColumns(data.column_names);

        uploadMessage.textContent =
            "Dataset uploaded successfully!";

    } catch (error) {

        uploadMessage.textContent = error.message;

        console.error("Upload error:", error);

    } finally {

        uploadButton.disabled = !currentFile;
        uploadButton.textContent = "Analyze Dataset";
    }
}


// Upload button click
uploadButton.addEventListener("click", uploadDataset);


// Check API when page loads
checkAPIStatus();


// Display ML experiment results
function displayExperimentResults(data) {

    const resultsContainer =
        document.getElementById("experimentResults");

    resultsContainer.replaceChildren();

    // Get model results
    const modelResults = data.model_results;
    let models = [];

    if (Array.isArray(modelResults)) {

        models = modelResults.map((item, index) => ({
            name: item.model_name || item.model || item.name || `Model ${index + 1}`,
            metrics: item.metrics || item
        }));

    } else if (modelResults && typeof modelResults === "object") {

        models = Object.entries(modelResults).map(([name, item]) => ({
            name,
            metrics: item.metrics || item
        }));
    }

    if (models.length === 0) {

        const message = document.createElement("p");

        message.textContent = "No model results were returned.";

        resultsContainer.appendChild(message);

        return;
    }


    // Experiment summary cards
    const summaryContainer = document.createElement("div");

    summaryContainer.className = "experiment-summary";

    const summaryItems = [
        ["Task Type", data.task_type],
        ["Target Column", data.target_column],
        ["Training Records", data.train_records],
        ["Testing Records", data.test_records]
    ];

    summaryItems.forEach(([label, value]) => {

        const card = document.createElement("div");

        card.className = "summary-card";

        const heading = document.createElement("p");

        heading.textContent = label;

        const result = document.createElement("h3");

        result.textContent = value ?? "-";

        card.append(heading, result);

        summaryContainer.appendChild(card);
    });

    resultsContainer.appendChild(summaryContainer);


    // Determine comparison metric
    const taskType = String(data.task_type || "").toLowerCase();

    const isClassification = taskType === "classification";


    function getComparisonValue(metrics) {

        const matchingKey = Object.keys(metrics).find(key => {

            const normalizedKey =
                key.toLowerCase().replaceAll("_", "");

            if (isClassification) {

                return normalizedKey === "f1" ||
                       normalizedKey === "f1score";
            }

            return normalizedKey === "rmse" ||
                   normalizedKey === "rootmeansquarederror";
        });

        return matchingKey ? metrics[matchingKey] : null;
    }


    // Find best-performing model
    const comparableModels = models.filter(model => {

        const value = getComparisonValue(model.metrics);

        return typeof value === "number" &&
               Number.isFinite(value);
    });

    let bestModel = null;

    if (comparableModels.length > 0) {

        bestModel = comparableModels.reduce((best, current) => {

            const bestValue = getComparisonValue(best.metrics);

            const currentValue =
                getComparisonValue(current.metrics);

            if (isClassification) {
                return currentValue > bestValue ? current : best;
            }

            return currentValue < bestValue ? current : best;
        });
    }


    // Best model highlight
    const bestModelCard = document.createElement("div");

    bestModelCard.className = "best-model-card";

    const bestHeading = document.createElement("h3");

    bestHeading.textContent = "Best Performing Model";

    const bestDescription = document.createElement("p");

    if (bestModel) {

        const bestValue = getComparisonValue(bestModel.metrics);

        bestDescription.textContent =
           `${bestModel.name} - ${isClassification ? "Highest F1 Score" : "Lowest RMSE"}: ${bestValue.toFixed(4)}`;
    } else {

        bestDescription.textContent =
            "Unable to determine the best model because the comparison metric is unavailable.";
    }

    bestModelCard.append(bestHeading, bestDescription);

    resultsContainer.appendChild(bestModelCard);


    // Create comparison table
    const table = document.createElement("table");

    table.className = "results-table";

    const thead = document.createElement("thead");

    const tbody = document.createElement("tbody");

    const headerRow = document.createElement("tr");

    const modelHeader = document.createElement("th");

    modelHeader.textContent = "Model";

    headerRow.appendChild(modelHeader);


    // Extract available metric names
    const metricKeys = [
        ...new Set(
            models.flatMap(model =>
                Object.keys(model.metrics).filter(
                    key => typeof model.metrics[key] === "number"
                )
            )
        )
    ];


    metricKeys.forEach(key => {

        const th = document.createElement("th");

        th.textContent = key.replaceAll("_", " ").toUpperCase();

        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);


    // Add model results to table
    models.forEach(model => {

        const row = document.createElement("tr");

        if (bestModel && model.name === bestModel.name) {
            row.className = "best-model-row";
        }

        const nameCell = document.createElement("td");

        nameCell.textContent = model.name;

        row.appendChild(nameCell);


        metricKeys.forEach(key => {

            const cell = document.createElement("td");

            const value = model.metrics[key];

            cell.textContent =
                typeof value === "number" && Number.isFinite(value)
                    ? value.toFixed(4)
                    : "-";

            row.appendChild(cell);
        });

        tbody.appendChild(row);
    });


    table.append(thead, tbody);

    resultsContainer.appendChild(table);
}


// Run ML experiment
async function runExperiment() {

    if (!currentFile) {

        alert("Please upload a dataset first.");

        return;
    }

    if (!targetColumn.value) {

        alert("Please select a target column.");

        return;
    }

    const formData = new FormData();

    formData.append("file", currentFile);

    formData.append("target_column", targetColumn.value);

    formData.append("task_type", taskType.value);

    runExperimentButton.disabled = true;

    runExperimentButton.textContent = "Running Experiment...";


    try {

        const response = await fetch(
            `${API_BASE_URL}/api/experiments/run`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Experiment failed.");
        }

        displayExperimentResults(data.experiment_results);

    } catch (error) {

        console.error("Experiment error:", error);

        const resultsContainer =
            document.getElementById("experimentResults");

        resultsContainer.textContent = error.message;

    } finally {

        runExperimentButton.disabled =!currentFile || !targetColumn.value;

        runExperimentButton.textContent = "Run Experiment";
    }
}


// Run experiment button click
runExperimentButton.addEventListener("click", runExperiment);
