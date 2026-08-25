/**
 * IIT Bombay Student Placement Portal - Controller & Interactive Logic
 */

let currentSectorFilter = "all";
let currentSearchQuery = "";
let currentCgpaFilter = "all";
let currentSortBy = "recommended";
let activeTab = "explore";

document.addEventListener("DOMContentLoaded", () => {
  initPortal();
  setupEventListeners();
});

function initPortal() {
  const state = getAppState();
  renderStudentProfile(state.student);
  renderStats(state.student.stats);
  renderJAFs();
  renderInterviews(state.upcomingInterviews);
  renderAnnouncements(state.announcements);
  renderResumeDrawer(state.student.resumes);
  renderApplicationsList();
}

function setupEventListeners() {
  // Navigation Tabs
  document.querySelectorAll(".nav-tab-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const tab = e.currentTarget.dataset.tab;
      switchTab(tab);
    });
  });

  // Search Input
  const searchInput = document.getElementById("job-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentSearchQuery = e.target.value.toLowerCase().trim();
      renderJAFs();
    });
  }

  // Sector Filter Pills
  document.querySelectorAll(".sector-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      document.querySelectorAll(".sector-btn").forEach(b => b.classList.remove("active"));
      e.currentTarget.classList.add("active");
      currentSectorFilter = e.currentTarget.dataset.sector;
      renderJAFs();
    });
  });

  // CGPA Filter
  const cgpaSelect = document.getElementById("cgpa-filter-select");
  if (cgpaSelect) {
    cgpaSelect.addEventListener("change", (e) => {
      currentCgpaFilter = e.target.value;
      renderJAFs();
    });
  }

  // Sort By
  const sortSelect = document.getElementById("sort-filter-select");
  if (sortSelect) {
    sortSelect.addEventListener("change", (e) => {
      currentSortBy = e.target.value;
      renderJAFs();
    });
  }

  // Modal Close buttons
  document.querySelectorAll(".modal-close-trigger").forEach(btn => {
    btn.addEventListener("click", closeModal);
  });

  // Close modal on background click
  const modalOverlay = document.getElementById("jaf-modal");
  if (modalOverlay) {
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) closeModal();
    });
  }

  const resumeModal = document.getElementById("resume-modal");
  if (resumeModal) {
    resumeModal.addEventListener("click", (e) => {
      if (e.target === resumeModal) resumeModal.classList.remove("active");
    });
  }
}

function switchTab(tabId) {
  activeTab = tabId;
  document.querySelectorAll(".nav-tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabId);
  });

  document.querySelectorAll(".tab-panel").forEach(panel => {
    panel.classList.remove("active");
  });

  const activePanel = document.getElementById(`panel-${tabId}`);
  if (activePanel) {
    activePanel.classList.add("active");
  }

  if (tabId === "applications") {
    renderApplicationsList();
  }
}

// -------------------------------------------------------------
// RENDERING FUNCTIONS
// -------------------------------------------------------------

function renderStudentProfile(student) {
  const nameEl = document.getElementById("student-name-display");
  const metaEl = document.getElementById("student-meta-display");
  const cgpaEl = document.getElementById("student-cpi-val");
  const headerName = document.getElementById("header-user-name");
  const headerRoll = document.getElementById("header-user-roll");

  if (nameEl) nameEl.textContent = student.name;
  if (metaEl) metaEl.textContent = `${student.degree} • ${student.specialization}`;
  if (cgpaEl) cgpaEl.textContent = student.cgpa;
  if (headerName) headerName.textContent = student.name;
  if (headerRoll) headerRoll.textContent = student.rollNumber;
}

function renderStats(stats) {
  const appliedEl = document.getElementById("stat-applied-count");
  const shortlistedEl = document.getElementById("stat-shortlisted-count");
  const interviewsEl = document.getElementById("stat-interviews-count");
  const offersEl = document.getElementById("stat-offers-count");

  if (appliedEl) appliedEl.textContent = stats.applied;
  if (shortlistedEl) shortlistedEl.textContent = stats.shortlisted;
  if (interviewsEl) interviewsEl.textContent = stats.interviews;
  if (offersEl) offersEl.textContent = stats.offers;
}

function renderJAFs() {
  const container = document.getElementById("jaf-list-container");
  const countBadge = document.getElementById("jaf-count-badge");
  if (!container) return;

  const state = getAppState();
  let list = [...state.jafs];

  // 1. Sector Filter
  if (currentSectorFilter !== "all") {
    list = list.filter(j => j.sector.toLowerCase().includes(currentSectorFilter.toLowerCase()));
  }

  // 2. Search Query
  if (currentSearchQuery) {
    list = list.filter(j => 
      j.company.toLowerCase().includes(currentSearchQuery) ||
      j.role.toLowerCase().includes(currentSearchQuery) ||
      j.location.toLowerCase().includes(currentSearchQuery) ||
      j.description.toLowerCase().includes(currentSearchQuery)
    );
  }

  // 3. CGPA Filter
  if (currentCgpaFilter !== "all") {
    const studentCgpa = parseFloat(state.student.cgpa);
    if (currentCgpaFilter === "eligible") {
      list = list.filter(j => studentCgpa >= j.cgpaCutoff);
    } else {
      const minVal = parseFloat(currentCgpaFilter);
      list = list.filter(j => j.cgpaCutoff <= minVal);
    }
  }

  // 4. Sorting
  if (currentSortBy === "ctc_desc") {
    list.sort((a, b) => extractNumericCtc(b.ctc) - extractNumericCtc(a.ctc));
  } else if (currentSortBy === "deadline") {
    list.sort((a, b) => new Date(a.deadlineTime) - new Date(b.deadlineTime));
  }

  if (countBadge) {
    countBadge.textContent = `${list.length} Openings`;
  }

  if (list.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 3rem 1.5rem; background: var(--bg-card); border-radius: var(--radius-md); border: 1px solid var(--border-card);">
        <p style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 0.5rem;">No job openings match your current search & filters.</p>
        <button class="btn btn-secondary btn-sm" onclick="resetFilters()">Reset All Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = list.map(jaf => {
    const isApplied = jaf.applied;
    let cardClass = "";
    let badgeHtml = "";

    if (jaf.status === "Interview Scheduled") {
      cardClass = "is-interview";
      badgeHtml = `<span class="status-badge badge-interview">⚡ Interview Scheduled</span>`;
    } else if (jaf.status === "Shortlisted") {
      cardClass = "is-shortlisted";
      badgeHtml = `<span class="status-badge badge-shortlisted">✓ Shortlisted</span>`;
    } else if (isApplied) {
      cardClass = "is-applied";
      badgeHtml = `<span class="status-badge badge-applied">Application Submitted</span>`;
    } else {
      badgeHtml = `<span class="status-badge badge-open">Open for Phase 1</span>`;
    }

    return `
      <div class="jaf-card ${cardClass}" id="card-${jaf.id}">
        <div class="jaf-card-header">
          <div class="company-brand-meta">
            <div class="company-logo-wrap">
              <img src="${jaf.logo}" alt="${jaf.company} Logo" class="company-logo-img" onerror="this.onerror=null; this.parentElement.innerHTML='<div class=\\'company-logo-fallback\\'>${jaf.logoFallback}</div>';">
            </div>
            <div class="company-title-wrap">
              <h3>${jaf.role}</h3>
              <p>
                <strong style="color: #fff;">${jaf.company}</strong>
                <span>•</span>
                <span>${jaf.location}</span>
              </p>
            </div>
          </div>
          <div>${badgeHtml}</div>
        </div>

        <div class="jaf-details-grid">
          <div class="detail-item">
            <span class="label">Package (CTC)</span>
            <span class="value ctc-val">${jaf.ctc}</span>
          </div>
          <div class="detail-item">
            <span class="label">Min. CGPA Cutoff</span>
            <span class="value">${jaf.cgpaCutoff} / 10.0</span>
          </div>
          <div class="detail-item">
            <span class="label">Hiring Slot</span>
            <span class="value" style="color: #cbd5e1;">${jaf.slot}</span>
          </div>
          <div class="detail-item">
            <span class="label">Sector Domain</span>
            <span class="value" style="color: #93c5fd;">${jaf.sector}</span>
          </div>
        </div>

        <div class="jaf-branches">
          <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Eligible:</span>
          ${jaf.branches.map(b => `<span class="branch-tag">${b}</span>`).join("")}
        </div>

        <div class="jaf-card-footer">
          <div class="deadline-notice">
            <span>⏰</span>
            <span>Application Deadline: <strong>${jaf.deadline}</strong></span>
          </div>
          <div class="jaf-actions">
            <button class="btn btn-secondary btn-sm" onclick="openJAFDetailsModal('${jaf.id}')">
              View JAF Details
            </button>
            ${
              isApplied
                ? `<button class="btn btn-applied btn-sm">
                     <span>✓</span> Applied
                   </button>`
                : `<button class="btn btn-primary btn-sm" onclick="handleApply('${jaf.id}')">
                     Apply with Verified Resume
                   </button>`
            }
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function extractNumericCtc(ctcStr) {
  if (ctcStr.includes("Cr")) return 142;
  const match = ctcStr.match(/₹?([\d.]+)\s*LPA/);
  return match ? parseFloat(match[1]) : 0;
}

function resetFilters() {
  currentSectorFilter = "all";
  currentSearchQuery = "";
  currentCgpaFilter = "all";
  currentSortBy = "recommended";

  const searchInput = document.getElementById("job-search-input");
  if (searchInput) searchInput.value = "";

  const cgpaSelect = document.getElementById("cgpa-filter-select");
  if (cgpaSelect) cgpaSelect.value = "all";

  const sortSelect = document.getElementById("sort-filter-select");
  if (sortSelect) sortSelect.value = "recommended";

  document.querySelectorAll(".sector-btn").forEach(b => {
    b.classList.toggle("active", b.dataset.sector === "all");
  });

  renderJAFs();
}

// -------------------------------------------------------------
// INTERVIEW SCHEDULE & ANNOUNCEMENTS
// -------------------------------------------------------------

function renderInterviews(interviews) {
  const container = document.getElementById("upcoming-interviews-list");
  if (!container) return;

  if (interviews.length === 0) {
    container.innerHTML = `<p style="font-size: 0.8rem; color: var(--text-muted);">No upcoming interviews scheduled yet.</p>`;
    return;
  }

  container.innerHTML = interviews.map(item => `
    <div class="timeline-item ${item.type.includes('Superday') ? 'superday' : ''}">
      <div class="timeline-company">${item.company}</div>
      <div class="timeline-round">${item.round}</div>
      <div class="timeline-meta">
        <span>📅 ${item.date}</span>
        <span>•</span>
        <span>⏱️ ${item.time}</span>
      </div>
      <div style="font-size: 0.72rem; color: var(--text-secondary); margin-top: 0.2rem;">
        📍 ${item.location}
      </div>
      <a href="${item.meetingLink}" target="_blank" class="timeline-link">
        <span>🔗 Join Video Room / Slot Link</span>
      </a>
    </div>
  `).join("");
}

function renderAnnouncements(announcements) {
  const container = document.getElementById("announcements-list-container");
  if (!container) return;

  container.innerHTML = announcements.map(ann => `
    <div class="announcement-item">
      <div class="announcement-top">
        <span class="ann-tag ${ann.tagType}">${ann.tag}</span>
        <span class="ann-time">${ann.time}</span>
      </div>
      <div class="ann-title">${ann.title}</div>
      <div class="ann-content">${ann.content}</div>
    </div>
  `).join("");
}

function renderResumeDrawer(resumes) {
  const container = document.getElementById("resume-list-container");
  if (!container) return;

  container.innerHTML = resumes.map(res => `
    <div class="resume-item-row">
      <div class="resume-info">
        <span class="resume-pdf-icon">📄</span>
        <div>
          <div class="resume-name" title="${res.name}">${res.name}</div>
          <div style="font-size: 0.68rem; color: #34d399;">✓ ${res.verifiedBy}</div>
        </div>
      </div>
      <button class="btn btn-secondary btn-sm" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="viewResumeModal('${res.name}')">
        View
      </button>
    </div>
  `).join("");
}

// -------------------------------------------------------------
// APPLICATIONS TAB VIEW
// -------------------------------------------------------------

function renderApplicationsList() {
  const container = document.getElementById("applications-table-body");
  if (!container) return;

  const state = getAppState();
  const appliedJafs = state.jafs.filter(j => j.applied);

  if (appliedJafs.length === 0) {
    container.innerHTML = `<tr><td colspan="5" style="text-align:center; color: var(--text-muted); padding: 2rem;">No applications submitted yet.</td></tr>`;
    return;
  }

  container.innerHTML = appliedJafs.map(j => {
    let statusClass = "badge-applied";
    if (j.status === "Interview Scheduled") statusClass = "badge-interview";
    if (j.status === "Shortlisted") statusClass = "badge-shortlisted";

    return `
      <tr>
        <td>
          <div style="font-weight: 700; color: #fff;">${j.company}</div>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">${j.location}</div>
        </td>
        <td>
          <div style="font-weight: 600;">${j.role}</div>
          <div style="font-size: 0.75rem; color: var(--accent-cyan); font-family: 'Outfit';">${j.ctc}</div>
        </td>
        <td>${j.slot}</td>
        <td><span class="status-badge ${statusClass}">${j.status}</span></td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="openJAFDetailsModal('${j.id}')">View JAF</button>
        </td>
      </tr>
    `;
  }).join("");
}

// -------------------------------------------------------------
// ACTIONS & MODALS
// -------------------------------------------------------------

function handleApply(jafId) {
  const state = getAppState();
  const jaf = state.jafs.find(j => j.id === jafId);
  if (!jaf) return;

  jaf.applied = true;
  jaf.status = "Applied";
  jaf.applicationDate = new Date().toISOString().split("T")[0];
  state.student.stats.applied += 1;

  saveAppState(state);

  // Re-render UI
  renderStats(state.student.stats);
  renderJAFs();
  renderApplicationsList();

  showToast(`✅ Successfully applied to ${jaf.company} (${jaf.role})! Application submitted to DPC.`);
}

function openJAFDetailsModal(jafId) {
  const state = getAppState();
  const jaf = state.jafs.find(j => j.id === jafId);
  if (!jaf) return;

  const modal = document.getElementById("jaf-modal");
  const title = document.getElementById("modal-jaf-title");
  const body = document.getElementById("modal-jaf-body");
  const footer = document.getElementById("modal-jaf-footer");

  if (!modal || !body) return;

  title.innerHTML = `
    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <div class="company-logo-wrap" style="width: 36px; height: 36px;">
        <img src="${jaf.logo}" alt="${jaf.company}" class="company-logo-img" onerror="this.onerror=null; this.parentElement.innerHTML='${jaf.logoFallback}';">
      </div>
      <div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #fff;">${jaf.role}</div>
        <div style="font-size: 0.8rem; color: var(--text-secondary);">${jaf.company} • ${jaf.location}</div>
      </div>
    </div>
  `;

  body.innerHTML = `
    <div>
      <h4 style="color: var(--accent-cyan); font-size: 0.95rem; margin-bottom: 0.5rem;">Job Description</h4>
      <p style="color: var(--text-secondary); font-size: 0.88rem; line-height: 1.6;">${jaf.description}</p>
    </div>

    <div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
      <h4 style="color: var(--text-primary); font-size: 0.88rem; margin-bottom: 0.5rem; text-transform: uppercase;">Compensation Structure</h4>
      <div style="font-size: 1.1rem; font-family: 'Outfit'; color: #38bdf8; font-weight: 700; margin-bottom: 0.35rem;">Total CTC: ${jaf.ctc}</div>
      <div style="font-size: 0.82rem; color: var(--text-secondary);">${jaf.ctcFull}</div>
    </div>

    <div>
      <h4 style="color: var(--text-primary); font-size: 0.95rem; margin-bottom: 0.5rem;">Selection Rounds & Timeline</h4>
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        ${jaf.process.map(p => `
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0.85rem; background: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div>
              <div style="font-size: 0.85rem; font-weight: 600; color: #fff;">${p.step}</div>
              <div style="font-size: 0.75rem; color: var(--text-secondary);">${p.details || ''}</div>
            </div>
            <div style="font-size: 0.75rem; color: var(--accent-cyan); font-family: 'JetBrains Mono';">${p.date}</div>
          </div>
        `).join("")}
      </div>
    </div>

    <div>
      <h4 style="color: var(--text-primary); font-size: 0.95rem; margin-bottom: 0.5rem;">Key Requirements</h4>
      <ul style="padding-left: 1.25rem; color: var(--text-secondary); font-size: 0.85rem; line-height: 1.6;">
        ${jaf.requirements.map(req => `<li>${req}</li>`).join("")}
      </ul>
    </div>
  `;

  footer.innerHTML = `
    <button class="btn btn-secondary" onclick="closeModal()">Close</button>
    ${
      jaf.applied
        ? `<button class="btn btn-applied" disabled>✓ Application Submitted</button>`
        : `<button class="btn btn-primary" onclick="handleApply('${jaf.id}'); closeModal();">Submit Application (Verified Master Resume)</button>`
    }
  `;

  modal.classList.add("active");
}

function closeModal() {
  const modal = document.getElementById("jaf-modal");
  if (modal) modal.classList.remove("active");
}

function viewResumeModal(resumeName) {
  const modal = document.getElementById("resume-modal");
  const textEl = document.getElementById("resume-modal-filename");
  if (textEl) textEl.textContent = resumeName;
  if (modal) modal.classList.add("active");
}

function showToast(message) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
