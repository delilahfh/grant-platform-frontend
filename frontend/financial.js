
let headings = [];

function addHeading(){
  const heading = document.getElementById("headingInput").value.trim();
  if(!heading) return;

  const newHeading = { heading, lines: [] };
  headings.push(newHeading);

  renderHeadings();
  document.getElementById("headingInput").value = "";
}

function addLine(index){
  const name = document.getElementById("lineName_"+index).value.trim();
  const unit = document.getElementById("lineUnit_"+index).value.trim();
  const price = document.getElementById("linePrice_"+index).value.trim();

  if(!name || !unit || !price) return;

  headings[index].lines.push({ name, unit, price });
  renderHeadings();
}

function renderHeadings(){
  const container = document.getElementById("headingsContainer");
  container.innerHTML = headings.map((h, i) => `
    <div class='block'>
      <h4>${h.heading}</h4>
      <input id="lineName_${i}" placeholder="Line name">
      <input id="lineUnit_${i}" placeholder="Unit amount">
      <input id="linePrice_${i}" placeholder="Price per unit">
      <button type="button" onclick="addLine(${i})">Add Line</button>

      <ul>${h.lines.map(l => `<li>${l.name} - ${l.unit} units x ${l.price}</li>`).join("")}</ul>
    </div>
  `).join("");
}

document.getElementById("financialForm").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  const payload = { headings };

  const res = await fetch("https://grant-app-backend.onrender.com/financial-proposal", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if(res.ok){
    alert("Submitted!");
    window.location.href="dashboard.html";
  } else {
    alert("Error submitting");
  }
});
