
const token = localStorage.getItem("jwt");
if(!token){ window.location.href="login.html"; }

// load existing
function loadDeadlines(){
  fetch("https://grant-app-backend.onrender.com/deadlines", {
    headers:{ Authorization:`Bearer ${token}` }
  })
  .then(r => r.json())
  .then(list => {
    const tbody = document.querySelector("#deadlinesTable tbody");
    tbody.innerHTML = "";
    list.forEach(d => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${d.title}</td>
        <td>${d.type}</td>
        <td>${d.project || ""}</td>
        <td>${d.due_at}</td>
        <td>${d.active ? "Active" : "Inactive"}</td>
        <td>
          <button onclick="toggleDeadline('${d.id}', ${d.active ? "false" : "true"})">
            ${d.active ? "Disable" : "Enable"}
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  })
  .catch(() => {
    document.querySelector("#deadlinesTable tbody").innerHTML = "<tr><td colspan='6'>Error loading</td></tr>";
  });
}

loadDeadlines();

document.getElementById("deadlineForm").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const payload = {
    title: document.getElementById("title").value,
    type: document.getElementById("dtype").value,
    project: document.getElementById("project").value,
    due_at: document.getElementById("due").value
  };

  const res = await fetch("https://grant-app-backend.onrender.com/deadlines", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if(res.ok){
    alert("Deadline saved");
    loadDeadlines();
    e.target.reset();
  } else {
    alert("Error saving deadline");
  }
});

async function toggleDeadline(id, active){
  const res = await fetch(`https://grant-app-backend.onrender.com/deadlines/${id}`, {
    method:"PATCH",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify({ active })
  });
  if(res.ok){
    loadDeadlines();
  } else {
    alert("Error updating deadline");
  }
}
