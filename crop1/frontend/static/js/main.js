document.addEventListener("DOMContentLoaded", function () {
  const stateSelect = document.getElementById("state");
  const districtSelect = document.getElementById("district");
  const seasonSelect = document.getElementById("season");
  const cropSelect = document.getElementById("crop");
  const areaInput = document.getElementById("area");
  const unitSelect = document.getElementById("area_unit");
  const predictBtn = document.getElementById("predict");
  const saveBtn = document.getElementById("save");
  const resultDiv = document.getElementById("result");

  /* ----------------------------
      1️⃣ Load states & districts
  ----------------------------- */
  fetch("/static/data/states_districts.json")
    .then((res) => res.json())
    .then((data) => {
      Object.keys(data).forEach((state) => {
        const opt = document.createElement("option");
        opt.value = state;
        opt.textContent = state;
        stateSelect.appendChild(opt);
      });

      stateSelect.addEventListener("change", () => {
        const selectedState = stateSelect.value;
        districtSelect.innerHTML = '<option value="">Select District</option>';
        if (data[selectedState]) {
          data[selectedState].forEach((district) => {
            const opt = document.createElement("option");
            opt.value = district;
            opt.textContent = district;
            districtSelect.appendChild(opt);
          });
        }
      });
    })
    .catch((err) => console.error("Failed to load state data:", err));

  /* ----------------------------
      2️⃣ Handle Calculate Button
  ----------------------------- */
  predictBtn?.addEventListener("click", async () => {
    const formData = {
      state: stateSelect.value,
      district: districtSelect.value,
      season: seasonSelect.value,
      crop: cropSelect.value,
      area: areaInput.value,
      area_unit: unitSelect.value,
    };

    // Basic form validation
    if (!formData.state || !formData.district || !formData.season || !formData.crop || !formData.area) {
      resultDiv.innerHTML = `<p class="error">⚠️ Please fill all fields before calculating.</p>`;
      return;
    }

    resultDiv.innerHTML = `<p>⏳ Calculating yield prediction...</p>`;

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      resultDiv.innerHTML = `
        <div class="result-card">
          <h3>🌾 Predicted Yield</h3>
          <p><strong>${result.yield_prediction.toFixed(2)}</strong> tons per ${formData.area_unit}</p>
        </div>`;
    } catch (error) {
      console.error("Prediction error:", error);
      resultDiv.innerHTML = `<p class="error">❌ Prediction failed. Try again later.</p>`;
    }
  });

  /* ----------------------------
      3️⃣ Handle Save Button
  ----------------------------- */
  saveBtn?.addEventListener("click", () => {
    // For now redirect to login/register if not logged in
    window.location.href = "/login";
  });

  /* ----------------------------
      4️⃣ UI Quality Enhancements
  ----------------------------- */
  const inputs = document.querySelectorAll("input, select");
  inputs.forEach((el) => {
    el.addEventListener("focus", () => (el.style.borderColor = "#1a73e8"));
    el.addEventListener("blur", () => (el.style.borderColor = "#dadce0"));
  });
});
