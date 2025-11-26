
document.getElementById("contractForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if (!token){ window.location.href="login.html"; return; }

  const payload = {
    signatory: document.getElementById("signName").value,
    passport: document.getElementById("passport").value,
    dob: document.getElementById("dob").value,
    entity_name: document.getElementById("entity").value,
    entity_registration: document.getElementById("reg").value
  };

  const res = await fetch("https://grant-app-backend.onrender.com/grant-contract", {
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
    a.download = "Grant_Contract.docx";
    a.click();
  } else {
    alert("Error generating contract");
  }
});
