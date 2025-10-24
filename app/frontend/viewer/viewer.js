// Parámetros: ?id=123  o  /viewer/<id> si lo sirves con routing aparte
const url = new URL(window.location.href);
const docId = url.searchParams.get("id") || (function(){
  // fallback si vives en /viewer/1
  const parts = location.pathname.split("/").filter(Boolean);
  const last = parts[parts.length-1];
  return /^\d+$/.test(last) ? last : 1;
})();

const authToken = localStorage.getItem("sst.token");

const pdfjsLib = window['pdfjs-dist/build/pdf'];
if (pdfjsLib) {
  pdfjsLib.GlobalWorkerOptions.workerSrc = 'pdfjs/pdf.worker.js';
}

async function getJSON(u){
  const headers = {};
  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }
  const r = await fetch(u, { headers });
  if(!r.ok) throw new Error(r.status);
  return r.json();
}
const fmt = (d)=> new Date(d).toLocaleString();
const bytes = (n)=> {
  const x = Number(n||0);
  if (x<1024) return x+" B";
  if (x<1024**2) return (x/1024).toFixed(1)+" KB";
  if (x<1024**3) return (x/1024**2).toFixed(1)+" MB";
  return (x/1024**3).toFixed(1)+" GB";
};

async function load() {
  // 1) listar documentos para ubicar nuestro doc y métricas
  // si ya tienes endpoint GET /api/v1/pdf/{id} que descarga, usamos /api/v1/pdf para metadata
  const list = await getJSON(`/api/v1/pdf`);
  const doc = list.find(d=> String(d.id)===String(docId));
  if (!doc) {
    document.getElementById("doc-title").textContent = "Documento no encontrado";
    return;
  }

  // 2) título y meta
  document.getElementById("doc-title").textContent = doc.nombre;
  document.getElementById("doc-meta").textContent = `Etiqueta: ${doc.etiqueta || "-"} • Actualizado: ${fmt(doc.actualizado_en)}`;
  document.getElementById("kpi-tag").textContent = doc.etiqueta || "-";
  document.getElementById("kpi-size").textContent = bytes(doc.tamano_bytes || 0);

  // 3) historial
  const hist = await getJSON(`/api/v1/pdf/${doc.id}/historial`);
  const ul = document.getElementById("historial");
  ul.innerHTML = "";
  let latestVersion = 1, latestHash = "-";
  hist.forEach(h=>{
    latestVersion = Math.max(latestVersion, h.version||1);
    latestHash = h.hash_sha256 || latestHash;
    const li = document.createElement("li");
    li.innerHTML = `<strong>v${h.version}</strong> — ${h.generado_por || "-"}<br>
                    <small>${fmt(h.creado_en)} • ${h.descripcion || ""}</small>`;
    ul.appendChild(li);
  });
  document.getElementById("kpi-version").textContent = latestVersion;
  document.getElementById("kpi-hash").textContent = latestHash;

  // 4) visor PDF (usamos el último archivo que apunta doc.ruta_relativa)
  const filename = (doc.ruta_relativa || "").split(/[\\/]/).pop();
  const frame = document.getElementById("pdf-frame");
  frame.src = `/files/${filename}#zoom=page-width`;
  const download = document.getElementById("btn-descargar");
  download.href = `/api/v1/pdf/${doc.id}/download`;
  if (authToken) {
    download.addEventListener("click", async (event) => {
      event.preventDefault();
      try {
        const response = await fetch(`/api/v1/pdf/${doc.id}/download`, {
          headers: { Authorization: `Bearer ${authToken}` },
        });
        if (!response.ok) {
          throw new Error(response.status);
        }
        const blob = await response.blob();
        const objectUrl = URL.createObjectURL(blob);
        const tmp = document.createElement("a");
        tmp.href = objectUrl;
        tmp.download = `${doc.nombre || "documento"}.pdf`;
        document.body.appendChild(tmp);
        tmp.click();
        tmp.remove();
        URL.revokeObjectURL(objectUrl);
      } catch (error) {
        console.error(error);
        alert("No se pudo descargar el archivo");
      }
    });
  }
}

load().catch(console.error);
