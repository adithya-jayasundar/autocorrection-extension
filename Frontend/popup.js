console.log("popup.js loaded!");

document.getElementById("correctBtn").addEventListener("click", () => {
  const text = document.getElementById("inputText").value;

  fetch("https://9102-111-92-46-42.ngrok-free.app/correct", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text })
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("result").textContent = "Corrected: " + data.corrected;
    })
    .catch(err => {
      console.error("Fetch error:", err);
      document.getElementById("result").textContent = "Error: " + err.message;
    });
});
