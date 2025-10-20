document.addEventListener("DOMContentLoaded", () => {
  const stateSel = document.getElementById("state");
  const districtSel = document.getElementById("district");
  const seasonSel = document.getElementById("season");
  const cropSel = document.getElementById("crop");
  const form = document.getElementById("predictionForm");
  const resultDiv = document.getElementById("predictionResult");
  const btnPdf = document.getElementById("downloadPdf");
  const btnDocx = document.getElementById("downloadDocx");

  Promise.all([
    fetch("/static/data/states_districts.json").then(r => r.json()),
    fetch("/static/data/crops_seasons.json").then(r => r.json())
  ]).then(([states, crops]) => {
    Object.keys(states).forEach(st => {
      const o = document.createElement("option");
      o.value = st; o.textContent = st;
      stateSel.appendChild(o);
    });
    Object.keys(crops.seasons).forEach(season => {
      const o = document.createElement("option");
      o.value = season; o.textContent = season;
      seasonSel.appendChild(o);
    });
    Object.keys(crops.crops).forEach(crop => {
      const o = document.createElement("option");
      o.value = crop; o.textContent = crop;
      cropSel.appendChild(o);
    });

    stateSel.addEventListener("change", () => {
      districtSel.innerHTML = "";
      const districts = states[stateSel.value] || [];
      districts.forEach(d => {
        const o = document.createElement("option");
        o.value = d; o.textContent = d;
        districtSel.appendChild(o);
      });
    });
  });

  form.addEventListener("submit", async e => {
    e.preventDefault();
    const data = {
      state: stateSel.value,
      district: districtSel.value,
      season: seasonSel.value,
      crop: cropSel.value,
      area: document.getElementById("area").value,
      area_unit: document.getElementById("area_unit").value
    };
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const out = await res.json();
    resultDiv.textContent = `Predicted Yield: ${out.yield_prediction}`;
    btnPdf.classList.remove("hidden");
    btnDocx.classList.remove("hidden");
    btnPdf.onclick = () => downloadReport("pdf", data, out.yield_prediction);
    btnDocx.onclick = () => downloadReport("docx", data, out.yield_prediction);
  });

  async function downloadReport(type, inputs, prediction) {
    const data = {...inputs, yield_prediction: prediction};
    const res = await fetch("/download_report", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({report_type:type, data})
    });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `CropAssist_Report.${type}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
});
