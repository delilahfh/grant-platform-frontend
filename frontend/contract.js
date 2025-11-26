
document.getElementById("contractForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  let payments;
  try { payments = JSON.parse(document.getElementById("payments").value); }
  catch { alert("Invalid payment schedule JSON"); return; }

  const payload = {
    supplier: document.getElementById("supplier").value,
    description: document.getElementById("description").value,
    total_price: document.getElementById("total").value,
    delivery_time: document.getElementById("delivery").value,
    payments: payments
  };

  const res = await fetch("https://grant-app-backend.onrender.com/procurement-contract", {
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
    a.download = "Procurement_Contract.docx";
    a.click();
  } else {
    alert("Error generating contract");
  }
});
