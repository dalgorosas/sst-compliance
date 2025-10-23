const urlParams = new URLSearchParams(window.location.search);
const pdfId = urlParams.get('id') || 1;

const pdfjsLib = window['pdfjs-dist/build/pdf'];
pdfjsLib.GlobalWorkerOptions.workerSrc = 'pdfjs/pdf.worker.js';

let pdfDoc = null,
    pageNum = 1,
    pageRendering = false,
    canvas = document.getElementById('pdf-render'),
    ctx = canvas.getContext('2d');

async function renderPage(num) {
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
  const response = await fetch(`/api/v1/pdf/${pdfId}`);
  const data = await response.json();
  const pdfUrl = `/storage/pdfs/${data.ruta}`;
  const pdf = await pdfjsLib.getDocument(pdfUrl).promise;
  pdfDoc = pdf;
  document.getElementById('page-count').textContent = pdfDoc.numPages;
  renderPage(pageNum);
  loadHistorial();
}

function nextPage() {
  if (pageNum >= pdfDoc.numPages) return;
  pageNum++;
  renderPage(pageNum);
}

function prevPage() {
  if (pageNum <= 1) return;
  pageNum--;
  renderPage(pageNum);
}

async function loadHistorial() {
  const res = await fetch(`/api/v1/pdf/${pdfId}/historial`);
  const historial = await res.json();
  const ul = document.getElementById('historial');
  ul.innerHTML = '';
  historial.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${item.fecha}</strong><br>${item.generado_por}`;
    ul.appendChild(li);
  });
}

document.getElementById('next-page').addEventListener('click', nextPage);
document.getElementById('prev-page').addEventListener('click', prevPage);
document.getElementById('download-pdf').addEventListener('click', () => {
  window.open(`/api/v1/pdf/${pdfId}/download`, '_blank');
});

loadPDF();
