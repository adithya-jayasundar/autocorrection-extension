console.log("popup.js loaded!");

// Elements
const inputText = document.getElementById("inputText");
const correctBtn = document.getElementById("correctBtn");
const resultDiv = document.getElementById("result");
const loader = document.getElementById("loader");

// Event: Correct Sentence
correctBtn.addEventListener("click", () => {
  const text = inputText.value.trim();
  if (!text) {
    resultDiv.textContent = "⚠️ Please enter a sentence.";
    return;
  }

  // Show loader
  loader.style.display = "block";
  resultDiv.textContent = "";

  fetch("https://3725-14-139-189-168.ngrok-free.app/correct", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text })
  })
    .then(response => response.json())
    .then(data => {
      loader.style.display = "none";
      resultDiv.textContent = "✅ Corrected: " + data.corrected;
    })
    .catch(err => {
      loader.style.display = "none";
      console.error("Fetch error:", err);
      resultDiv.textContent = "❌ Error: " + err.message;
    });
});

// Function: Copy to Clipboard
function copyResult() {
  const text = resultDiv.textContent;
  if (!text) {
    alert("There is no corrected sentence to copy.");
    return;
  }

  navigator.clipboard.writeText(text.replace("✅ Corrected: ", ""))
    .then(() => {
      alert("Corrected text copied to clipboard!");
    })
    .catch(err => {
      console.error("Copy failed:", err);
    });
}

// Attach only copyResult globally if needed
window.copyResult = copyResult;
