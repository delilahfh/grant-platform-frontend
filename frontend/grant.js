
document.getElementById("grantForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  const payload = {
    signatory_name: document.getElementById("signName").value,
    passport_number: document.getElementById("passport").value,
    date_of_birth: document.getElementById("dob").value,
    entity_name: document.getElementById("entity").value,
    entity_registration_number: document.getElementById("regNum").value
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
