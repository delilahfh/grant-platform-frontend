
document.getElementById("receiptForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  const payload = {
    recipient: document.getElementById("recipient").value,
    date: document.getElementById("date").value,
    items: document.getElementById("items").value.split("\n").filter(x=>x.trim())
  };

  const res = await fetch("https://grant-app-backend.onrender.com/certificate-of-receipt", {
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
    a.download = "Certificate_of_Receipt.docx";
    a.click();
  } else {
    alert("Error generating certificate");
  }
});
