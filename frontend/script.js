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

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ code })
    });

    const data = await response.json();
    loading.classList.add("hidden");

    if (data.error) {
      showError(data.error);
      return;
    }

    renderResults(data);

  } catch (err) {
    loading.classList.add("hidden");
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
  resultsDiv.innerHTML = `
    ${createCard("Language", data.language)}
    ${createCard("Domain", data.domain)}
    ${createCard("Architectural Layer", data.architectural_layer)}
    ${createCard("Time Complexity", data.time_complexity)}
    ${createCard("Space Complexity", data.space_complexity)}
    ${createCard("Primary Concepts", data.primary_concepts.join(", "))}
    ${createCard("Secondary Concepts", data.secondary_concepts.join(", "))}
    ${createCard("Design Patterns", data.design_patterns.join(", "))}
    ${createCard("Execution Flow", data.execution_flow)}
    ${createCard("Why Abstraction Exists", data.why_abstraction_exists)}
    ${createCard("Prerequisites", data.prerequisite_concepts.join(", "))}
  `;
}
