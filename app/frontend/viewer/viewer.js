const urlParams = new URLSearchParams(window.location.search);
const pathSegments = window.location.pathname.split('/').filter(Boolean);
let requestedId = urlParams.get('id');

if (!requestedId && pathSegments.length) {
  const candidate = pathSegments[pathSegments.length - 1];
  if (!Number.isNaN(Number.parseInt(candidate, 10))) {
    requestedId = candidate;
  }
}

const pdfId = Number.parseInt(requestedId ?? '', 10) || 1;

const pdfjsLib = window['pdfjs-dist/build/pdf'];
pdfjsLib.GlobalWorkerOptions.workerSrc = 'pdfjs/pdf.worker.js';

let pdfDoc = null;
let pageNum = 1;
let pageRendering = false;
const canvas = document.getElementById('pdf-render');
const ctx = canvas.getContext('2d');

function showError(message) {
  const container = document.getElementById('viewer-container');
  if (container) {
    container.innerHTML = `<p class="viewer-error">${message}</p>`;
  }
}

async function renderPage(num) {
  if (!pdfDoc) {
    return;
  }

  pageRendering = true;
  const page = await pdfDoc.getPage(num);
  const viewport = page.getViewport({ scale: 1.5 });
  canvas.height = viewport.height;
  canvas.width = viewport.width;
  await page.render({ canvasContext: ctx, viewport: viewport }).promise;
  document.getElementById('page-num').textContent = num;
  pageRendering = false;
}

async function loadPDF() {
  try {
    const response = await fetch(`/api/v1/pdf/${pdfId}`);
    if (!response.ok) {
      throw new Error('metadata-response');
    }

    const data = await response.json();
    const archivo = data.archivo || data.ruta_relativa;
    if (!archivo) {
      throw new Error('missing-file-reference');
    }

    const pdfUrl = `/files/${encodeURIComponent(archivo)}`;
    const pdf = await pdfjsLib.getDocument(pdfUrl).promise;
    pdfDoc = pdf;
    document.getElementById('page-count').textContent = pdfDoc.numPages;
    document.getElementById('download-pdf').dataset.href = `/api/v1/pdf/${pdfId}/download`;
    await renderPage(pageNum);
    await loadHistorial();
  } catch (error) {
    console.error('Error cargando el PDF', error);
    showError('No se pudo cargar el documento solicitado.');
  }
}

function nextPage() {
  if (!pdfDoc || pageNum >= pdfDoc.numPages) return;
  pageNum++;
  renderPage(pageNum);
}

function prevPage() {
  if (!pdfDoc || pageNum <= 1) return;
  pageNum--;
  renderPage(pageNum);
}

async function loadHistorial() {
  try {
    const res = await fetch(`/api/v1/pdf/${pdfId}/historial`);
    if (!res.ok) {
      throw new Error('historial-response');
    }
    const historial = await res.json();
    const ul = document.getElementById('historial');
    if (!ul) return;

    ul.innerHTML = '';
    historial.forEach((item) => {
      const li = document.createElement('li');
      const fecha = item.fecha || item.creado_en || '';
      const generadoPor = item.generado_por || '';
      li.innerHTML = `<strong>${fecha}</strong><br>${generadoPor}`;
      ul.appendChild(li);
    });
  } catch (error) {
    console.error('Error cargando el historial', error);
  }
}

document.getElementById('next-page').addEventListener('click', nextPage);
document.getElementById('prev-page').addEventListener('click', prevPage);
document.getElementById('download-pdf').addEventListener('click', () => {
  const link = document.getElementById('download-pdf').dataset.href || `/api/v1/pdf/${pdfId}/download`;
  window.open(link, '_blank');
});

loadPDF();
