// frontend/static/js/main.js
document.addEventListener("DOMContentLoaded", function () {
  const stateEl = document.getElementById("state");
  const districtEl = document.getElementById("district");
  const calculateBtn = document.getElementById("btn-calculate");
  const clearBtn = document.getElementById("btn-clear");
  const saveBtn = document.getElementById("btn-save");
  const areaInput = document.getElementById("area");
  const areaUnit = document.getElementById("area_unit");
  const resultBox = document.getElementById("prediction-result");

  // helper to create placeholder option
  function placeholderOption(text) {
    const o = document.createElement("option");
    o.value = "";
    o.textContent = text;
    o.disabled = true;
    o.selected = true;
    o.hidden = true;
    return o;
  }

  // load states-districts json
  fetch("/static/data/states_districts.json")
    .then((r) => r.json())
    .then((data) => {
      // populate states
      stateEl.innerHTML = "";
      stateEl.appendChild(placeholderOption("Select state..."));
      Object.keys(data).sort().forEach((s) => {
        const opt = document.createElement("option");
        opt.value = s;
        opt.textContent = s;
        stateEl.appendChild(opt);
      });

      // when state changes, populate districts
      stateEl.addEventListener("change", function () {
        const chosen = this.value;
        const districts = data[chosen] || [];
        districtEl.innerHTML = "";
        districtEl.appendChild(placeholderOption("Select district..."));
        districts.forEach((d) => {
          const o = document.createElement("option");
          o.value = d;
          o.textContent = d;
          districtEl.appendChild(o);
        });
      });
    })
    .catch((err) => {
      console.error("Failed to load states JSON", err);
    });

  // Clear form
  if (clearBtn) {
    clearBtn.addEventListener("click", function (e) {
      e.preventDefault();
      const form = this.closest("form") || document.querySelector("form");
      if (form) form.reset();
      resultBox && (resultBox.textContent = "");
    });
  }

  // Calculate
  if (calculateBtn) {
    calculateBtn.addEventListener("click", function (e) {
      e.preventDefault();
      // gather main fields - adapt if your form fields are named differently
      const payload = {
        state: stateEl.value || "",
        district: districtEl.value || "",
        season: document.getElementById("season")?.value || "",
        crop: document.getElementById("crop")?.value || "",
        area: areaInput?.value || "",
        area_unit: areaUnit?.value || "",
        // include any other fields your backend expects
      };

      // Basic front-end validation
      if (!payload.state || !payload.crop) {
        alert("Please select state and crop.");
        return;
      }

      calculateBtn.disabled = true;
      calculateBtn.textContent = "Calculating...";

      fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((r) => r.json())
        .then((json) => {
          resultBox && (resultBox.innerText = "Prediction: " + (json.yield_prediction ?? JSON.stringify(json)));
        })
        .catch((err) => {
          console.error(err);
          alert("Prediction failed. See console.");
        })
        .finally(() => {
          calculateBtn.disabled = false;
          calculateBtn.textContent = "Calculate";
        });
    });
  }

  // Save -> require login
  if (saveBtn) {
    saveBtn.addEventListener("click", function (e) {
      e.preventDefault();
      const username = window.USERNAME || "";
      if (!username) {
        // redirect to login (keeping current location in next param)
        const redirect = encodeURIComponent(window.location.pathname);
        window.location.href = `/login?next=${redirect}`;
        return;
      }
      // If logged in, call a save endpoint (you can implement on backend)
      alert("Saving prediction to your history (backend must implement save endpoint).");
    });
  }

  // small UX: placeholders and grey text handled by HTML placeholder attrs + CSS
});
