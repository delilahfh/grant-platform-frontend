
document.getElementById("deliveryForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  const payload = {
    supplier: document.getElementById("supplier").value,
    date: document.getElementById("date").value,
    items: document.getElementById("items").value.split("\n").filter(x=>x.trim())
  };

  const res = await fetch("https://grant-app-backend.onrender.com/delivery-certificate", {
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
    a.download = "Delivery_Certificate.docx";
    a.click();
  } else {
    alert("Error generating certificate");
  }
});
