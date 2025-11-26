
document.getElementById("finReportForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  let exp;
  try { exp = JSON.parse(document.getElementById("exp").value); }
  catch { alert("Invalid JSON"); return; }

  const payload = { expenditures: exp };

  const res = await fetch("https://grant-app-backend.onrender.com/financial-report", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if(res.ok){
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Financial_Report.xlsx";
    a.click();
  } else {
    alert("Error generating report");
  }
});
