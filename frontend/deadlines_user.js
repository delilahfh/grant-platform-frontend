
const tokenU = localStorage.getItem("jwt");
if(!tokenU){ window.location.href="login.html"; }

fetch("https://grant-app-backend.onrender.com/my-deadlines", {
  headers:{ Authorization:`Bearer ${tokenU}` }
})
.then(r => r.json())
.then(list => {
  const tbody = document.querySelector("#deadlinesTable tbody");
  tbody.innerHTML = "";
  const now = new Date();
  list.forEach(d => {
    const due = new Date(d.due_at);
    const status = due < now ? "Closed" : "Open";
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${d.title}</td>
      <td>${d.type}</td>
      <td>${d.project || ""}</td>
      <td>${d.due_at}</td>
      <td>${status}</td>
    `;
    tbody.appendChild(tr);
  });
})
.catch(()=>{
  document.querySelector("#deadlinesTable tbody").innerHTML = "<tr><td colspan='5'>Error loading</td></tr>";
});
