/**
 * IIT Bombay Student Placement Portal - Django Front-end Controller
 */

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function getCsrfToken() {
  const hiddenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
  if (hiddenInput && hiddenInput.value) {
    return hiddenInput.value;
  }
  return getCookie('csrftoken') || '';
}

document.addEventListener('DOMContentLoaded', () => {
  setupFilterControls();
  setupModals();
  setupNavScrollSpy();
});

function setupNavScrollSpy() {
  if (window.location.pathname.includes('/login') || window.location.pathname.includes('/register')) return;
  const navTabs = document.querySelectorAll('.public-nav-tabs .nav-tab-link');
  if (!navTabs || navTabs.length === 0) return;

  const sectionMap = [
    { id: 'leadership', el: document.getElementById('leadership') },
    { id: 'roadmap', el: document.getElementById('roadmap') },
    { id: 'partners', el: document.getElementById('partners') },
    { id: 'portals', el: document.getElementById('portals') },
    { id: 'about', el: document.getElementById('about') },
    { id: 'home', el: document.getElementById('home') }
  ];

  function setActiveTab(targetId) {
    navTabs.forEach(tab => {
      const href = tab.getAttribute('href') || '';
      if (href === `/#${targetId}` || href === `#${targetId}` || (targetId === 'home' && (href === '/' || href === '/#home' || href === '#home'))) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });
  }

  // Handle click on tabs
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const href = tab.getAttribute('href') || '';
      const hashIndex = href.indexOf('#');
      if (hashIndex !== -1) {
        const hash = href.substring(hashIndex + 1);
        if (document.getElementById(hash)) {
          setActiveTab(hash);
        }
      } else if (href === '/') {
        setActiveTab('home');
      }
    });
  });

  // Check URL hash on page load
  if (window.location.hash) {
    const initialHash = window.location.hash.substring(1);
    if (document.getElementById(initialHash)) {
      setActiveTab(initialHash);
    }
  }

  // ScrollSpy listener as user scrolls down the page
  let scrollTimeout;
  window.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      if (window.scrollY < 120) {
        setActiveTab('home');
        return;
      }
      const scrollPosition = window.scrollY + 130;
      for (const section of sectionMap) {
        if (section.el) {
          const top = section.el.offsetTop;
          if (scrollPosition >= top) {
            setActiveTab(section.id);
            break;
          }
        }
      }
    }, 30);
  }, { passive: true });
}

function setupFilterControls() {
  const searchInput = document.getElementById('job-search-input');
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        document.getElementById('filter-form').submit();
      }, 500);
    });
  }

  const cgpaSelect = document.getElementById('cgpa-filter-select');
  if (cgpaSelect) {
    cgpaSelect.addEventListener('change', () => {
      document.getElementById('filter-form').submit();
    });
  }

  const sortSelect = document.getElementById('sort-filter-select');
  if (sortSelect) {
    sortSelect.addEventListener('change', () => {
      document.getElementById('filter-form').submit();
    });
  }
}

function setupModals() {
  const jafModal = document.getElementById('jaf-modal');
  if (jafModal) {
    jafModal.addEventListener('click', (e) => {
      if (e.target === jafModal) closeModal();
    });
  }

  const resumeModal = document.getElementById('resume-modal');
  if (resumeModal) {
    resumeModal.addEventListener('click', (e) => {
      if (e.target === resumeModal) resumeModal.classList.remove('active');
    });
  }

  const profileModal = document.getElementById('student-profile-modal');
  if (profileModal) {
    profileModal.addEventListener('click', (e) => {
      if (e.target === profileModal) profileModal.classList.remove('active');
    });
  }
}

function openStudentProfileModal() {
  const modal = document.getElementById('student-profile-modal');
  if (modal) modal.classList.add('active');
}

function closeStudentProfileModal() {
  const modal = document.getElementById('student-profile-modal');
  if (modal) modal.classList.remove('active');
}

async function handleApply(jafId) {
  const csrftoken = getCsrfToken();
  const btn = document.getElementById(`apply-btn-${jafId}`);
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span>⏳</span> Submitting...`;
  }

  try {
    const response = await fetch(`/api/apply/${jafId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      }
    });

    const data = await response.json();
    if (data.success) {
      // Update Button
      if (btn) {
        btn.className = 'btn btn-applied btn-sm';
        btn.innerHTML = `<span>✓</span> Applied`;
        const parent = btn.parentElement;
        if (parent && !parent.querySelector(`.track-flow-btn-${jafId}`)) {
          const trackBtn = document.createElement('button');
          trackBtn.type = 'button';
          trackBtn.className = `btn btn-sm track-flow-btn-${jafId}`;
          trackBtn.style.cssText = 'background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-weight: 700; padding: 0.35rem 0.75rem; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; gap: 0.3rem;';
          trackBtn.innerHTML = `<span>📊</span> View More (Hiring Flow) →`;
          trackBtn.onclick = () => openHiringTrackerModal(jafId);
          parent.appendChild(trackBtn);
        }
      }

      // Update Card Styling
      const card = document.getElementById(`card-${jafId}`);
      if (card) {
        card.classList.add('is-applied');
        const badgeSlot = card.querySelector('.jaf-badge-slot');
        if (badgeSlot) {
          badgeSlot.innerHTML = `<span class="status-badge badge-applied">Application Submitted</span>`;
        }
      }

      // Update Stats
      if (data.stats) {
        const appliedStat = document.getElementById('stat-applied-count');
        if (appliedStat) appliedStat.textContent = data.stats.applied;
      }

      showToast(`✅ Successfully applied to <strong>${data.company}</strong> (${data.role})! Document verified.`);
    } else {
      showToast(`⚠️ Could not submit application: ${data.error || 'Please try again.'}`);
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = `Apply with Verified Resume`;
      }
    }
  } catch (error) {
    console.error('Error applying:', error);
    showToast(`❌ Network error while submitting application.`);
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `Apply with Verified Resume`;
    }
  }
}

async function openJAFDetailsModal(jafId) {
  const modal = document.getElementById('jaf-modal');
  const title = document.getElementById('modal-jaf-title');
  const body = document.getElementById('modal-jaf-body');
  const footer = document.getElementById('modal-jaf-footer');

  if (!modal || !body) return;

  modal.style.display = 'flex';
  modal.classList.add('active');
  body.innerHTML = `
    <div style="text-align: center; padding: 3rem 1.5rem; color: #64748b;">
      <div style="font-size: 2.2rem; margin-bottom: 0.75rem; animation: spin 1s infinite linear;">⚙️</div>
      <div style="font-weight: 700; font-size: 1.05rem; color: #0f172a;">Retrieving In-Depth JAF Specifications...</div>
      <p style="font-size: 0.82rem; margin: 0.35rem 0 0; color: #64748b;">Loading compensation breakdown, eligibility criteria, and hiring roadmap.</p>
    </div>
  `;

  try {
    const res = await fetch(`/api/jaf/${jafId}/`);
    const json = await res.json();
    if (!json.success) throw new Error(json.error || "JAF not found");

    const jaf = json.jaf;

    // 1. Header
    title.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.85rem;">
        <div class="company-logo-wrap" style="width: 44px; height: 44px; border-radius: 10px; background: #ffffff; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); flex-shrink: 0;">
          <img src="${jaf.company_logo}" alt="${jaf.company}" class="company-logo-img" style="max-width: 100%; max-height: 100%; object-fit: contain;" onerror="this.onerror=null; this.parentElement.innerHTML='<div style=\\'font-weight:800; color:#1e40af; font-size:0.9rem;\\'>${jaf.company_fallback}</div>';">
        </div>
        <div>
          <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
            <h3 style="font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.2;">${jaf.role}</h3>
            <span style="background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 0.68rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 9999px;">${jaf.sector}</span>
          </div>
          <div style="font-size: 0.82rem; color: #475569; margin-top: 0.15rem; font-weight: 500;">
            <strong style="color: #1e40af;">${jaf.company}</strong> • <span>📍 ${jaf.location}</span> • <span style="color: #64748b;">${jaf.slot}</span>
          </div>
        </div>
      </div>
      <button type="button" class="modal-close-btn" onclick="closeModal()" style="font-size: 1.5rem; width: 36px; height: 36px; border: none; background: #f1f5f9; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #64748b;">&times;</button>
    `;

    // 2. Body
    let roundsHtml = '';
    if (jaf.hiring_rounds && jaf.hiring_rounds.length > 0) {
      roundsHtml = jaf.hiring_rounds.map((r, i) => `
        <div style="display: flex; gap: 0.85rem; padding: 0.75rem 1rem; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; align-items: flex-start;">
          <div style="width: 28px; height: 28px; border-radius: 50%; background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-weight: 800; font-size: 0.78rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            ${r.number || (i+1)}
          </div>
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem; flex-wrap: wrap; gap: 0.3rem;">
              <strong style="font-size: 0.88rem; color: #0f172a;">${r.title}</strong>
              <span style="font-size: 0.72rem; color: #0284c7; background: #f0f9ff; border: 1px solid #bae6fd; padding: 0.15rem 0.45rem; border-radius: 4px; font-weight: 700;">
                📅 ${r.date} ${r.time ? '• ' + r.time : ''}
              </span>
            </div>
            <p style="font-size: 0.78rem; color: #475569; margin: 0; line-height: 1.4;">${r.description}</p>
            <div style="font-size: 0.72rem; color: #64748b; margin-top: 0.25rem; display: flex; gap: 0.75rem;">
              <span><strong>Platform:</strong> ${r.platform || 'Campus / Online'}</span>
              <span><strong>Evaluation:</strong> <span style="color: #059669; font-weight: 600;">${r.criteria || 'Standard Shortlist'}</span></span>
            </div>
          </div>
        </div>
      `).join('');
    }

    const cpiPass = parseFloat(jaf.student_cpi || '0') >= parseFloat(jaf.cgpa_cutoff || '0');
    const tenthPass = parseFloat(jaf.student_tenth || '0') >= parseFloat(jaf.min_tenth_percentage || '0');
    const twelfthPass = parseFloat(jaf.student_twelfth || '0') >= parseFloat(jaf.min_twelfth_percentage || '0');
    const backlogsPass = parseInt(jaf.student_backlogs || '0') <= parseInt(jaf.max_backlogs_allowed || '0');

    body.innerHTML = `
      <!-- Top 4-Metric Highlights -->
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem;">
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 1px solid #bbf7d0; border-radius: 10px; padding: 0.85rem 1rem;">
          <div style="font-size: 0.7rem; font-weight: 700; color: #15803d; text-transform: uppercase;">Total Package (CTC)</div>
          <div style="font-size: 1.25rem; font-weight: 800; color: #166534; font-family: 'Outfit', sans-serif; margin-top: 0.2rem;">${jaf.ctc}</div>
        </div>
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; border-radius: 10px; padding: 0.85rem 1rem;">
          <div style="font-size: 0.7rem; font-weight: 700; color: #1d4ed8; text-transform: uppercase;">Min CPI Cutoff</div>
          <div style="font-size: 1.25rem; font-weight: 800; color: #1e40af; margin-top: 0.2rem;">${jaf.cgpa_cutoff} <span style="font-size: 0.75rem; font-weight: 500; color: #60a5fa;">/ 10.0</span></div>
        </div>
        <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border: 1px solid #fecaca; border-radius: 10px; padding: 0.85rem 1rem;">
          <div style="font-size: 0.7rem; font-weight: 700; color: #b91c1c; text-transform: uppercase;">Deadline</div>
          <div style="font-size: 0.95rem; font-weight: 800; color: #991b1b; margin-top: 0.35rem; line-height: 1.2;">⏰ ${jaf.deadline}</div>
        </div>
        <div style="background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); border: 1px solid #e9d5ff; border-radius: 10px; padding: 0.85rem 1rem;">
          <div style="font-size: 0.7rem; font-weight: 700; color: #7e22ce; text-transform: uppercase;">Hiring Slot</div>
          <div style="font-size: 0.95rem; font-weight: 800; color: #6b21a8; margin-top: 0.35rem; line-height: 1.2;">⚡ ${jaf.slot}</div>
        </div>
      </div>

      <!-- Eligibility Check Matrix -->
      <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
          <h4 style="font-size: 0.88rem; font-weight: 700; color: #0f172a; margin: 0; display: flex; align-items: center; gap: 0.4rem;">
            <span>🎯</span> Academic Eligibility & Prerequisite Criteria
          </h4>
          <span style="font-size: 0.72rem; font-weight: 700; padding: 0.25rem 0.6rem; border-radius: 4px; ${jaf.is_eligible ? 'background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0;' : 'background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca;'}">
            ${jaf.is_eligible ? '✓ You Meet All Academic Criteria' : `❌ Ineligible: ${jaf.eligibility_reasons && jaf.eligibility_reasons.length ? jaf.eligibility_reasons[0] : 'Branch / Criteria Mismatch'}`}
          </span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem;">
          <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.5rem 0.65rem;">
            <div style="font-size: 0.68rem; color: #64748b;">CPI Requirement</div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #0f172a; margin-top: 0.1rem;">≥ ${jaf.cgpa_cutoff} (You: ${jaf.student_cpi})</div>
            <div style="font-size: 0.68rem; font-weight: 700; color: ${cpiPass ? '#059669' : '#dc2626'};">${cpiPass ? '✓ Satisfied' : '❌ Below Cutoff'}</div>
          </div>
          <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.5rem 0.65rem;">
            <div style="font-size: 0.68rem; color: #64748b;">10th Standard %</div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #0f172a; margin-top: 0.1rem;">≥ ${jaf.min_tenth_percentage}% (You: ${jaf.student_tenth}%)</div>
            <div style="font-size: 0.68rem; font-weight: 700; color: ${tenthPass ? '#059669' : '#dc2626'};">${tenthPass ? '✓ Satisfied' : '❌ Below Cutoff'}</div>
          </div>
          <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.5rem 0.65rem;">
            <div style="font-size: 0.68rem; color: #64748b;">12th / Diploma %</div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #0f172a; margin-top: 0.1rem;">≥ ${jaf.min_twelfth_percentage}% (You: ${jaf.student_twelfth}%)</div>
            <div style="font-size: 0.68rem; font-weight: 700; color: ${twelfthPass ? '#059669' : '#dc2626'};">${twelfthPass ? '✓ Satisfied' : '❌ Below Cutoff'}</div>
          </div>
          <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.5rem 0.65rem;">
            <div style="font-size: 0.68rem; color: #64748b;">Backlog Limit</div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #0f172a; margin-top: 0.1rem;">Max ${jaf.max_backlogs_allowed} (You: ${jaf.student_backlogs})</div>
            <div style="font-size: 0.68rem; font-weight: 700; color: ${backlogsPass ? '#059669' : '#dc2626'};">${backlogsPass ? '✓ 0 Backlogs' : '❌ Exceeds Limit'}</div>
          </div>
        </div>
        <div style="margin-top: 0.6rem; font-size: 0.74rem; color: #475569;">
          <strong>Eligible Disciplines & Branches:</strong>
          <div style="display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.25rem;">
            ${(jaf.eligible_branches || []).map(b => `<span style="background: #ffffff; border: 1px solid #cbd5e1; padding: 0.15rem 0.5rem; border-radius: 4px; font-weight: 600; font-size: 0.72rem; color: #1e40af;">${b}</span>`).join('')}
          </div>
        </div>
      </div>

      <!-- Job Description & Role Overview -->
      <div>
        <h4 style="font-size: 0.92rem; font-weight: 800; color: #0f172a; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.4rem;">
          <span>📝</span> Detailed Job Description & Responsibilities
        </h4>
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; color: #334155; font-size: 0.84rem; line-height: 1.6; white-space: pre-line;">
          ${jaf.description}
        </div>
      </div>

      <!-- Compensation Breakdown -->
      <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 1rem;">
        <h4 style="font-size: 0.88rem; font-weight: 700; color: #0f172a; margin-bottom: 0.35rem;">
          💰 Compensation Structure & Service Agreement
        </h4>
        <div style="font-size: 0.82rem; color: #475569; line-height: 1.5; margin-bottom: 0.5rem;">
          ${jaf.ctc_breakdown}
        </div>
        <div style="font-size: 0.76rem; color: #64748b; display: flex; gap: 1.5rem; border-top: 1px solid #e2e8f0; padding-top: 0.4rem;">
          <span><strong>Service Bond:</strong> ${jaf.bond}</span>
          <span><strong>Relocation:</strong> Standard Tier 1 Campus Relocation Package</span>
        </div>
      </div>

      <!-- Selection Roadmap -->
      <div>
        <h4 style="font-size: 0.92rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
          <span>📈</span> Structured Multi-Stage Recruitment Roadmap
        </h4>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          ${roundsHtml}
        </div>
      </div>

      <!-- Technical Stack & Requirements -->
      <div>
        <h4 style="font-size: 0.92rem; font-weight: 800; color: #0f172a; margin-bottom: 0.4rem;">
          🛠️ Desired Technical Skillset & Competencies
        </h4>
        <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.82rem; color: #475569; line-height: 1.55;">
          ${(jaf.requirements || []).map(r => `<li>${r}</li>`).join('')}
        </ul>
      </div>
    `;

    // 3. Footer Actions
    footer.innerHTML = `
      <button type="button" class="btn btn-secondary btn-sm" onclick="closeModal()" style="padding: 0.45rem 1rem;">Close</button>
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        ${
          jaf.is_applied
            ? `<button type="button" class="btn btn-applied btn-sm" disabled style="padding: 0.45rem 1.25rem; font-weight: 700;">✓ Application Submitted</button>`
            : (!jaf.student_verified
                ? `<button type="button" class="btn btn-secondary btn-sm" onclick="closeModal(); showLockedApprovalModal('${jaf.company}');" style="color: #92400e; background: #fef3c7; border-color: #fcd34d; font-weight: 700; padding: 0.45rem 1rem;"><span>🔒</span> Approval Required to Apply</button>`
                : (!jaf.is_eligible
                    ? `<button type="button" class="btn btn-secondary btn-sm" disabled style="color: #b91c1c; background: #fee2e2; border-color: #fca5a5; font-weight: 700; padding: 0.45rem 1rem;" title="${jaf.eligibility_reasons ? jaf.eligibility_reasons.join('; ') : ''}">❌ Ineligible (${jaf.eligibility_reasons && jaf.eligibility_reasons.length ? jaf.eligibility_reasons[0] : 'Branch Mismatch'})</button>`
                    : `<button type="button" class="btn btn-primary btn-sm" onclick="handleApply('${jaf.id}'); closeModal();" style="padding: 0.45rem 1.25rem; font-weight: 700; background: #2563eb; color: #ffffff; box-shadow: 0 2px 8px rgba(37,99,235,0.35);">Apply with Verified Master Resume →</button>`
                  )
              )
        }
      </div>
    `;

  } catch (err) {
    console.error(err);
    body.innerHTML = `<div style="color: #dc2626; padding: 2rem; text-align: center; background: #fef2f2; border-radius: 8px; border: 1px solid #fca5a5;">
      <strong>⚠️ Error Loading Specifications:</strong><br>
      <span style="font-size: 0.85rem;">${err.message || 'Could not fetch JAF details from server.'}</span>
    </div>`;
  }
}

function closeModal() {
  const modal = document.getElementById('jaf-modal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.remove('active');
  }
}

async function openHiringTrackerModal(jafId) {
  const modal = document.getElementById('hiring-tracker-modal');
  const title = document.getElementById('modal-tracker-title');
  const body = document.getElementById('modal-tracker-body');

  if (!modal || !body) return;

  modal.style.display = 'flex';
  modal.classList.add('active');
  body.innerHTML = `
    <div style="text-align: center; padding: 3rem 1.5rem; color: #64748b;">
      <div style="font-size: 2.2rem; margin-bottom: 0.75rem; animation: spin 1s infinite linear;">🔄</div>
      <div style="font-weight: 700; font-size: 1.05rem; color: #0f172a;">Connecting to Recruiter Live Pipeline...</div>
      <p style="font-size: 0.82rem; margin: 0.35rem 0 0; color: #64748b;">Syncing candidate evaluation milestones, online test schedule, and interview stages.</p>
    </div>
  `;

  try {
    const res = await fetch(`/api/jaf/${jafId}/`);
    const json = await res.json();
    if (!json.success) throw new Error(json.error || "Recruitment drive details not found.");

    const jaf = json.jaf;
    const appStatus = jaf.application_status || (jaf.is_applied ? 'APPLIED' : 'NOT_APPLIED');

    // Header Title
    title.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.85rem;">
        <div class="company-logo-wrap" style="width: 44px; height: 44px; border-radius: 10px; background: #ffffff; border: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); flex-shrink: 0;">
          <img src="${jaf.company_logo}" alt="${jaf.company}" class="company-logo-img" style="max-width: 100%; max-height: 100%; object-fit: contain;" onerror="this.onerror=null; this.parentElement.innerHTML='<div style=\\'font-weight:800; color:#1e40af; font-size:0.9rem;\\'>${jaf.company_fallback}</div>';">
        </div>
        <div>
          <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
            <h3 style="font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.2;">${jaf.company} • Hiring Process & Pipeline Tracker</h3>
          </div>
          <div style="font-size: 0.82rem; color: #475569; margin-top: 0.15rem; font-weight: 500;">
            <strong style="color: #1e40af;">${jaf.role}</strong> • <span>💰 ${jaf.ctc}</span> • <span style="color: #6d28d9; font-weight: 700;">⚡ ${jaf.slot}</span>
          </div>
        </div>
      </div>
      <button type="button" class="modal-close-btn" onclick="closeHiringTrackerModal()" style="font-size: 1.5rem; width: 36px; height: 36px; border: none; background: #f1f5f9; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #64748b;">&times;</button>
    `;

    // Candidate Live Status Banner
    let statusBanner = '';
    if (appStatus === 'OFFERED') {
      statusBanner = `
        <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 1.5px solid #6ee7b7; border-radius: 12px; padding: 1.1rem 1.25rem; display: flex; align-items: center; gap: 1rem;">
          <div style="width: 48px; height: 48px; border-radius: 50%; background: #059669; color: #ffffff; font-size: 1.6rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 12px rgba(5,150,105,0.3);">🏆</div>
          <div>
            <div style="font-weight: 800; color: #065f46; font-size: 1rem;">Campus Placement Offer Extended!</div>
            <div style="font-size: 0.82rem; color: #047857; margin-top: 0.15rem;">Congratulations! You have cleared all recruitment rounds for ${jaf.company}. Official offer package: <strong>${jaf.ctc}</strong>.</div>
          </div>
        </div>
      `;
    } else if (appStatus === 'INTERVIEW') {
      statusBanner = `
        <div style="background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 1.5px solid #fcd34d; border-radius: 12px; padding: 1.1rem 1.25rem; display: flex; align-items: center; gap: 1rem;">
          <div style="width: 48px; height: 48px; border-radius: 50%; background: #d97706; color: #ffffff; font-size: 1.6rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 12px rgba(217,119,6,0.3);">⚡</div>
          <div>
            <div style="font-weight: 800; color: #92400e; font-size: 1rem;">Shortlisted for Interview Round (Day 1 Superday)</div>
            <div style="font-size: 0.82rem; color: #b45309; margin-top: 0.15rem;">Your profile has cleared the technical assessment. Your interview slot is confirmed for <strong>${jaf.slot}</strong>. Check your Interview Schedule for room & panel details.</div>
          </div>
        </div>
      `;
    } else if (appStatus === 'SHORTLISTED') {
      statusBanner = `
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1.5px solid #93c5fd; border-radius: 12px; padding: 1.1rem 1.25rem; display: flex; align-items: center; gap: 1rem;">
          <div style="width: 48px; height: 48px; border-radius: 50%; background: #2563eb; color: #ffffff; font-size: 1.6rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 12px rgba(37,99,235,0.3);">✓</div>
          <div>
            <div style="font-weight: 800; color: #1e40af; font-size: 1rem;">Shortlisted for Online Assessment / Coding Round</div>
            <div style="font-size: 0.82rem; color: #1d4ed8; margin-top: 0.15rem;">Your academic criteria & master resume met the recruiter benchmarks. You are invited to participate in the online test round.</div>
          </div>
        </div>
      `;
    } else if (appStatus === 'APPLIED') {
      statusBanner = `
        <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 1.1rem 1.25rem; display: flex; align-items: center; gap: 1rem;">
          <div style="width: 48px; height: 48px; border-radius: 50%; background: #0284c7; color: #ffffff; font-size: 1.6rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 12px rgba(2,132,199,0.3);">📝</div>
          <div>
            <div style="font-weight: 800; color: #0f172a; font-size: 1rem;">Application Submitted & Criteria Verified</div>
            <div style="font-size: 0.82rem; color: #475569; margin-top: 0.15rem;">Your certified master resume has been delivered to ${jaf.company} talent acquisition desk. The company is evaluating candidate profiles.</div>
          </div>
        </div>
      `;
    }

    // Rounds Timeline
    let roundsHtml = '';
    const rounds = jaf.hiring_rounds || [];
    if (rounds.length > 0) {
      roundsHtml = rounds.map((r, idx) => {
        let badgeStyle = 'background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;';
        let badgeText = '⏳ Scheduled / Upcoming';
        let iconBg = '#f1f5f9';
        let iconColor = '#64748b';

        if (r.status === 'COMPLETED') {
          badgeStyle = 'background: #ecfdf5; color: #047857; border: 1px solid #6ee7b7;';
          badgeText = '✓ Completed';
          iconBg = '#dcfce7';
          iconColor = '#15803d';
        } else if (r.status === 'ACTIVE') {
          badgeStyle = 'background: #eff6ff; color: #1d4ed8; border: 1px solid #93c5fd;';
          badgeText = '⚡ Active In Progress';
          iconBg = '#dbeafe';
          iconColor = '#1e40af';
        }

        return `
          <div style="display: flex; gap: 1rem; position: relative; padding-bottom: ${idx === rounds.length - 1 ? '0' : '1.25rem'};">
            ${idx !== rounds.length - 1 ? '<div style="position: absolute; left: 18px; top: 38px; bottom: 0; width: 2px; background: #e2e8f0;"></div>' : ''}
            
            <div style="width: 38px; height: 38px; border-radius: 50%; background: ${iconBg}; color: ${iconColor}; font-weight: 800; font-size: 0.95rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; z-index: 2; border: 2px solid #ffffff; box-shadow: 0 2px 6px rgba(0,0,0,0.08);">
              ${r.status === 'COMPLETED' ? '✓' : (r.number || idx + 1)}
            </div>

            <div style="flex: 1; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; flex-wrap: wrap; gap: 0.4rem;">
                <h4 style="font-size: 0.96rem; font-weight: 800; color: #0f172a; margin: 0;">${r.title}</h4>
                <span style="font-size: 0.72rem; font-weight: 800; padding: 0.25rem 0.65rem; border-radius: 9999px; ${badgeStyle}">${badgeText}</span>
              </div>
              <p style="font-size: 0.84rem; color: #475569; margin: 0 0 0.65rem 0; line-height: 1.5;">${r.description}</p>
              
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.5rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.6rem 0.85rem; font-size: 0.76rem; color: #334155;">
                <div>📅 <strong>Date & Time:</strong> ${r.date} ${r.time ? '• ' + r.time : ''}</div>
                <div>📍 <strong>Venue / Platform:</strong> ${r.platform || 'Online / Campus'}</div>
                <div style="grid-column: 1 / -1;">🎯 <strong>Passing Benchmark:</strong> <span style="color: #059669; font-weight: 700;">${r.criteria || 'Top Percentile'}</span></div>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    body.innerHTML = `
      ${statusBanner}

      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">
          <h4 style="font-size: 1rem; font-weight: 800; color: #0f172a; margin: 0; display: flex; align-items: center; gap: 0.45rem;">
            <span>📍</span> Recruitment Stages & Company Road Map
          </h4>
          <span style="font-size: 0.76rem; color: #64748b;">Configured by ${jaf.company} HR Talent Team</span>
        </div>
        <div style="display: flex; flex-direction: column;">
          ${roundsHtml}
        </div>
      </div>
    `;

    // Dynamic Footer Action Button Update
    const footerAction = document.getElementById('modal-tracker-footer-action');
    if (footerAction) {
      if (jaf.has_interview_slot) {
        footerAction.innerHTML = `
          <a href="/schedule/" class="btn btn-primary btn-sm" style="background: #1e40af; color: #ffffff; text-decoration: none; font-weight: 700; padding: 0.45rem 1rem; border-radius: 6px; display: inline-flex; align-items: center; gap: 0.35rem;">
            <span>📅</span> View Confirmed Interview Schedule
          </a>
        `;
      } else if (appStatus === 'INTERVIEW' || appStatus === 'SHORTLISTED') {
        footerAction.innerHTML = `
          <span style="font-size: 0.8rem; color: #b45309; background: #fef3c7; border: 1px solid #fcd34d; padding: 0.45rem 0.85rem; border-radius: 6px; font-weight: 700; display: inline-flex; align-items: center; gap: 0.35rem;">
            <span>⏳</span> Interview Slot Allocation Pending by Recruiter
          </span>
        `;
      } else if (appStatus === 'APPLIED') {
        footerAction.innerHTML = `
          <span style="font-size: 0.8rem; color: #0284c7; background: #f0f9ff; border: 1px solid #bae6fd; padding: 0.45rem 0.85rem; border-radius: 6px; font-weight: 600; display: inline-flex; align-items: center; gap: 0.35rem;">
            <span>📝</span> Application Submitted (Awaiting Shortlist)
          </span>
        `;
      } else {
        footerAction.innerHTML = `
          <span style="font-size: 0.8rem; color: #64748b; background: #f1f5f9; border: 1px solid #cbd5e1; padding: 0.45rem 0.85rem; border-radius: 6px; font-weight: 600;">
            No Active Interview Scheduled
          </span>
        `;
      }
    }

  } catch (err) {
    console.error(err);
    body.innerHTML = `
      <div style="color: #dc2626; padding: 2rem; text-align: center; background: #fef2f2; border-radius: 8px; border: 1px solid #fca5a5;">
        <strong>⚠️ Error Loading Hiring Workflow:</strong><br>
        <span style="font-size: 0.85rem;">${err.message || 'Could not fetch company recruitment stages.'}</span>
      </div>
    `;
  }
}

function closeHiringTrackerModal() {
  const modal = document.getElementById('hiring-tracker-modal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.remove('active');
  }
}

function viewResumeModal(resumeName) {
  const modal = document.getElementById('resume-modal');
  const textEl = document.getElementById('resume-modal-filename');
  if (textEl && resumeName) textEl.textContent = resumeName;
  if (modal) {
    modal.style.display = 'flex';
    modal.classList.add('active');
  }
}

function closeResumeModal() {
  const modal = document.getElementById('resume-modal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.remove('active');
  }
}

function showToast(message) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
