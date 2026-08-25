/**
 * IIT Bombay Placement Portal - Mock Data Store
 */

const INITIAL_DATA = {
  student: {
    name: "Aarav Sharma",
    rollNumber: "220050042",
    email: "aarav.sharma@iitb.ac.in",
    degree: "B.Tech in Computer Science & Engineering",
    department: "Computer Science & Engineering",
    specialization: "Honours in Artificial Intelligence • Minor in Finance",
    cgpa: "9.48",
    batch: "Class of 2026",
    resumes: [
      { id: "res_tech", name: "Aarav_Sharma_SDE_Master.pdf", verified: true, date: "2026-10-15", verifiedBy: "Prof. S. Bhattacharya (DPC)" },
      { id: "res_quant", name: "Aarav_Sharma_Quant_Finance.pdf", verified: true, date: "2026-10-18", verifiedBy: "Prof. S. Bhattacharya (DPC)" }
    ],
    placementStatus: "In Progress (Phase 1)",
    placementOffer: null,
    stats: {
      applied: 6,
      shortlisted: 3,
      interviews: 2,
      offers: 0
    }
  },

  jafs: [
    {
      id: "jaf_01",
      company: "Google",
      logo: "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
      logoFallback: "G",
      role: "Software Development Engineer - Systems & AI",
      sector: "Software & AI",
      location: "Bengaluru / Hyderabad (Domestic) • Mountain View (Intl)",
      ctc: "₹48.5 LPA",
      ctcFull: "Base: ₹24 LPA + Stocks: $35,000 (4 yrs) + Joining Bonus: ₹5 LPA + Relocation",
      cgpaCutoff: 8.5,
      branches: ["Computer Science (CS)", "Electrical Engg (EE)", "Maths & Computing (MnC)"],
      degrees: ["B.Tech", "Dual Degree"],
      deadline: "Today, 11:59 PM IST",
      deadlineTime: new Date(Date.now() + 10 * 3600 * 1000).toISOString(),
      slot: "Day 1 - Slot 1 (Dec 1)",
      description: "As an SDE at Google, you will tackle massive scale engineering problems across distributed systems, machine learning infrastructure, and cloud networking. You will collaborate with global teams on products touching billions of users worldwide.",
      requirements: [
        "Strong fundamentals in Data Structures, Distributed Algorithms, and OS",
        "Proficiency in C++, Go, Java, or Python",
        "Prior experience in systems programming, high-performance computing, or AI is a plus"
      ],
      process: [
        { step: "Online Coding Test", date: "Nov 20, 2026", details: "3 Algorithmic Challenges (90 mins)" },
        { step: "Shortlist Announcement", date: "Nov 25, 2026", details: "Top 40 candidates shortlisted" },
        { step: "Technical Round 1 & 2", date: "Dec 1, 2026", details: "System Design & Algorithms" },
        { step: "Googlyness & Leadership", date: "Dec 1, 2026", details: "Behavioral & Culture Fit" }
      ],
      bond: "None",
      applied: true,
      applicationDate: "2026-11-10",
      status: "Shortlisted"
    },
    {
      id: "jaf_02",
      company: "Jane Street",
      logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Jane_Street_Capital_Logo.svg/1200px-Jane_Street_Capital_Logo.svg.png",
      logoFallback: "JS",
      role: "Quantitative Trader / Researcher",
      sector: "Quant & Finance",
      location: "Hong Kong / London / New York",
      ctc: "₹1.42 Cr ($275,000 USD)",
      ctcFull: "Base: $150,000 + Performance Bonus: $100,000 + Relocation: $25,000",
      cgpaCutoff: 9.0,
      branches: ["Open to All Branches (B.Tech / DD / BS)"],
      degrees: ["B.Tech", "Dual Degree", "BS"],
      deadline: "Tomorrow, 6:00 PM IST",
      deadlineTime: new Date(Date.now() + 30 * 3600 * 1000).toISOString(),
      slot: "Day 1 - Slot 1 (Dec 1)",
      description: "Jane Street is a quantitative trading firm with a unique focus on technology and collaborative problem solving. Traders and researchers build mathematical models and trade hundreds of thousands of financial products around the world.",
      requirements: [
        "Exceptional mathematical intuition, probability theory, and combinatorics skills",
        "Quick mental math and risk evaluation under uncertainty",
        "Experience in OCaml, Python, C++, or functional programming is a bonus"
      ],
      process: [
        { step: "Mental Math & Probability Test", date: "Nov 18, 2026", details: "45 mins speed calculation" },
        { step: "Quant Interview Round 1", date: "Nov 26, 2026", details: "Game theory and probability puzzles" },
        { step: "Final Superday (Day 1)", date: "Dec 1, 2026", details: "3 Intensive Trading Simulation Rounds" }
      ],
      bond: "None",
      applied: true,
      applicationDate: "2026-11-08",
      status: "Interview Scheduled"
    },
    {
      id: "jaf_03",
      company: "Microsoft",
      logo: "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
      logoFallback: "MS",
      role: "Software Development Engineer II",
      sector: "Software & AI",
      location: "Hyderabad / Bengaluru / Noida",
      ctc: "₹51.0 LPA",
      ctcFull: "Base: ₹22.5 LPA + Performance Bonus: 20% + Stocks: $40,000 + Joining Bonus: ₹6 LPA",
      cgpaCutoff: 7.5,
      branches: ["CS", "EE", "MnC", "Mechanical (ME)", "Civil (CE)"],
      degrees: ["B.Tech", "Dual Degree", "M.Tech"],
      deadline: "In 2 days",
      deadlineTime: new Date(Date.now() + 48 * 3600 * 1000).toISOString(),
      slot: "Day 1 - Slot 2 (Dec 1)",
      description: "Join the Azure Cloud and AI division at Microsoft. You will build cutting-edge generative AI copilot experiences and ultra-low latency hyper-scale infrastructure powering millions of enterprises worldwide.",
      requirements: [
        "Solid foundations in object-oriented programming (C#, C++, Java)",
        "Understanding of asynchronous architectures and microservices",
        "Problem-solving acumen and collaborative team spirit"
      ],
      process: [
        { step: "Online Assessment (OA)", date: "Nov 15, 2026", details: "Codility Test (2 questions)" },
        { step: "Technical Interviews (Day 1)", date: "Dec 1, 2026", details: "3 Technical Rounds + 1 AA Round" }
      ],
      bond: "None",
      applied: true,
      applicationDate: "2026-11-05",
      status: "Interview Scheduled"
    },
    {
      id: "jaf_04",
      company: "Tower Research Capital",
      logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Tower_Research_Capital_logo.svg/1200px-Tower_Research_Capital_logo.svg.png",
      logoFallback: "TRC",
      role: "Core Engineering Analyst - High Frequency Trading",
      sector: "Quant & Finance",
      location: "Gurugram / Singapore",
      ctc: "₹65.0 LPA",
      ctcFull: "Base: ₹32 LPA + Guaranteed Bonus: ₹18 LPA + Performance Incentive + Relocation",
      cgpaCutoff: 8.8,
      branches: ["Computer Science (CS)", "Electrical Engg (EE)", "Maths & Computing (MnC)"],
      degrees: ["B.Tech", "Dual Degree"],
      deadline: "In 3 days",
      deadlineTime: new Date(Date.now() + 72 * 3600 * 1000).toISOString(),
      slot: "Day 1 - Slot 1 (Dec 1)",
      description: "Develop sub-microsecond low-latency trading software, custom kernel bypass network stacks, and FPGA accelerated pipelines in C++20 for global financial exchanges.",
      requirements: [
        "Mastery in Modern C++ (C++17/20), multi-threading, lock-free data structures",
        "In-depth grasp of CPU cache hierarchies, memory models, and Linux internals"
      ],
      process: [
        { step: "Hackerrank Systems Test", date: "Nov 22, 2026", details: "Low-latency C++ challenges" },
        { step: "Interviews (Day 1)", date: "Dec 1, 2026", details: "Architecture, Concurrency & C++ Deep Dive" }
      ],
      bond: "None",
      applied: false,
      status: "Open"
    },
    {
      id: "jaf_05",
      company: "Texas Instruments",
      logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Texas_Instruments_logo.svg/1200px-Texas_Instruments_logo.svg.png",
      logoFallback: "TI",
      role: "Analog & Mixed-Signal IC Design Engineer",
      sector: "Core Engineering",
      location: "Bengaluru",
      ctc: "₹34.0 LPA",
      ctcFull: "Base: ₹20 LPA + RSU: $20,000 + Joining Bonus: ₹4 LPA",
      cgpaCutoff: 7.8,
      branches: ["Electrical (EE)", "Energy Science (EN)", "Engineering Physics (EP)"],
      degrees: ["B.Tech", "Dual Degree", "M.Tech"],
      deadline: "In 3 days",
      deadlineTime: new Date(Date.now() + 70 * 3600 * 1000).toISOString(),
      slot: "Day 2 - Slot 1 (Dec 2)",
      description: "Design state-of-the-art power management ICs, RF transceivers, and precision data converters for next-generation automotive and aerospace electronics.",
      requirements: [
        "Deep knowledge of CMOS Analog Circuit Design, Op-Amps, and Bandgap References",
        "Familiarity with Cadence Virtuoso and SPICE simulation suites"
      ],
      process: [
        { step: "Written Technical Assessment", date: "Nov 23, 2026", details: "Analog Circuits & Signals" },
        { step: "Technical Interviews", date: "Dec 2, 2026", details: "Schematic design and layout questions" }
      ],
      bond: "None",
      applied: false,
      status: "Open"
    },
    {
      id: "jaf_06",
      company: "McKinsey & Company",
      logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/McKinsey_%26_Company_Logo.svg/1200px-McKinsey_%26_Company_Logo.svg.png",
      logoFallback: "McK",
      role: "Junior Associate - Strategy & Digital Transformation",
      sector: "Management Consulting",
      location: "Mumbai / Delhi / Bengaluru",
      ctc: "₹32.0 LPA",
      ctcFull: "Fixed: ₹24 LPA + Performance Bonus: ₹6 LPA + Retiral & Benefits",
      cgpaCutoff: 8.0,
      branches: ["Open to All Engineering & Science Branches"],
      degrees: ["B.Tech", "Dual Degree", "M.Tech", "MBA"],
      deadline: "In 4 days",
      deadlineTime: new Date(Date.now() + 96 * 3600 * 1000).toISOString(),
      slot: "Day 1 - Slot 2 (Dec 1)",
      description: "Work with C-suite leadership across Fortune 500 companies to solve complex strategic dilemmas, execute digital transformations, and drive sustainable growth.",
      requirements: [
        "Strong structured problem solving and quantitative reasoning",
        "Exemplary communication, stakeholder management, and executive presence"
      ],
      process: [
        { step: "Problem Solving Game (PSG)", date: "Nov 16, 2026", details: "Imbellus Simulation Assessment" },
        { step: "Case Interviews (Day 1)", date: "Dec 1, 2026", details: "3 Rounds of Business Case & PEI" }
      ],
      bond: "None",
      applied: true,
      applicationDate: "2026-11-12",
      status: "Applied"
    },
    {
      id: "jaf_07",
      company: "Apple",
      logo: "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
      logoFallback: "AAPL",
      role: "Silicon Validation & Architecture Engineer",
      sector: "Core Engineering",
      location: "Hyderabad / Bengaluru",
      ctc: "₹42.0 LPA",
      ctcFull: "Base: ₹24 LPA + Apple RSU: $28,000 + Joining Bonus: ₹5 LPA",
      cgpaCutoff: 8.0,
      branches: ["Electrical (EE)", "Computer Science (CS)", "Mechanical (ME)"],
      degrees: ["B.Tech", "Dual Degree", "M.Tech"],
      deadline: "In 5 days",
      deadlineTime: new Date(Date.now() + 120 * 3600 * 1000).toISOString(),
      slot: "Day 2 - Slot 1 (Dec 2)",
      description: "Join the Silicon Engineering Group to test, debug, and validate next-gen M-series Apple Silicon powering Mac, iPad, and Vision Pro devices.",
      requirements: [
        "Knowledge of Computer Architecture, RISC-V/ARM, and Verilog/SystemVerilog",
        "Proficiency with Python/C++ automation test harnesses"
      ],
      process: [
        { step: "Silicon Architecture Test", date: "Nov 24, 2026", details: "Microarchitecture & Digital Logic" },
        { step: "Technical Interviews", date: "Dec 2, 2026", details: "3 Technical Architecture Rounds" }
      ],
      bond: "None",
      applied: false,
      status: "Open"
    },
    {
      id: "jaf_08",
      company: "Boston Consulting Group (BCG)",
      logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Boston_Consulting_Group_2020_logo.svg/1200px-Boston_Consulting_Group_2020_logo.svg.png",
      logoFallback: "BCG",
      role: "Associate Consultant",
      sector: "Management Consulting",
      location: "Mumbai / Gurugram",
      ctc: "₹33.5 LPA",
      ctcFull: "Fixed: ₹25 LPA + Performance Incentive: ₹6.5 LPA + Wellness & Travel Stipend",
      cgpaCutoff: 8.0,
      branches: ["Open to All Branches"],
      degrees: ["B.Tech", "Dual Degree"],
      deadline: "In 4 days",
      deadlineTime: new Date(Date.now() + 90 * 3600 * 1000).toISOString(),
      slot: "Day 1 - Slot 2 (Dec 1)",
      description: "Partner with industry leaders to unlock business value through innovative business models, decarbonization strategies, and AI implementation.",
      requirements: [
        "High analytical rigor, hypothesis-driven problem solving, and top-tier communication"
      ],
      process: [
        { step: "Casey AI Chatbot Assessment", date: "Nov 17, 2026" },
        { step: "Case Interviews (Day 1)", date: "Dec 1, 2026", details: "Market Entry & Profitability Cases" }
      ],
      bond: "None",
      applied: false,
      status: "Open"
    }
  ],

  upcomingInterviews: [
    {
      id: "int_01",
      company: "Microsoft",
      role: "Software Development Engineer II",
      round: "Round 1: Systems & Concurrency",
      date: "Dec 1, 2026",
      time: "08:30 AM - 09:30 AM IST",
      slot: "Day 1 • Slot 1",
      location: "Room MB-204 (Gulmohar Building) / Microsoft Teams",
      meetingLink: "https://teams.microsoft.com/l/meetup-join/iitb-slot1-msft",
      status: "Confirmed",
      type: "Technical"
    },
    {
      id: "int_02",
      company: "Jane Street",
      role: "Quantitative Trader / Researcher",
      round: "Round 2: Probability & Market Making Games",
      date: "Dec 1, 2026",
      time: "11:00 AM - 12:15 PM IST",
      slot: "Day 1 • Slot 1",
      location: "Computer Center Lab 1 (CC-102)",
      meetingLink: "https://janestreet.zoom.us/j/iitb-day1-superday",
      status: "Confirmed",
      type: "Superday Quant"
    },
    {
      id: "int_03",
      company: "Google",
      role: "Software Development Engineer",
      round: "Round 1: Distributed Algorithms",
      date: "Dec 1, 2026",
      time: "03:00 PM - 04:00 PM IST",
      slot: "Day 1 • Slot 2",
      location: "Google Meet / Room MB-301",
      meetingLink: "https://meet.google.com/iitb-goog-day1",
      status: "Tentative (Awaiting Slot Finalization)",
      type: "Technical"
    }
  ],

  announcements: [
    {
      id: "ann_01",
      tag: "URGENT",
      tagType: "danger",
      title: "Day 1 Slot 1 Interview Schedules Released",
      time: "15 mins ago",
      author: "Placement Office (TPO)",
      content: "All shortlisted students for Google, Jane Street, Microsoft, and Tower Research must report to the Gulmohar Building by 07:30 AM IST on Dec 1st. Formal dress code and physical ID cards mandatory."
    },
    {
      id: "ann_02",
      tag: "SHORTLIST",
      tagType: "success",
      title: "Google SDE Shortlist (40 Candidates) Published",
      time: "2 hours ago",
      author: "DPC Computer Science",
      content: "The shortlist for Google Software Engineering (Systems & AI) has been published on the portal. Shortlisted candidates have received direct calendar invites."
    },
    {
      id: "ann_03",
      tag: "NOTICE",
      tagType: "warning",
      title: "Resume Freezing Window Closes Tonight at 23:59 IST",
      time: "5 hours ago",
      author: "Prof. In-Charge, Placements",
      content: "No further modifications will be permitted for Master Resumes for Phase 1 Day 1 & Day 2 companies after midnight."
    },
    {
      id: "ann_04",
      tag: "PPT INFO",
      tagType: "info",
      title: "Tower Research Capital Pre-Placement Talk Recording",
      time: "Yesterday",
      author: "Student Placement Team",
      content: "The video recording of the TRC PPT held in Auditorium 1 has been uploaded to the placement portal drive."
    }
  ]
};

// Initialize State
function getAppState() {
  const saved = localStorage.getItem("IITB_PLACEMENT_STATE");
  if (saved) {
    try { return JSON.parse(saved); } catch (e) { console.error("Error parsing state", e); }
  }
  localStorage.setItem("IITB_PLACEMENT_STATE", JSON.stringify(INITIAL_DATA));
  return JSON.parse(JSON.stringify(INITIAL_DATA));
}

function saveAppState(state) {
  localStorage.setItem("IITB_PLACEMENT_STATE", JSON.stringify(state));
}
