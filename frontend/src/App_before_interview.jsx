import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";


const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: "▦" },
  { id: "evaluate", label: "Evaluate Candidates", icon: "⌁" },
  { id: "ranking", label: "Candidate Ranking", icon: "▥" },
  { id: "compare", label: "Candidate Comparison", icon: "⇄" },
  { id: "intelligence", label: "Candidate Intelligence", icon: "◉" },
  { id: "roadmap", label: "Skill Gap & Roadmap", icon: "↗" },

  { id: "assessment", label: "Technical Assessment", icon: "⌘" },

  { id: "history", label: "Evaluation History", icon: "◴" },
];

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [resumes, setResumes] = useState([]);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [selectedCandidateIndex, setSelectedCandidateIndex] = useState(0);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  const ranking = result?.ranking || [];
  const selectedCandidate =
    ranking[selectedCandidateIndex] || ranking[0] || null;
  const selectedEvaluation = selectedCandidate?.evaluation || {};

  const handleFiles = (e) => {
    setResumes(Array.from(e.target.files || []));
  };

  const evaluateCandidates = async () => {
    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }
    if (resumes.length === 0) {
      setError("Please select at least one resume.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    resumes.forEach((file) => formData.append("resumes", file));
    formData.append("job_description", jobDescription);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/evaluate-multiple`,
        formData,
      );
      setResult(response.data);
      setSelectedCandidateIndex(0);
      setActiveTab("ranking");
      await loadHistory();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Unable to evaluate candidates.");
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    setHistoryLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/history`);
      setHistory(response.data.history || []);
    } catch (err) {
      console.error(err);
    } finally {
      setHistoryLoading(false);
    }
  };

  const deleteHistoryItem = async (id) => {
    try {
      await axios.delete(`${API_BASE_URL}/history/${id}`);
      setHistory((items) => items.filter((item) => item.id !== id));
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete evaluation.");
    }
  };

  const exportHistoryToCSV = () => {
    if (!history.length) {
      setError("No history available to export.");
      return;
    }

    const headers = [
      "ID",
      "Candidate Name",
      "NeuroHire Score",
      "Recommendation",
      "Overall Skill Match",
      "Required Skill Match",
      "Preferred Skill Match",
      "Weighted Skill Match",
      "JD Similarity",
      "Experience Years",
      "Required Experience",
      "Experience Score",
      "Education Score",
      "Matched Skills",
      "Missing Skills",
      "Created At",
    ];

    const rows = history.map((item) => [
      item.id,
      item.candidate_name,
      item.neural_network_score,
      item.recommendation,
      item.skill_match,
      item.required_skill_match,
      item.preferred_skill_match,
      item.weighted_skill_match,
      item.jd_similarity,
      item.experience_years,
      item.required_experience,
      item.experience_score,
      item.education_score,
      (item.matched_skills || []).join(", "),
      (item.missing_skills || []).join(", "),
      item.created_at,
    ]);

    const escapeCSV = (value) => `"${String(value ?? "").replace(/"/g, '""')}"`;
    const csv = [
      headers.map(escapeCSV).join(","),
      ...rows.map((row) => row.map(escapeCSV).join(",")),
    ].join("\n");

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "neurohire_evaluation_history.csv";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const dashboardStats = useMemo(() => {
    const total = history.length;
    const avgScore =
      total > 0
        ? history.reduce(
            (sum, item) => sum + Number(item.neural_network_score || 0),
            0,
          ) / total
        : 0;

    const avgSkill =
      total > 0
        ? history.reduce(
            (sum, item) => sum + Number(item.skill_match || 0),
            0,
          ) / total
        : 0;

    const ready = history.filter(
      (item) => Number(item.neural_network_score || 0) >= 75,
    ).length;

    return { total, avgScore, avgSkill, ready };
  }, [history]);

  const topMissingSkills = useMemo(() => {
    const counts = {};
    history.forEach((item) => {
      (item.missing_skills || []).forEach((skill) => {
        counts[skill] = (counts[skill] || 0) + 1;
      });
    });
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);
  }, [history]);

  const filteredHistory = history.filter((item) =>
    `${item.candidate_name} ${item.recommendation}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );

  const navigate = (tab) => {
    setActiveTab(tab);
    setError("");
    if (tab === "history") loadHistory();
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">N</div>
          <div>
            <strong>NeuroHire</strong>
            <span>AI Recruitment & Readiness</span>
          </div>
        </div>

        <div className="side-label">NEURAL PLATFORM</div>

        <nav className="side-nav">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.id}
              className={activeTab === item.id ? "side-active" : ""}
              onClick={() => navigate(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="side-bottom">
          <div className="fairness-card">
            <span>✓ Human-in-the-Loop</span>
            <small>Final hiring decisions are made by recruiters</small>
          </div>
          <div className="side-links">
            <span>⚙ Settings</span>
            <span>ⓘ Help</span>
          </div>
        </div>
      </aside>

      <div className="workspace">
        <header className="topbar">
          <div className="search-shell">
            <span>⌕</span>
            <input
              placeholder="Search candidate, skill, JD or role..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="ai-online">
            <span className="online-dot" />
            NeuroHire AI Online
          </div>

          <button className="top-primary" onClick={() => navigate("evaluate")}>
            + New JD Evaluation
          </button>

          <div className="profile">
            <div className="avatar">NH</div>
            <div></div>
          </div>
        </header>

        <main className="main-content">
          {error && <div className="alert error-alert">{error}</div>}

          {activeTab === "dashboard" && (
            <Dashboard
              stats={dashboardStats}
              topMissingSkills={topMissingSkills}
              history={history}
              goEvaluate={() => navigate("evaluate")}
              goRanking={() => navigate("ranking")}
            />
          )}

          {activeTab === "evaluate" && (
            <EvaluateScreen
              jobDescription={jobDescription}
              setJobDescription={setJobDescription}
              resumes={resumes}
              handleFiles={handleFiles}
              setResumes={setResumes}
              loading={loading}
              evaluateCandidates={evaluateCandidates}
            />
          )}

          {activeTab === "ranking" && (
            <RankingScreen
              result={result}
              onInspect={(index) => {
                setSelectedCandidateIndex(index);
                navigate("intelligence");
              }}
              onCompare={() => navigate("compare")}
            />
          )}

          {activeTab === "intelligence" && (
            <CandidateIntelligence
              candidate={selectedCandidate}
              evaluation={selectedEvaluation}
              onRoadmap={() => navigate("roadmap")}
              onCompare={() => navigate("compare")}
            />
          )}

          {activeTab === "compare" && (
            <CompareCandidatesScreen
              ranking={ranking}
              onInspect={(index) => {
                setSelectedCandidateIndex(index);
                navigate("intelligence");
              }}
            />
          )}

          {activeTab === "roadmap" && (
            <RoadmapScreen
              candidate={selectedCandidate}
              evaluation={selectedEvaluation}
            />
          )}
          {activeTab === "assessment" && (
            <TechnicalAssessmentScreen
              candidate={selectedCandidate}
                evaluation={selectedEvaluation}
  />
)}

          {activeTab === "history" && (
            <HistoryScreen
              history={filteredHistory}
              loading={historyLoading}
              exportCSV={exportHistoryToCSV}
              refresh={loadHistory}
              onDelete={deleteHistoryItem}
            />
          )}
        </main>
      </div>
    </div>
  );
}

function Dashboard({
  stats,
  topMissingSkills,
  history,
  goEvaluate,
  goRanking,
}) {
  const latest = history.slice(0, 4);

  return (
    <>
      <section className="hero-panel">
        <div>
          <p className="eyebrow">AI-POWERED CANDIDATE INTELLIGENCE</p>
          <h1>
            Skill-Gap-Aware Neural Network
            <br />
            Candidate Intelligence
          </h1>
          <p className="hero-copy">
            Evaluate talent against precise job descriptions, expose latent
            skill gaps, and transform candidates into opportunity-ready hires.
          </p>
          <div className="hero-actions">
            <button className="primary" onClick={goEvaluate}>
              ✦ Evaluate Candidates
            </button>
            <button className="secondary" onClick={goRanking}>
              ▥ View Rankings
            </button>
          </div>
        </div>
        <div className="hero-badge-grid">
          <MiniBadge value={`${history.length}`} label="Saved Evaluations" />
          <MiniBadge value="Live" label="AI Scoring Engine" />
        </div>
      </section>

      <section className="stats-grid">
        <StatCard
          label="Evaluated Pool"
          value={stats.total}
          note="Saved candidate evaluations"
          accent="blue"
        />
        <StatCard
          label="Avg NeuroHire Score"
          value={`${stats.avgScore.toFixed(1)}%`}
          note="Across evaluation history"
          accent="indigo"
        />
        <StatCard
          label="Average Skill Match"
          value={`${stats.avgSkill.toFixed(1)}%`}
          note="Resume ↔ JD alignment"
          accent="green"
        />
        <StatCard
          label="Opportunity Ready"
          value={stats.ready}
          note="Score ≥ 75 threshold"
          accent="violet"
        />
      </section>

      <section className="insight-banner">
        <div className="insight-icon">✦</div>
        <div>
          <strong>NeuroHire Intelligence</strong>
          <p>
            {topMissingSkills.length
              ? `Most frequent current skill gaps: ${topMissingSkills
                  .map(([skill]) => skill)
                  .join(", ")}.`
              : "Evaluate candidates to generate skill-gap intelligence."}
          </p>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <div className="panel-heading">
            <div>
              <h3>Skill Gaps (Intervention Priority)</h3>
              <p>Most frequently missing skills across saved evaluations</p>
            </div>
          </div>

          <div className="gap-list">
            {topMissingSkills.length ? (
              topMissingSkills.map(([skill, count], index) => (
                <div className="gap-row" key={skill}>
                  <span className="gap-rank">{index + 1}</span>
                  <div className="gap-info">
                    <strong>{skill}</strong>
                    <small>{count} candidate gap(s)</small>
                  </div>
                  <span className="severity">
                    {index < 2 ? "High" : "Medium"}
                  </span>
                </div>
              ))
            ) : (
              <EmptyState text="No skill-gap data yet." />
            )}
          </div>
        </div>

        <div className="panel">
          <div className="panel-heading">
            <div>
              <h3>Recent Candidate Evaluations</h3>
              <p>Latest NeuroHire decisions</p>
            </div>
          </div>

          <div className="recent-list">
            {latest.length ? (
              latest.map((item) => (
                <div className="recent-row" key={item.id}>
                  <div className="candidate-dot">
                    {initials(item.candidate_name)}
                  </div>
                  <div>
                    <strong>{item.candidate_name}</strong>
                    <small>{item.recommendation || "Not Available"}</small>
                  </div>
                  <div className="recent-score">
                    {formatPercent(item.neural_network_score)}
                  </div>
                </div>
              ))
            ) : (
              <EmptyState text="No evaluations saved yet." />
            )}
          </div>
        </div>
      </section>
    </>
  );
}

function EvaluateScreen({
  jobDescription,
  setJobDescription,
  resumes,
  handleFiles,
  setResumes,
  loading,
  evaluateCandidates,
}) {
  return (
    <>
      <PageHeading
        eyebrow="WORKSPACE INGESTION ENGINE"
        title="AI Candidate Evaluation Workspace"
        subtitle="Parse job descriptions, extract skill taxonomies, and analyze applicant resumes against real neural benchmarks."
      />

      <section className="evaluate-grid">
        <div className="panel evaluate-panel">
          <div className="section-title-row">
            <div>
              <h3>Job Description Analysis</h3>
              <p>Raw JD semantic parser & extractor</p>
            </div>
            <span className="verified-pill">✓ JD analyzed by NeuroHire AI</span>
          </div>

          <label className="field-label">SOURCE ROLE DESCRIPTION</label>
          <textarea
            className="jd-textarea"
            placeholder="Paste the role requirements here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
          <div className="char-count">{jobDescription.length} characters</div>
        </div>

        <div className="panel evaluate-panel">
          <div className="section-title-row">
            <div>
              <h3>Candidate Resumes & Ingestion</h3>
              <p>Multi-document PDF/DOCX processing</p>
            </div>
            <span className="verified-pill">✓ PII-aware workflow</span>
          </div>

          <label className="upload-zone">
            <div className="upload-glyph">⇧</div>
            <strong>Drop candidate resumes here or click to browse</strong>
            <span>PDF / DOCX • Multiple candidates supported</span>
            <input
              type="file"
              multiple
              accept=".pdf,.docx"
              onChange={handleFiles}
            />
          </label>

          {resumes.length > 0 && (
            <div className="file-queue">
              <div className="queue-head">
                <span>{resumes.length} file(s) ready</span>
                <button onClick={() => setResumes([])}>Clear</button>
              </div>
              {resumes.map((file, index) => (
                <div className="queue-item" key={`${file.name}-${index}`}>
                  <span className="file-icon">▣</span>
                  <div>
                    <strong>{file.name}</strong>
                    <small>{(file.size / 1024 / 1024).toFixed(2)} MB</small>
                  </div>
                  <span className="ready-chip">Ready</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      <section className="pipeline panel">
        <div className="panel-heading">
          <div>
            <h3>Neural Inference Pipeline Architecture</h3>
            <p>Real-time evaluation stages</p>
          </div>
          <span className={loading ? "live-pill" : "idle-pill"}>
            {loading ? "Execution Active" : "Ready"}
          </span>
        </div>

        <div className="pipeline-steps">
          {[
            "Parsing Resume",
            "Extracting Skills",
            "Job Req Match",
            "Skill Match Index",
            "Neural Scoring",
            "Readiness Insights",
          ].map((step, index) => (
            <div className="pipeline-step" key={step}>
              <span>Stage 0{index + 1}</span>
              <strong>{step}</strong>
              <div className="tiny-progress">
                <div
                  style={{
                    width: loading
                      ? `${Math.min(100, 25 + index * 13)}%`
                      : "0%",
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </section>

      <div className="execute-bar">
        <div>
          <strong>Execution Safety Audit</strong>
          <span>Skills-based scoring with human decision support.</span>
        </div>
        <button
          className="primary large"
          onClick={evaluateCandidates}
          disabled={loading}
        >
          {loading ? "Analyzing Candidates..." : "Analyze & Rank Candidates →"}
        </button>
      </div>
    </>
  );
}

function RankingScreen({ result, onInspect, onCompare }) {
  const ranking = result?.ranking || [];

  return (
    <>
      <PageHeading
        eyebrow="FLAGSHIP NEURAL INFERENCE"
        title="AI Candidate Ranking"
        subtitle="Candidates ranked using skill alignment, experience, education, JD semantic similarity and neural-network scoring."
        action={
          <button
            className="primary"
            onClick={onCompare}
            disabled={!ranking.length}
          >
            ⇄ Compare Candidates
          </button>
        }
      />

      {!ranking.length ? (
        <EmptyPanel text="Run an evaluation first to generate candidate rankings." />
      ) : (
        <>
          <section className="ranking-summary">
            <SummaryCard
              label="Candidates Evaluated"
              value={result.total_evaluated ?? ranking.length}
            />
            <SummaryCard
              label="Top Score"
              value={`${Number(ranking[0]?.evaluation?.neural_network_score || 0).toFixed(1)}%`}
            />
            <SummaryCard
              label="Strong Matches"
              value={
                ranking.filter(
                  (c) => c.evaluation?.recommendation === "Strong Match",
                ).length
              }
            />
          </section>

          <section className="panel ranking-panel">
            <div className="table-head">
              <span>Rank</span>
              <span>Candidate</span>
              <span>NeuroHire Score</span>
              <span>Skill Match</span>
              <span>Required Skills</span>
              <span>Experience</span>
              <span>Readiness</span>
              <span>Action</span>
            </div>

            {ranking.map((candidate, index) => {
              const e = candidate.evaluation || {};
              const readiness = calculateReadiness(e);

              return (
                <div
                  className="rank-row"
                  key={`${candidate.rank}-${candidate.candidate_name}`}
                >
                  <div className="rank-number">{candidate.rank}</div>
                  <div className="candidate-cell">
                    <div className="candidate-avatar">
                      {initials(candidate.candidate_name)}
                    </div>
                    <div>
                      <strong>{candidate.candidate_name}</strong>
                      <small>{e.recommendation || "Not Available"}</small>
                    </div>
                  </div>
                  <ScoreRing value={e.neural_network_score} />
                  <BarMetric value={e.skill_match} />
                  <div className="table-metric">
                    <strong>{formatPercent(e.required_skill_match)}</strong>
                    <small>
                      {(e.matched_required_skills || []).length}/
                      {(e.required_skills || []).length || 0} matched
                    </small>
                  </div>
                  <div className="table-metric">
                    <strong>{e.experience_years ?? 0} yrs</strong>
                    <small>Target: {e.required_experience ?? 0} yrs</small>
                  </div>
                  <ReadinessBadge value={readiness} />
                  <button
                    className="link-button"
                    onClick={() => onInspect(index)}
                  >
                    Inspect →
                  </button>
                </div>
              );
            })}
          </section>
        </>
      )}
    </>
  );
}

function CompareCandidatesScreen({ ranking, onInspect }) {
  const [selectedIndexes, setSelectedIndexes] = useState(() =>
    (ranking || [])
      .slice(0, Math.min(2, ranking.length))
      .map((_, index) => index),
  );

  useEffect(() => {
    setSelectedIndexes(
      (ranking || [])
        .slice(0, Math.min(2, ranking.length))
        .map((_, index) => index),
    );
  }, [ranking]);

  if (!ranking?.length) {
    return (
      <EmptyPanel text="Run a multi-candidate evaluation first to compare candidates." />
    );
  }

  const toggleCandidate = (index) => {
    setSelectedIndexes((current) => {
      if (current.includes(index)) {
        if (current.length <= 2) return current;
        return current.filter((item) => item !== index);
      }

      if (current.length >= 4) return current;

      return [...current, index].sort((a, b) => a - b);
    });
  };

  const compared = selectedIndexes
    .map((index) => ({ index, candidate: ranking[index] }))
    .filter((item) => item.candidate);

  const recommended = [...compared].sort(
    (a, b) =>
      safeNumber(b.candidate?.evaluation?.neural_network_score) -
      safeNumber(a.candidate?.evaluation?.neural_network_score),
  )[0];

  const metricRows = [
    {
      key: "neural_network_score",
      label: "NeuroHire Score",
      format: formatPercent,
      higherIsBetter: true,
    },
    {
      key: "required_skill_match",
      label: "Required Skill Match",
      format: formatPercent,
      higherIsBetter: true,
    },
    {
      key: "preferred_skill_match",
      label: "Preferred Skill Match",
      format: formatPercent,
      higherIsBetter: true,
    },
    {
      key: "weighted_skill_match",
      label: "Weighted Skill Match",
      format: formatPercent,
      higherIsBetter: true,
    },
    {
      key: "jd_similarity",
      label: "JD Similarity",
      format: formatPercent,
      higherIsBetter: true,
    },
    {
      key: "experience_score",
      label: "Experience Score",
      format: formatPercent,
      higherIsBetter: true,
    },
    {
      key: "education_score",
      label: "Education Score",
      format: formatPercent,
      higherIsBetter: true,
    },
    {
      key: "readiness",
      label: "Opportunity Readiness",
      format: formatPercent,
      higherIsBetter: true,
      derive: (evaluation) => calculateReadiness(evaluation),
    },
  ];

  const bestForMetric = (metric) => {
    if (!compared.length) return null;

    return compared.reduce((best, item) => {
      const evaluation = item.candidate?.evaluation || {};
      const bestEvaluation = best.candidate?.evaluation || {};

      const value = metric.derive
        ? metric.derive(evaluation)
        : safeNumber(evaluation[metric.key]);

      const bestValue = metric.derive
        ? metric.derive(bestEvaluation)
        : safeNumber(bestEvaluation[metric.key]);

      return value > bestValue ? item : best;
    }, compared[0]);
  };

  return (
    <>
      <PageHeading
        eyebrow="SIDE-BY-SIDE DECISION SUPPORT"
        title="Candidate Comparison"
        subtitle="Compare 2–4 candidates across NeuroHire score, skill alignment, experience, education, semantic similarity and opportunity readiness."
      />

      <section className="compare-selector panel">
        <div className="panel-heading">
          <div>
            <h3>Select Candidates</h3>
            <p>
              Choose between 2 and 4 candidates for a fair side-by-side
              comparison.
            </p>
          </div>
          <span className="compare-count">
            {selectedIndexes.length}/4 selected
          </span>
        </div>

        <div className="compare-selector-grid">
          {ranking.map((candidate, index) => {
            const selected = selectedIndexes.includes(index);
            const disabled = !selected && selectedIndexes.length >= 4;

            return (
              <button
                type="button"
                className={`compare-select-card ${selected ? "selected" : ""}`}
                key={`${candidate.rank}-${candidate.candidate_name}`}
                onClick={() => toggleCandidate(index)}
                disabled={disabled}
              >
                <span className="compare-check">{selected ? "✓" : "+"}</span>
                <div className="candidate-avatar">
                  {initials(candidate.candidate_name)}
                </div>
                <div>
                  <strong>{candidate.candidate_name}</strong>
                  <small>
                    Rank #{candidate.rank} •{" "}
                    {formatPercent(candidate.evaluation?.neural_network_score)}
                  </small>
                </div>
              </button>
            );
          })}
        </div>

        {selectedIndexes.length < 2 && (
          <div className="compare-warning">
            Select at least two candidates to compare.
          </div>
        )}
      </section>

      {compared.length >= 2 && (
        <>
          <section className="compare-hero-grid">
            {compared.map(({ index, candidate }) => {
              const evaluation = candidate.evaluation || {};
              const isRecommended = recommended?.index === index;

              return (
                <div
                  className={`compare-candidate-card ${
                    isRecommended ? "recommended" : ""
                  }`}
                  key={`${candidate.rank}-${candidate.candidate_name}`}
                >
                  {isRecommended && (
                    <span className="recommended-ribbon">
                      🏆 Recommended Candidate
                    </span>
                  )}

                  <div className="compare-candidate-top">
                    <div className="candidate-avatar xl">
                      {initials(candidate.candidate_name)}
                    </div>
                    <div>
                      <h3>{candidate.candidate_name}</h3>
                      <span>
                        Rank #{candidate.rank} •{" "}
                        {evaluation.recommendation || "Not Available"}
                      </span>
                    </div>
                  </div>

                  <div className="compare-score-block">
                    <ScoreRing value={evaluation.neural_network_score} />
                    <div>
                      <span>NeuroHire Score</span>
                      <strong>
                        {formatPercent(evaluation.neural_network_score)}
                      </strong>
                    </div>
                  </div>

                  <div className="compare-readiness-line">
                    <span>Opportunity Readiness</span>
                    <strong>
                      {formatPercent(calculateReadiness(evaluation))}
                    </strong>
                  </div>

                  <button
                    className="secondary compare-inspect"
                    onClick={() => onInspect(index)}
                  >
                    Inspect Candidate →
                  </button>
                </div>
              );
            })}
          </section>

          <section className="panel comparison-matrix">
            <div
              className="comparison-grid comparison-grid-head"
              style={{
                gridTemplateColumns: `minmax(180px, 1.2fr) repeat(${compared.length}, minmax(170px, 1fr))`,
              }}
            >
              <div>Evaluation Dimension</div>
              {compared.map(({ candidate }) => (
                <div key={`head-${candidate.rank}-${candidate.candidate_name}`}>
                  {candidate.candidate_name}
                </div>
              ))}
            </div>

            {metricRows.map((metric) => {
              const best = bestForMetric(metric);

              return (
                <div
                  className="comparison-grid comparison-grid-row"
                  style={{
                    gridTemplateColumns: `minmax(180px, 1.2fr) repeat(${compared.length}, minmax(170px, 1fr))`,
                  }}
                  key={metric.key}
                >
                  <div className="comparison-label">{metric.label}</div>

                  {compared.map(({ index, candidate }) => {
                    const evaluation = candidate.evaluation || {};
                    const value = metric.derive
                      ? metric.derive(evaluation)
                      : evaluation[metric.key];

                    const isBest = best?.index === index;

                    return (
                      <div
                        className={`comparison-value ${isBest ? "best-metric" : ""}`}
                        key={`${metric.key}-${index}`}
                      >
                        <strong>{metric.format(value)}</strong>
                        {isBest && <span>Best</span>}
                      </div>
                    );
                  })}
                </div>
              );
            })}

            <div
              className="comparison-grid comparison-grid-row"
              style={{
                gridTemplateColumns: `minmax(180px, 1.2fr) repeat(${compared.length}, minmax(170px, 1fr))`,
              }}
            >
              <div className="comparison-label">Experience</div>
              {compared.map(({ index, candidate }) => {
                const evaluation = candidate.evaluation || {};
                return (
                  <div className="comparison-value" key={`exp-${index}`}>
                    <strong>{evaluation.experience_years ?? 0} yrs</strong>
                    <small>
                      Target: {evaluation.required_experience ?? 0} yrs
                    </small>
                  </div>
                );
              })}
            </div>
          </section>

          <section className="compare-detail-grid">
            {compared.map(({ index, candidate }) => {
              const evaluation = candidate.evaluation || {};

              return (
                <div
                  className="panel compare-detail-card"
                  key={`detail-${candidate.rank}-${candidate.candidate_name}`}
                >
                  <div className="compare-detail-head">
                    <div>
                      <h3>{candidate.candidate_name}</h3>
                      <p>Skills profile comparison</p>
                    </div>
                    <button
                      className="link-button"
                      onClick={() => onInspect(index)}
                    >
                      Inspect →
                    </button>
                  </div>

                  <div className="compare-skill-section positive">
                    <strong>✓ Matched Required Skills</strong>
                    <div className="skill-chip-wrap">
                      {(evaluation.matched_required_skills || []).length ? (
                        evaluation.matched_required_skills.map((skill) => (
                          <span
                            className="compare-skill-chip matched"
                            key={`m-${skill}`}
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span className="empty-chip">None</span>
                      )}
                    </div>
                  </div>

                  <div className="compare-skill-section negative">
                    <strong>✕ Critical Missing Skills</strong>
                    <div className="skill-chip-wrap">
                      {(evaluation.missing_required_skills || []).length ? (
                        evaluation.missing_required_skills.map((skill) => (
                          <span
                            className="compare-skill-chip missing"
                            key={`x-${skill}`}
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span className="empty-chip">None</span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </section>

          <section className="compare-decision-note">
            <div className="insight-icon">✦</div>
            <div>
              <strong>Decision Support Summary</strong>
              <p>
                {recommended?.candidate?.candidate_name} currently has the
                highest NeuroHire score among the selected candidates. This is
                an AI-assisted recommendation based on job-related evaluation
                dimensions; the final recruitment decision should remain with
                the human reviewer.
              </p>
            </div>
          </section>
        </>
      )}
    </>
  );
}

function CandidateIntelligence({
  candidate,
  evaluation,
  onRoadmap,
  onCompare,
}) {
  if (!candidate) {
    return (
      <EmptyPanel text="Select a ranked candidate to inspect intelligence." />
    );
  }

  const readiness = calculateReadiness(evaluation);

  return (
    <>
      <div className="candidate-header-card">
        <div className="candidate-avatar xl">
          {initials(candidate.candidate_name)}
        </div>
        <div className="candidate-head-copy">
          <div className="candidate-name-line">
            <h2>{candidate.candidate_name}</h2>
            <span className="id-pill">Rank #{candidate.rank}</span>
          </div>
          <span className="readiness-line">
            ⚡ Opportunity Readiness: {readiness}%
          </span>
          <small>{evaluation.recommendation || "Not Available"}</small>
        </div>
        <div className="candidate-header-actions">
          <button className="secondary" onClick={onCompare}>
            ⇄ Compare
          </button>
          <button className="primary" onClick={onRoadmap}>
            ✦ Upskilling Plan
          </button>
        </div>
      </div>

      <section className="intelligence-top">
        <div className="panel score-panel">
          <p className="eyebrow">NEUROHIRE INDEX</p>
          <ScoreDonut value={evaluation.neural_network_score} />
          <strong>Neural Composite Index</strong>
          <span>{evaluation.recommendation || "Not Available"}</span>
        </div>

        <div className="panel explanation-panel">
          <div className="panel-heading">
            <div>
              <h3>Why this result?</h3>
              <p>
                Deterministic semantic explanation based on current model
                outputs
              </p>
            </div>
            <span className="audit-pill">Auditable</span>
          </div>
          <div className="explanation-box">
            {evaluation.recommendation_reason || "No explanation available."}
          </div>
          <div className="explain-mini-grid">
            <MiniFact
              label="Matched Required"
              value={`${(evaluation.matched_required_skills || []).length}`}
            />
            <MiniFact
              label="Missing Required"
              value={`${(evaluation.missing_required_skills || []).length}`}
            />
            <MiniFact
              label="Experience"
              value={`${evaluation.experience_years ?? 0} yrs`}
            />
          </div>
        </div>
      </section>

      <h3 className="section-heading">Dimensional Evaluation Matrix</h3>
      <section className="metric-matrix">
        <MetricCard
          label="Overall Skill Match"
          value={evaluation.skill_match}
        />
        <MetricCard
          label="Required Skill Match"
          value={evaluation.required_skill_match}
        />
        <MetricCard
          label="Preferred Skill Match"
          value={evaluation.preferred_skill_match}
        />
        <MetricCard
          label="Weighted Skill Match"
          value={evaluation.weighted_skill_match}
        />
        <MetricCard
          label="JD Semantic Similarity"
          value={evaluation.jd_similarity}
        />
        <MetricCard
          label="Experience Score"
          value={evaluation.experience_score}
        />
        <MetricCard
          label="Education Score"
          value={evaluation.education_score}
        />
        <MetricCard label="Opportunity Readiness" value={readiness} />
      </section>

      <section className="panel explainability-panel">
        <div className="panel-heading">
          <div>
            <h3>Why did NeuroHire give this score?</h3>
            <p>Transparent positive contributors and improvement factors</p>
          </div>
        </div>

        <div className="contributors-grid">
          <div className="contributor-column positive">
            <h4>✓ Positive Contributors</h4>
            {(evaluation.matched_required_skills || [])
              .slice(0, 5)
              .map((skill) => (
                <div className="contributor-card" key={skill}>
                  <strong>{skill}</strong>
                  <span>Required skill detected in candidate profile</span>
                </div>
              ))}
            {Number(evaluation.education_score || 0) >= 75 && (
              <div className="contributor-card">
                <strong>Education Requirement Satisfied</strong>
                <span>Education score contributes positively</span>
              </div>
            )}
          </div>

          <div className="contributor-column negative">
            <h4>✕ Critical Improvement Factors</h4>
            {(evaluation.missing_required_skills || [])
              .slice(0, 5)
              .map((skill) => (
                <div className="contributor-card" key={skill}>
                  <strong>{skill}</strong>
                  <span>
                    Missing required skill reduces opportunity readiness
                  </span>
                </div>
              ))}
          </div>
        </div>

        <div className="responsible-ai">
          <strong>Responsible AI & Governance</strong>
          <span>
            NeuroHire supports transparent skills-based decision-making and does
            not replace final human recruitment judgment.
          </span>
        </div>
      </section>
    </>
  );
}

function RoadmapScreen({ candidate, evaluation }) {
  if (!candidate) {
    return (
      <EmptyPanel text="Select a candidate to generate a skill-gap roadmap." />
    );
  }

  const readiness = calculateReadiness(evaluation);
  const recs = evaluation.certificate_recommendations || [];
  const projected = Math.min(100, readiness + Math.min(25, recs.length * 5));

  return (
    <>
      <div className="candidate-header-card">
        <div className="candidate-avatar xl">
          {initials(candidate.candidate_name)}
        </div>
        <div className="candidate-head-copy">
          <h2>{candidate.candidate_name}</h2>
          <span className="readiness-line">AI Upskilling Active</span>
          <small>{evaluation.recommendation || "Not Available"}</small>
        </div>
      </div>

      <section className="readiness-journey panel">
        <div className="journey-score">
          <ScoreRing value={readiness} />
          <div>
            <span>Current State</span>
            <strong>Readiness Now</strong>
          </div>
        </div>
        <div className="journey-arrow">→</div>
        <div className="journey-score">
          <ScoreRing value={projected} />
          <div>
            <span>Projected State</span>
            <strong>Potential Readiness</strong>
          </div>
        </div>
        <div className="journey-advice">
          <strong>✦ NeuroHire Recommendation</strong>
          <p>
            Prioritize required-skill gaps first, then address preferred skills
            to improve role alignment.
          </p>
        </div>
      </section>

      <h3 className="section-heading">Skill Gap Intelligence</h3>
      <section className="skill-gap-grid">
        <SkillBucket
          title="Matched Required"
          count={(evaluation.matched_required_skills || []).length}
          skills={evaluation.matched_required_skills}
          type="matched"
        />
        <SkillBucket
          title="Missing Required"
          count={(evaluation.missing_required_skills || []).length}
          skills={evaluation.missing_required_skills}
          type="missing"
        />
        <SkillBucket
          title="Matched Preferred"
          count={(evaluation.matched_preferred_skills || []).length}
          skills={evaluation.matched_preferred_skills}
          type="matched"
        />
        <SkillBucket
          title="Missing Preferred"
          count={(evaluation.missing_preferred_skills || []).length}
          skills={evaluation.missing_preferred_skills}
          type="preferred"
        />
      </section>

      <section className="panel gap-table-panel">
        <div className="gap-table-head">
          <span>Skill Entity</span>
          <span>Gap Severity</span>
          <span>Classification</span>
          <span>Action</span>
        </div>
        {(evaluation.missing_required_skills || []).map((skill) => (
          <div className="gap-table-row" key={`req-${skill}`}>
            <strong>{skill}</strong>
            <span className="high-gap">HIGH GAP</span>
            <span>Critical Required</span>
            <span className="linkish">View Learning Path</span>
          </div>
        ))}
        {(evaluation.missing_preferred_skills || []).map((skill) => (
          <div className="gap-table-row" key={`pref-${skill}`}>
            <strong>{skill}</strong>
            <span className="medium-gap">MEDIUM GAP</span>
            <span>Preferred</span>
            <span className="linkish">View Learning Path</span>
          </div>
        ))}
      </section>

      <div className="roadmap-title">
        <div>
          <h3>Personalized Learning Roadmap</h3>
          <p>
            NeuroHire converts detected skill gaps into actionable certification
            and learning recommendations.
          </p>
        </div>
        <span>{recs.length} learning recommendation(s)</span>
      </div>

      <section className="roadmap-list">
        {recs.length ? (
          recs.map((recommendation, index) => (
            <div
              className="roadmap-card"
              key={`${recommendation.skill}-${index}`}
            >
              <div className="roadmap-index">{index + 1}</div>
              <div className="roadmap-main">
                <div className="roadmap-card-head">
                  <div>
                    <h3>{recommendation.skill}</h3>
                    <span>
                      {recommendation.skill_type || "Skill Gap"} •{" "}
                      {recommendation.priority || "Medium"} Priority
                    </span>
                  </div>
                  <span
                    className={
                      recommendation.priority === "High"
                        ? "priority high"
                        : "priority medium"
                    }
                  >
                    {recommendation.priority || "Medium"} Priority
                  </span>
                </div>

                <div className="roadmap-reason">
                  <strong>AI Justification:</strong> {recommendation.reason}
                </div>

                {(recommendation.certificates || []).map((cert, certIndex) => (
                  <div
                    className="certificate-line"
                    key={`${cert.name}-${certIndex}`}
                  >
                    <div className="certificate-symbol">🎓</div>
                    <div>
                      <strong>{cert.name}</strong>
                      <span>
                        Provider: {cert.provider} • Level: {cert.level}
                      </span>
                    </div>
                    <button
                      className="primary compact"
                      onClick={() =>
                        window.open(
                          cert.url ||
                            `https://www.google.com/search?q=${encodeURIComponent(
                              `${cert.name} ${cert.provider}`,
                            )}`,
                          "_blank",
                          "noopener,noreferrer",
                        )
                      }
                    >
                      Start Learning ↗
                    </button>
                  </div>
                ))}
              </div>
            </div>
          ))
        ) : (
          <EmptyPanel text="No certification recommendations were generated for this candidate." />
        )}
      </section>
    </>
  );
}
function TechnicalAssessmentScreen({ candidate, evaluation }) {
  const [assessment, setAssessment] = useState(null);
  const [answers, setAnswers] = useState({});
  const [assessmentResult, setAssessmentResult] = useState(null);
  const [assessmentLoading, setAssessmentLoading] = useState(false);
  const [assessmentError, setAssessmentError] = useState("");

  useEffect(() => {
    setAssessment(null);
    setAnswers({});
    setAssessmentResult(null);
    setAssessmentError("");
  }, [candidate]);

  if (!candidate) {
    return (
      <EmptyPanel text="Evaluate and select a candidate before starting the technical assessment." />
    );
  }

  const candidateName =
    candidate?.candidate_name ||
    candidate?.candidate?.file_name ||
    candidate?.file_name ||
    "Selected Candidate";

  const candidateId = String(
    candidate?.evaluation_id || candidate?.id || candidateName,
  );

  const targetSkills = Array.from(
    new Set([
      ...(evaluation?.missing_required_skills || []),
      ...(evaluation?.missing_preferred_skills || []),
    ]),
  );

  const generateAssessment = async () => {
    setAssessmentLoading(true);
    setAssessmentError("");
    setAssessmentResult(null);
    setAnswers({});

    try {
      const response = await axios.post(`${API_BASE_URL}/assessment/generate`, {
        candidate_id: candidateId,
        skills: targetSkills,
        num_questions: Math.min(4, Math.max(1, targetSkills.length || 4)),
      });
      setAssessment(response.data);
    } catch (err) {
      console.error(err);
      setAssessmentError(
        err.response?.data?.detail || "Unable to generate technical assessment.",
      );
    } finally {
      setAssessmentLoading(false);
    }
  };

  const submitAssessment = async () => {
    if (!assessment?.questions?.length) return;

    const unanswered = assessment.questions.some(
      (question) => !String(answers[question.question_id] || "").trim(),
    );

    if (unanswered) {
      setAssessmentError("Please answer every question before submitting.");
      return;
    }

    setAssessmentLoading(true);
    setAssessmentError("");

    try {
      const response = await axios.post(`${API_BASE_URL}/assessment/evaluate`, {
        candidate_id: candidateId,
        resume_score: Number(evaluation?.neural_network_score || 0),
        questions: assessment.questions,
        answers,
      });
      setAssessmentResult(response.data);
    } catch (err) {
      console.error(err);
      setAssessmentError(
        err.response?.data?.detail || "Unable to evaluate assessment answers.",
      );
    } finally {
      setAssessmentLoading(false);
    }
  };

  return (
    <>
      <PageHeading
        eyebrow="SKILL-GAP VALIDATION ENGINE"
        title="Targeted Technical Assessment"
        subtitle="Validate candidate capability through skill-gap-aware technical questions and direct evidence."
      />

      {assessmentError && (
        <div className="alert error-alert">{assessmentError}</div>
      )}

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h3>{candidateName}</h3>
            <p>
              NeuroHire targets the candidate's detected skill gaps and converts
              their answers into evidence-backed assessment signals.
            </p>
          </div>
          <span className="audit-pill">Human-in-the-Loop</span>
        </div>

        <div className="skill-chip-wrap">
          {targetSkills.length ? (
            targetSkills.slice(0, 8).map((skill) => (
              <span className="skill-chip" key={skill}>
                × {skill}
              </span>
            ))
          ) : (
            <span className="empty-chip">
              No missing skills detected. A problem-solving question will be used.
            </span>
          )}
        </div>

        {!assessment && (
          <div style={{ marginTop: "24px" }}>
            <button
              className="primary"
              onClick={generateAssessment}
              disabled={assessmentLoading}
            >
              {assessmentLoading
                ? "Generating Assessment..."
                : "Generate Technical Assessment →"}
            </button>
          </div>
        )}
      </section>

      {assessment?.questions?.length > 0 && !assessmentResult && (
        <section className="panel" style={{ marginTop: "18px" }}>
          <div className="panel-heading">
            <div>
              <h3>Technical Questions</h3>
              <p>
                Assessment ID: {assessment.assessment_id || "Generated"} • Answer
                all questions before submission.
              </p>
            </div>
            <span className="verified-pill">
              {assessment.questions.length} Question(s)
            </span>
          </div>

          <div style={{ display: "grid", gap: "18px" }}>
            {assessment.questions.map((question, index) => (
              <div className="contributor-card" key={question.question_id}>
                <div style={{ marginBottom: "10px" }}>
                  <span className="eyebrow">
                    QUESTION {index + 1} • {question.skill || "Technical"}
                  </span>
                  <h3 style={{ marginTop: "6px" }}>{question.question}</h3>
                </div>
                <textarea
                  className="jd-textarea"
                  style={{ minHeight: "120px" }}
                  placeholder="Write your answer here..."
                  value={answers[question.question_id] || ""}
                  onChange={(event) =>
                    setAnswers((current) => ({
                      ...current,
                      [question.question_id]: event.target.value,
                    }))
                  }
                />
              </div>
            ))}
          </div>

          <div style={{ marginTop: "22px", display: "flex", gap: "12px" }}>
            <button
              className="primary"
              onClick={submitAssessment}
              disabled={assessmentLoading}
            >
              {assessmentLoading ? "Evaluating..." : "Submit Assessment →"}
            </button>
            <button
              className="secondary"
              onClick={generateAssessment}
              disabled={assessmentLoading}
            >
              Regenerate Questions
            </button>
          </div>
        </section>
      )}

      {assessmentResult && (
        <>
          <section className="ranking-summary" style={{ marginTop: "18px" }}>
            <SummaryCard
              label="Resume Score"
              value={`${Number(assessmentResult.resume_score || 0).toFixed(1)}%`}
            />
            <SummaryCard
              label="Assessment Score"
              value={`${Number(assessmentResult.overall_score || 0).toFixed(1)}%`}
            />
            <SummaryCard
              label="Combined Readiness"
              value={`${Number(
                assessmentResult.combined_readiness_score || 0,
              ).toFixed(1)}%`}
            />
            <SummaryCard
              label="Evidence Confidence"
              value={`${Math.round(
                Number(assessmentResult.confidence || 0) * 100,
              )}%`}
            />
          </section>

          <section className="panel" style={{ marginTop: "18px" }}>
            <div className="panel-heading">
              <div>
                <h3>Evidence-Backed Assessment</h3>
                <p>
                  Direct answer evidence supplements the resume-based NeuroHire
                  evaluation. Final hiring decisions remain with recruiters.
                </p>
              </div>
              <ReadinessBadge
                value={Number(assessmentResult.combined_readiness_score || 0)}
              />
            </div>

            <div className="contributors-grid">
              <div className="contributor-column positive">
                <h4>✓ Demonstrated Strengths</h4>
                {(assessmentResult.strengths || []).length ? (
                  assessmentResult.strengths.map((skill) => (
                    <div className="contributor-card" key={`strength-${skill}`}>
                      <strong>{skill}</strong>
                      <span>Assessment evidence indicates acceptable coverage.</span>
                    </div>
                  ))
                ) : (
                  <div className="contributor-card">
                    <span>No strong skill evidence detected yet.</span>
                  </div>
                )}
              </div>

              <div className="contributor-column negative">
                <h4>✕ Improvement Areas</h4>
                {(assessmentResult.weaknesses || []).length ? (
                  assessmentResult.weaknesses.map((skill) => (
                    <div className="contributor-card" key={`weakness-${skill}`}>
                      <strong>{skill}</strong>
                      <span>Further validation or upskilling is recommended.</span>
                    </div>
                  ))
                ) : (
                  <div className="contributor-card">
                    <span>No major assessment weakness detected.</span>
                  </div>
                )}
              </div>
            </div>
          </section>

          <section className="panel" style={{ marginTop: "18px" }}>
            <div className="panel-heading">
              <div>
                <h3>Question-Level Evidence</h3>
                <p>Concept coverage, confidence and auditable evidence IDs.</p>
              </div>
            </div>

            <div style={{ display: "grid", gap: "14px" }}>
              {(assessmentResult.question_results || []).map((item, index) => (
                <div className="contributor-card" key={item.evidence_id || index}>
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      gap: "16px",
                      alignItems: "flex-start",
                    }}
                  >
                    <div>
                      <span className="eyebrow">
                        {item.skill || "Technical"} • {item.evidence_id}
                      </span>
                      <strong style={{ display: "block", marginTop: "6px" }}>
                        {item.question}
                      </strong>
                    </div>
                    <span className="recommend-chip">
                      {Number(item.score || 0).toFixed(1)}%
                    </span>
                  </div>

                  <div className="skill-chip-wrap" style={{ marginTop: "12px" }}>
                    {(item.matched_concepts || []).map((concept) => (
                      <span
                        className="compare-skill-chip matched"
                        key={`matched-${item.question_id}-${concept}`}
                      >
                        ✓ {concept}
                      </span>
                    ))}
                    {(item.missing_concepts || []).map((concept) => (
                      <span
                        className="compare-skill-chip missing"
                        key={`missing-${item.question_id}-${concept}`}
                      >
                        × {concept}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div style={{ marginTop: "22px" }}>
              <button
                className="secondary"
                onClick={() => {
                  setAssessment(null);
                  setAssessmentResult(null);
                  setAnswers({});
                  setAssessmentError("");
                }}
              >
                Start New Assessment
              </button>
            </div>
          </section>
        </>
      )}
    </>
  );
}


function HistoryScreen({ history, loading, exportCSV, refresh, onDelete }) {
  return (
    <>
      <PageHeading
        eyebrow="AUDIT TRAIL & PROVENANCE"
        title="Candidate Evaluation History"
        subtitle="Searchable archive of saved candidate evaluations and scoring records."
        action={
          <div className="heading-actions">
            <button className="secondary" onClick={refresh}>
              ↻ Refresh
            </button>
            <button className="primary" onClick={exportCSV}>
              ⇩ Export CSV
            </button>
          </div>
        }
      />

      {loading ? (
        <EmptyPanel text="Loading evaluation history..." />
      ) : !history.length ? (
        <EmptyPanel text="No evaluation history found." />
      ) : (
        <section className="panel history-table">
          <div className="history-table-head">
            <span>Candidate</span>
            <span>Score</span>
            <span>Skill Alignment</span>
            <span>Top Missing Gap</span>
            <span>Recommendation</span>
            <span>Date</span>
            <span>Action</span>
          </div>
          {history.map((item) => (
            <div className="history-table-row" key={item.id}>
              <div className="candidate-cell">
                <div className="candidate-avatar">
                  {initials(item.candidate_name)}
                </div>
                <div>
                  <strong>{item.candidate_name}</strong>
                  <small>ID #{item.id}</small>
                </div>
              </div>
              <ScoreRing value={item.neural_network_score} compact />
              <BarMetric value={item.skill_match} />
              <span className="gap-chip">
                {(item.missing_required_skills ||
                  item.missing_skills ||
                  [])[0] || "None"}
              </span>
              <span className="recommend-chip">
                {item.recommendation || "Not Available"}
              </span>
              <small>
                {item.created_at
                  ? new Date(item.created_at).toLocaleDateString()
                  : "N/A"}
              </small>
              <button className="delete-link" onClick={() => onDelete(item.id)}>
                Delete
              </button>
            </div>
          ))}
        </section>
      )}
    </>
  );
}

function PageHeading({ eyebrow, title, subtitle, action }) {
  return (
    <div className="page-heading">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
      {action}
    </div>
  );
}

function StatCard({ label, value, note, accent }) {
  return (
    <div className={`stat-card ${accent}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{note}</small>
    </div>
  );
}

function SummaryCard({ label, value }) {
  return (
    <div className="summary-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function MiniBadge({ value, label }) {
  return (
    <div className="mini-badge">
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

function MiniFact({ label, value }) {
  return (
    <div className="mini-fact">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function MetricCard({ label, value }) {
  const num = safeNumber(value);
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{formatPercent(num)}</strong>
      <div className="metric-track">
        <div style={{ width: `${clamp(num)}%` }} />
      </div>
    </div>
  );
}

function SkillBucket({ title, count, skills, type }) {
  const safeSkills = skills || [];
  return (
    <div className={`skill-bucket ${type}`}>
      <div className="bucket-head">
        <strong>{title}</strong>
        <span>{count} skills</span>
      </div>
      <div className="skill-chip-wrap">
        {safeSkills.length ? (
          safeSkills.map((skill) => (
            <span className="skill-chip" key={`${title}-${skill}`}>
              {type === "matched" ? "✓" : "×"} {skill}
            </span>
          ))
        ) : (
          <span className="empty-chip">None</span>
        )}
      </div>
    </div>
  );
}

function ScoreRing({ value, compact = false }) {
  const num = clamp(safeNumber(value));
  return (
    <div
      className={`score-ring ${compact ? "compact" : ""}`}
      style={{
        background: `conic-gradient(#4f46e5 ${num * 3.6}deg, #e9ecf5 0deg)`,
      }}
    >
      <div>
        <strong>{Math.round(num)}</strong>
        {!compact && <small>/100</small>}
      </div>
    </div>
  );
}

function ScoreDonut({ value }) {
  const num = clamp(safeNumber(value));
  return (
    <div
      className="score-donut"
      style={{
        background: `conic-gradient(#4f46e5 ${num * 3.6}deg, #e7eaf3 0deg)`,
      }}
    >
      <div>
        <strong>{Math.round(num)}</strong>
        <span>OUT OF 100</span>
      </div>
    </div>
  );
}

function BarMetric({ value }) {
  const num = clamp(safeNumber(value));
  return (
    <div className="bar-metric">
      <strong>{formatPercent(num)}</strong>
      <div className="bar-track">
        <div style={{ width: `${num}%` }} />
      </div>
    </div>
  );
}

function ReadinessBadge({ value }) {
  const state =
    value >= 75
      ? "Opportunity Ready"
      : value >= 60
        ? "Nearly Ready"
        : "Needs Upskilling";
  return (
    <span
      className={`readiness-badge ${value >= 75 ? "ready" : value >= 60 ? "near" : "needs"}`}
    >
      {state} ({Math.round(value)}%)
    </span>
  );
}

function EmptyPanel({ text }) {
  return (
    <div className="empty-panel">
      <div className="empty-icon">✦</div>
      <h3>{text}</h3>
      <p>Use NeuroHire evaluation to populate this section with real data.</p>
    </div>
  );
}

function EmptyState({ text }) {
  return <div className="inline-empty">{text}</div>;
}

function calculateReadiness(evaluation = {}) {
  const values = [
    safeNumber(evaluation.required_skill_match),
    safeNumber(evaluation.weighted_skill_match),
    safeNumber(evaluation.experience_score),
    safeNumber(evaluation.education_score),
    safeNumber(evaluation.jd_similarity),
  ];

  const weights = [0.35, 0.25, 0.15, 0.15, 0.1];

  return clamp(
    values.reduce((sum, value, index) => sum + value * weights[index], 0),
  );
}

function safeNumber(value) {
  const num = Number(value);
  return Number.isFinite(num) ? num : 0;
}

function clamp(value) {
  return Math.min(100, Math.max(0, value));
}

function formatPercent(value) {
  if (value === null || value === undefined || value === "") return "N/A";
  const num = Number(value);
  return Number.isFinite(num) ? `${Number(num.toFixed(1))}%` : "N/A";
}

function initials(name = "") {
  return (
    name
      .replace(/\.[^.]+$/, "")
      .split(/[\s_-]+/)
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("") || "NH"
  );
}

export default App;
