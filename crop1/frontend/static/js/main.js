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
  const clearBtn = document.getElementById("clear");

  // load states/districts
  fetch("/static/data/states_districts.json")
    .then(res => res.json())
    .then(data => {
      const states = Object.keys(data).sort();
      states.forEach(s => {
        const o = document.createElement("option");
        o.value = s; o.textContent = s; stateSelect.appendChild(o);
      });
      stateSelect.addEventListener("change", () => {
        const selected = stateSelect.value;
        districtSelect.innerHTML = '<option value="">Enter the district...</option>';
        (data[selected] || []).forEach(d => {
          const o = document.createElement("option");
          o.value = d; o.textContent = d; districtSelect.appendChild(o);
        });
      });
    }).catch(err => console.error("Failed to load states:", err));

  // calculate
  predictBtn?.addEventListener("click", async () => {
    const payload = {
      state: stateSelect.value,
      district: districtSelect.value,
      season: seasonSelect.value,
      crop: cropSelect.value,
      area: areaInput.value,
      area_unit: unitSelect.value
    };
    if (!payload.state || !payload.district || !payload.crop || !payload.area) {
      resultDiv.innerHTML = '<div class="error">Please fill all mandatory fields.</div>'; return;
    }
    resultDiv.innerHTML = '⏳ Calculating...';
    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
      });
      const json = await res.json();
      const v = (json.yield_prediction !== undefined) ? json.yield_prediction : (json.yield || 0);
      resultDiv.innerHTML = `<div class="card"><h3>Predicted Yield</h3><p style="font-size:18px">${v} (units)</p></div>`;
    } catch (e) {
      console.error(e);
      resultDiv.innerHTML = '<div class="error">Prediction failed. Try again later.</div>';
    }
  });

  // clear behavior
  clearBtn?.addEventListener("click", () => {
    resultDiv.innerHTML = "";
  });

  // save behavior (smart)
  saveBtn?.addEventListener("click", async () => {
    const payload = {
      state: stateSelect.value,
      district: districtSelect.value,
      season: seasonSelect.value,
      crop: cropSelect.value,
      area: areaInput.value,
      area_unit: unitSelect.value
    };
    try {
      const res = await fetch("/save_prediction", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
      if (res.status === 401) {
        // not logged in
        window.location.href = "/login";
        return;
      }
      const data = await res.json();
      if (data.status === "saved") {
        // redirect to predictions page
        window.location.href = "/predictions";
      } else {
        alert("Save failed");
      }
    } catch (e) {
      console.error("Save error", e);
      alert("Save failed");
    }
  });

  // small ui focus style
  document.querySelectorAll("input, select").forEach(el => {
    el.addEventListener("focus", () => el.style.borderColor = "#1a73e8");
    el.addEventListener("blur", () => el.style.borderColor = "#e0e0e0");
  });
});
