
document.getElementById("amendForm").addEventListener("submit", async (e)=>{
    e.preventDefault();

    const token = localStorage.getItem("jwt");
    if(!token){ window.location.href="login.html"; return; }

    let fin, nar;
    try { fin = JSON.parse(document.getElementById("financial").value); }
    catch { alert("Invalid financial JSON"); return; }

    try { nar = JSON.parse(document.getElementById("narrative").value); }
    catch { alert("Invalid narrative JSON"); return; }

    const payload = {
        justification: document.getElementById("justification").value,
        financial_changes: fin,
        narrative_changes: nar
    };

    const res = await fetch("https://grant-app-backend.onrender.com/financial-amendment", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            Authorization:`Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    if(res.ok){
        alert("Amendment request submitted!");
        window.location.href="participant_dashboard.html";
    } else {
        alert("Error submitting amendment");
    }
});
