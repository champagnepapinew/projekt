const API_BASE = "";

async function loadOptions() {
    const res = await fetch(`${API_BASE}/api/form-options`);
    const data = await res.json();

    fillSelect("boat_type", data.boat_types);
    fillSelect("region", data.regions);
    fillSelect("cabins", data.cabins);
    fillSelect("berths", data.berths);
    fillSelect("length", data.lengths);
}

function fillSelect(id, values) {
    const select = document.getElementById(id);
    select.innerHTML = `<option value="">Any</option>`;

    values.forEach(v => {
        const opt = document.createElement("option");
        opt.value = v;
        opt.textContent = v;
        select.appendChild(opt);
    });
}

async function getPrice() {
  const date = document.getElementById("date").value;
  const boat_type = document.getElementById("boat_type").value;
  const region = document.getElementById("region").value;
  const cabins = document.getElementById("cabins").value;
  const berths = document.getElementById("berths").value;
  const length = document.getElementById("length").value;

  if (!date) {
    alert("Please select a date");
    return;
  }

  const params = new URLSearchParams();
  params.set("date", date);

  // Only add filters if the user selected something
  if (boat_type) params.set("boat_type", boat_type);
  if (region) params.set("region", region);
  if (cabins) params.set("cabins", cabins);
  if (berths) params.set("berths", berths);
  if (length) params.set("length", length);

  const url = `${API_BASE}/api/suggest-price?${params.toString()}`;

  const res = await fetch(url);
  const data = await res.json();

  console.log("API response:", data); // debug

  if (data.suggested_price_euro === null || data.suggested_price_euro === undefined) {
  document.getElementById("result").innerText =
    "No matching boats found for selected criteria.";
} else {
  document.getElementById("result").innerText =
    `Suggested weekly price: €${data.suggested_price_euro}`;
}
}

loadOptions();
