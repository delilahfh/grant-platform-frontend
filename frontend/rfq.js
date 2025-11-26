
document.getElementById("rfqForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  const payload = {
    procurement_type: document.getElementById("procType").value,
    description: document.getElementById("description").value.trim(),
    supplier_prices: {
      supplier1: document.getElementById("s1").value,
      supplier2: document.getElementById("s2").value,
      supplier3: document.getElementById("s3").value
    }
  };

  const res = await fetch("https://grant-app-backend.onrender.com/request-for-quotation", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if(res.ok){
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "RFQ.docx";
    a.click();
  } else {
    alert("Error generating RFQ");
  }
});
