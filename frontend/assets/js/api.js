const BASE_URL = "https://grant-app-backend.onrender.com";

function getToken() {
  return window.localStorage.getItem("token") || "";
}
function setToken(token) {
  window.localStorage.setItem("token", token);
}
function getRole() {
  return window.localStorage.getItem("role") || "";
}
function setRole(role) {
  window.localStorage.setItem("role", role);
}

async function postJSON(path, data) {
  const res = await fetch(BASE_URL + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": getToken() ? "Bearer " + getToken() : undefined
    },
    body: JSON.stringify(data || {})
  });
  const text = await res.text();
  try { return JSON.parse(text); } catch { return { raw: text, status: res.status }; }
}

async function uploadFiles(path, formData) {
  if (!(formData instanceof FormData)) {
    const fd = new FormData();
    for (const [k, v] of Object.entries(formData)) {
      if (Array.isArray(v)) v.forEach(f => fd.append(k, f));
      else fd.append(k, v);
    }
    formData = fd;
  }
  const res = await fetch(BASE_URL + path, {
    method: "POST",
    headers: {
      "Authorization": getToken() ? "Bearer " + getToken() : undefined
    },
    body: formData
  });
  const text = await res.text();
  try { return JSON.parse(text); } catch { return { raw: text, status: res.status }; }
}

function requireAuth() {
  if (!getToken()) {
    window.location.hash = "#/login";
    return false;
  }
  return true;
}

function showNotice(type, msg) {
  const app = document.getElementById("app");
  if (!app) return;
  const div = document.createElement("div");
  div.className = "notice " + type;
  div.textContent = msg;
  app.prepend(div);
  setTimeout(() => div.remove(), 4000);
}
