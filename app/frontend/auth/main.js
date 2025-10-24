const messages = document.getElementById("messages");
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

function showMessage(text, type = "") {
  messages.innerHTML = "";
  if (!text) return;
  const p = document.createElement("p");
  p.textContent = text;
  if (type) {
    p.classList.add(type);
  }
  messages.appendChild(p);
}

async function sendJSON(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const errorMessage = detail?.detail || `Error ${response.status}`;
    throw new Error(errorMessage);
  }
  return response.json();
}

loginForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  showMessage("Procesando…");
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form));
  try {
    const result = await sendJSON("/api/v1/auth/login", payload);
    const token = result?.token?.access_token;
    if (token) {
      localStorage.setItem("sst.token", token);
    }
    showMessage("Inicio de sesión correcto, redirigiendo…", "ok");
    setTimeout(() => {
      window.location.href = "/viewer-assets/viewer/index.html";
    }, 600);
  } catch (error) {
    console.error(error);
    showMessage(error.message || "No se pudo iniciar sesión", "error");
  }
});

registerForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  showMessage("Registrando usuario…");
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form));
  try {
    await sendJSON("/api/v1/auth/register", payload);
    showMessage("Usuario registrado correctamente. Puedes iniciar sesión.", "ok");
    form.reset();
  } catch (error) {
    console.error(error);
    showMessage(error.message || "No se pudo registrar el usuario", "error");
  }
});