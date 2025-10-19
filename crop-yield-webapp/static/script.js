document.addEventListener("DOMContentLoaded", function(){
  const form = document.getElementById("predict-form");
  const resultsCard = document.getElementById("results");
  const output = document.getElementById("output");
  const backBtn = document.getElementById("back-btn");
  const downloadBtn = document.getElementById("download-btn");

  function showResults(data){
    output.innerHTML = "";
    const addRow = (k,v) => {
      const div = document.createElement("div");
      div.className = "result-row";
      div.innerHTML = `<div>${k}</div><div><strong>${v}</strong></div>`;
      output.appendChild(div);
    };
    addRow("Predicted yield", `${data.predicted_yield} ${data.yield_units}`);
    addRow("Estimated ETc", `${data.ETc_mm} mm (season)`);
    addRow("Water required (total)", `${data.water_m3_total} m³`);
    addRow("Water required (per ha)", `${data.water_m3_per_ha} m³/ha`);
    const pre = document.createElement("pre");
    pre.style.marginTop = "10px";
    pre.style.fontSize = "0.85rem";
    pre.textContent = "Assumptions:\\n" + JSON.stringify(data.assumptions, null, 2);
    output.appendChild(pre);
    resultsCard.style.display = "block";
    form.parentElement.style.display = "none";
  }

  form.addEventListener("submit", async function(e){
    e.preventDefault();
    const state = document.getElementById("state").value;
    const district = document.getElementById("district").value;
    const season = document.getElementById("season").value;
    const crop = document.getElementById("crop").value;
    const area = document.getElementById("area").value;
    const payload = { state, district, season, crop, area };
    try {
      const resp = await fetch("/predict", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      if (!resp.ok) {
        alert("Error: " + (data.detail || data.error || "Unknown"));
        return;
      }
      showResults(data);
    } catch(err) {
      alert("Request failed: " + err);
    }
  });

  backBtn.addEventListener("click", function(){
    resultsCard.style.display = "none";
    form.parentElement.style.display = "block";
  });

  downloadBtn.addEventListener("click", function(){
    alert("Report download feature is a placeholder. Can be implemented to generate PDF or CSV per user request.");
  });

  // Language toggle top-right
  const langInputs = document.querySelectorAll('input[name="lang"]');
  langInputs.forEach(i => i.addEventListener("change", (ev) => {
    const v = ev.target.value;
    if (v === "ta") {
      document.getElementById("title").textContent = "பயிர் பயன் & நீா் மதிப்பீடு";
      document.getElementById("form-title").textContent = "உள்ளீடுகளை அனுப்பு";
      document.getElementById("results-title").textContent = "முடிவுகள்";
      document.getElementById("predict-btn").textContent = "முன்னறிவு";
      document.querySelector('label[for="state"]').textContent = "மாநிலம் தேர்ந்தெடு";
      document.querySelector('label[for="district"]').textContent = "மாவட்டம் (தமிழ்நாடு)";
      document.querySelector('label[for="season"]').textContent = "பருவம்";
      document.querySelector('label[for="crop"]').textContent = "பயிர்";
      document.querySelector('label[for="area"]').textContent = "பிள்ளை இடம் (ha)";
    } else {
      document.getElementById("title").textContent = "Crop Yield & Water Estimator";
      document.getElementById("form-title").textContent = "Enter inputs";
      document.getElementById("results-title").textContent = "Results";
      document.getElementById("predict-btn").textContent = "Get Prediction";
      document.querySelector('label[for="state"]').textContent = "Select State";
      document.querySelector('label[for="district"]').textContent = "Select District (Tamil Nadu)";
      document.querySelector('label[for="season"]').textContent = "Select Season";
      document.querySelector('label[for="crop"]').textContent = "Select Crop";
      document.querySelector('label[for="area"]').textContent = "Area (hectares)";
    }
  }));
});