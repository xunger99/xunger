function fmtSize(bytes) {
  if (!bytes) return '';
  const units = ['B', 'KB', 'MB', 'GB'];
  let n = bytes;
  let i = 0;
  while (n >= 1024 && i < units.length - 1) {
    n /= 1024;
    i++;
  }
  return `${n.toFixed(n >= 10 || i === 0 ? 0 : 1)} ${units[i]}`;
}

function esc(s) {
  return String(s ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function lectureCard(lec) {
  const no = String(lec.no).padStart(2, '0');
  const hasPdf = !!lec.pdf;
  const topics = (lec.topics || [])
    .map(t => `<li>${esc(t)}</li>`)
    .join('');

  const status = hasPdf
    ? `<span class="status ready">Material available</span>`
    : `<span class="status pending">To be added</span>`;

  const download = hasPdf
    ? `<a class="download-btn" href="${esc(lec.pdf)}" download>Download PDF</a>`
    : `<span class="download-btn disabled">Reserved for later</span>`;

  const extraDownloads = (lec.extraDownloads || [])
    .map(item => `<a class="download-btn ghost" href="${esc(item.file)}" download>${esc(item.label)}</a>`)
    .join('');

  return `
    <article class="lecture-card modern ${hasPdf ? '' : 'is-pending'}" id="${esc(lec.id || 'lecture-' + no)}">
      <div class="lecture-no">
        <span>Lecture</span>
        <strong>${no}</strong>
      </div>

      <div class="lecture-main">
        <div class="lecture-topline">
          <span class="kicker">Class ${lec.no}</span>
          ${status}
        </div>

        <h3>${esc(lec.title)}</h3>
        <p class="lecture-focus">${esc(lec.focus)}</p>

        ${topics ? `<ul class="clean">${topics}</ul>` : ''}

        <p class="lab-line">
          <strong>Lab focus:</strong> ${esc(lec.lab || 'This session is reserved for later release.')}
        </p>

        <div class="downloads">
          ${download}
          ${extraDownloads}
        </div>
      </div>
    </article>
  `;
}

function codeCard(pkg) {
  const tags = (pkg.tags || [])
    .map(t => `<span class="pill">${esc(t)}</span>`)
    .join('');

  return `
    <article class="card code-card modern">
      <div class="code-card-head">
        <span class="kicker">Class ${esc(pkg.classNo)}</span>
        <span class="status ready">ZIP package</span>
      </div>

      <h3>${esc(pkg.title)}</h3>
      <p>${esc(pkg.description)}</p>

      <div class="pill-row">${tags}</div>

      <div class="downloads">
        <a class="download-btn" href="${esc(pkg.file)}" download>
          Download ZIP ${pkg.size ? '(' + fmtSize(pkg.size) + ')' : ''}
        </a>
      </div>
    </article>
  `;
}

function taskRow(task) {
  return `
    <tr>
      <td>Class ${esc(task.classNo)}</td>
      <td>${esc(task.title)}</td>
      <td>${esc(task.deliverable)}</td>
      <td>${esc(task.emphasis)}</td>
    </tr>
  `;
}

function setActiveNav() {
  const current = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === current || (current === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setActiveNav();

  const lectures = document.querySelector('[data-lectures]');
  if (lectures) {
    lectures.innerHTML = COURSE_DATA.lectures.map(lectureCard).join('');
  }

  const code = document.querySelector('[data-code]');
  if (code) {
    code.innerHTML = COURSE_DATA.codePackages.map(codeCard).join('');
  }

  const tasks = document.querySelector('[data-tasks]');
  if (tasks) {
    tasks.innerHTML = COURSE_DATA.tasks.map(taskRow).join('');
  }

  const homeLectures = document.querySelector('[data-home-lectures]');
  if (homeLectures) {
    homeLectures.innerHTML = COURSE_DATA.lectures.slice(0, 3).map(lectureCard).join('');
  }
});
