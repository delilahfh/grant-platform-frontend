
document.getElementById("fundForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  const payload = {
    amount_number: document.getElementById("amount").value,
    amount_text: document.getElementById("amountText").value,
    account_name: document.getElementById("accName").value,
    account_number: document.getElementById("accNumber").value,
    iban: document.getElementById("iban").value,
    swift: document.getElementById("swift").value,
    bank: document.getElementById("bank").value
  };

  const res = await fetch("https://grant-app-backend.onrender.com/fund-request", {
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
    a.download = "Request_for_Instalment.docx";
    a.click();
  } else {
    alert("Error generating request");
  }
});
