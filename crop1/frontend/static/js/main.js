document.addEventListener("DOMContentLoaded", function () {
  const predictBtn = document.getElementById("predict");
  const saveBtn = document.getElementById("save");
  const resultDiv = document.getElementById("result");

  predictBtn?.addEventListener("click", async () => {
    const data = {
      state: document.getElementById("state").value,
      district: document.getElementById("district").value,
      season: document.getElementById("season").value,
      crop: document.getElementById("crop").value,
      area: document.getElementById("area").value,
      area_unit: document.getElementById("area_unit").value,
    };

    resultDiv.innerHTML = "⏳ Calculating...";

    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    resultDiv.innerHTML = `<b>Predicted Yield:</b> ${result.yield_prediction.toFixed(2)}`;
  });

  saveBtn?.addEventListener("click", () => {
    window.location.href = "/login";
  });
});
