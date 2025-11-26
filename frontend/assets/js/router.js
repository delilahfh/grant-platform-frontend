const routes = {
  "login": "pages/login.html",
  "register": "pages/register.html",
  "admin/dashboard": "pages/admin_dashboard.html",
  "applicant/dashboard": "pages/applicant_dashboard.html",
  "participant/dashboard": "pages/participant_dashboard.html",
  "proposals/narrative": "pages/proposals_narrative.html",
  "proposals/financial": "pages/proposals_financial.html",
  "supporting-documents": "pages/supporting_documents.html",
  "procurement/rfq": "pages/procurement_rfq.html",
  "delivery-certificate": "pages/procurement_delivery_certificate.html",
  "certificate-of-receipt": "pages/procurement_certificate_of_receipt.html",
  "financial-report": "pages/reports_financial.html",
  "fund-request": "pages/fund_request.html",
  "grant-contract": "pages/grant_contract.html"
};

function buildSidebar() {
  const bar = document.getElementById("sidebar");
  if (!bar) return;
  const role = getRole();
  let html = "<h2>CESVI</h2>";
  if (!getToken()) {
    html += "<a href='#/login'>Login</a><a href='#/register'>Register</a>";
  } else if (role === "admin") {
    html += `
      <a href='#/admin/dashboard'>Dashboard</a>
      <a href='#/grant-contract'>Grant Contracts</a>
      <a href='#/financial-report'>Financial Reports</a>
    `;
  } else if (role === "participant") {
    html += `
      <a href='#/participant/dashboard'>Dashboard</a>
      <a href='#/delivery-certificate'>Delivery Certificates</a>
      <a href='#/certificate-of-receipt'>Certificates of Receipt</a>
      <a href='#/financial-report'>Financial Reports</a>
    `;
  } else { // applicant default
    html += `
      <a href='#/applicant/dashboard'>Dashboard</a>
      <a href='#/proposals/narrative'>Narrative Proposal</a>
      <a href='#/proposals/financial'>Financial Proposal</a>
      <a href='#/supporting-documents'>Supporting Documents</a>
      <a href='#/procurement/rfq'>Procurement: RFQ</a>
      <a href='#/delivery-certificate'>Delivery Certificates</a>
      <a href='#/certificate-of-receipt'>Certificates of Receipt</a>
      <a href='#/fund-request'>Request for Instalment</a>
      <a href='#/financial-report'>Financial Report</a>
    `;
  }
  if (getToken()) {
    html += "<hr><button onclick='logout()' class='secondary'>Logout</button>";
  }
  bar.innerHTML = html;
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  window.location.hash = "#/login";
  buildSidebar();
}

async function loadRoute() {
  const hash = window.location.hash.replace(/^#\//, "") || "login";
  const path = routes[hash] || routes["login"];
  if (hash !== "login" && hash !== "register") {
    if (!requireAuth()) return;
  }
  buildSidebar();
  const res = await fetch(path);
  const html = await res.text();
  const app = document.getElementById("app");
  app.innerHTML = html;
}

window.addEventListener("hashchange", loadRoute);
window.addEventListener("load", loadRoute);
