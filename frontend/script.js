const analyzeBtn = document.getElementById("analyzeBtn");
const textarea = document.getElementById("codeInput");
const resultsDiv = document.getElementById("results");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("errorBox");

analyzeBtn.addEventListener("click", async () => {

  const code = textarea.value.trim();

  if (!code) {
    alert("Please paste some code first.");
    return;
  }

  resultsDiv.innerHTML = "";
  errorBox.classList.add("hidden");
  loading.classList.remove("hidden");
  analyzeBtn.disabled = true;

  try {

    const response = await fetch(
      "https://codeunderstood.onrender.com/analyze",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code })
      }
    );

    if (!response.ok) {
      throw new Error("Backend error: " + response.status);
    }

    const data = await response.json();

    loading.classList.add("hidden");
    analyzeBtn.disabled = false;

    if (data.error) {
      showError(data.error);
      return;
    }

    renderResults(data);

  } catch (err) {

    loading.classList.add("hidden");
    analyzeBtn.disabled = false;

    showError("Failed to connect to backend.");
    console.error(err);

  }

});

function showError(message) {
  errorBox.innerText = message;
  errorBox.classList.remove("hidden");
}

function createCard(title, content) {
  return `
    <div class="card">
      <h3>${title}</h3>
      <div>${content}</div>
    </div>
  `;
}

function renderResults(data) {

  const safeJoin = (value) =>
    Array.isArray(value) ? value.join(", ") : value || "N/A";

  resultsDiv.innerHTML = `
    ${createCard("Language", data.language || "N/A")}
    ${createCard("Domain", data.domain || "N/A")}
    ${createCard("Architectural Layer", data.architectural_layer || "N/A")}
    ${createCard("Time Complexity", data.time_complexity || "N/A")}
    ${createCard("Space Complexity", data.space_complexity || "N/A")}
    ${createCard("Primary Concepts", safeJoin(data.primary_concepts))}
    ${createCard("Secondary Concepts", safeJoin(data.secondary_concepts))}
    ${createCard("Design Patterns", safeJoin(data.design_patterns))}
    ${createCard("Execution Flow", data.execution_flow || "N/A")}
    ${createCard("Why Abstraction Exists", data.why_abstraction_exists || "N/A")}
    ${createCard("Prerequisites", safeJoin(data.prerequisite_concepts))}
  `;
}
