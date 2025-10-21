document.addEventListener("DOMContentLoaded", function() {
  const stateSelect = document.getElementById("state");
  const districtSelect = document.getElementById("district");

  fetch("/static/data/states_districts.json")
    .then(res => res.json())
    .then(data => {
      Object.keys(data).forEach(state => {
        const opt = document.createElement("option");
        opt.value = state;
        opt.textContent = state;
        stateSelect.appendChild(opt);
      });

      stateSelect.addEventListener("change", function() {
        const selectedState = this.value;
        districtSelect.innerHTML = "";
        const districts = data[selectedState] || [];
        districts.forEach(d => {
          const opt = document.createElement("option");
          opt.value = d;
          opt.textContent = d;
          districtSelect.appendChild(opt);
        });
      });
    });
});
