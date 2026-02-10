import { Link } from "react-router-dom";
import { useState } from "react";
import ThemeToggle from "./ThemeToggle";

function FileUpload({ theme, onToggleTheme }) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError("Please upload a ciphertext file.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  const confidencePct = result
    ? Math.round(Number(result.confidence) * 100)
    : 0;
  const topPreds = result?.top_predictions || [];
  const isUncertain = result?.is_uncertain;
  const thresholdPct = result?.threshold
    ? Math.round(Number(result.threshold) * 100)
    : null;

  return (
    <div className="shell">
      <div className="hero-card">
        <div className="top-row">
          <div className="top-spacer" />
          <ThemeToggle theme={theme} onToggle={onToggleTheme} />
        </div>

        <div className="hero-grid">
          <div className="hero-word">CRYPTANALYSIS</div>

          <div className="hero-copy">
            <p className="eyebrow">Cryptographic Algorithm Identifier</p>
            <p className="hero-sub">
              ML classifier that identifies modern cryptographic algorithms from
              encrypted datasets using statistical feature extraction.
            </p>
            <div className="metrics">
              <div className="metric">
                <span className="metric-value">3K+</span>
                <span className="metric-label">Encrypted samples</span>
              </div>
              <div className="metric">
                <span className="metric-value">6</span>
                <span className="metric-label">Algorithms supported</span>
              </div>
            </div>
          </div>

          <div className="hero-visual">
            <div className="orb">
              <span className="ring ring-1" />
              <span className="ring ring-2" />
              <span className="ring ring-3" />
            </div>
          </div>

          <div className="hero-side">
            <div className="side-list">
              <p>Web based / 01</p>
              <p>Collaborative / 02</p>
              <p>Real time / 03</p>
            </div>
            <Link className="lime-cta" to="/how-it-works">
              How it works?
            </Link>
          </div>
        </div>

        <section className="analyze-panel">
          <div className="panel-left">
            <h2>Analyze Ciphertext</h2>
            <p>
              Upload a .bin file from the dataset or your own encrypted sample
              to identify the most likely algorithm.
            </p>

            <form onSubmit={handleSubmit} className="upload-form">
              <label className="file-pill">
                <input
                  type="file"
                  onChange={(e) => setFile(e.target.files[0])}
                />
                <span className="file-name">
                  {file ? file.name : "Choose a ciphertext file"}
                </span>
                <span className="file-browse">Browse</span>
              </label>
              <button className="primary-btn" type="submit" disabled={loading}>
                {loading ? "Analyzing..." : "Analyze"}
              </button>
            </form>

            {error && <p className="error">{error}</p>}
          </div>

          <div className="panel-right">
            {result ? (
              <div className="result-card">
                <p className="result-title">Prediction</p>
                <p className="result-algo">
                  {isUncertain ? "Unknown" : result.predicted_algorithm}
                </p>
                {isUncertain && (
                  <p className="result-flag">
                    Low confidence — below {thresholdPct}% threshold
                  </p>
                )}
                <div className="meter">
                  <div
                    className={`meter-fill ${isUncertain ? "meter-uncertain" : ""}`}
                    style={{ width: `${confidencePct}%` }}
                  />
                </div>
                <p className="result-meta">Confidence: {confidencePct}%</p>
                {thresholdPct !== null && (
                  <p className="result-meta">Threshold: {thresholdPct}%</p>
                )}
                {topPreds.length > 0 && (
                  <div className="top-badges">
                    {topPreds.slice(0, 2).map((item, idx) => (
                      <span className="top-badge" key={`${item.algorithm}-${idx}`}>
                        #{idx + 1} {item.algorithm} ·{" "}
                        {Math.round(Number(item.confidence) * 100)}%
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="result-card result-placeholder">
                <p className="result-title">Prediction</p>
                <p className="result-algo">Waiting for input</p>
                <p className="result-meta">Upload a file to see results.</p>
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

export default FileUpload;
