import { Link } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";

function HowItWorks({ theme, onToggleTheme }) {
  return (
    <div className="shell">
      <div className="hero-card how-card">
        <div className="top-row">
          <Link className="back-link" to="/">Back to analysis</Link>
          <ThemeToggle theme={theme} onToggle={onToggleTheme} />
        </div>

        <div className="how-hero">
          <p className="eyebrow">How It Works</p>
          <h1>From Ciphertext to Prediction</h1>
          <p className="hero-sub">
            The system uses statistical fingerprints extracted from ciphertext
            to classify which cryptographic algorithm produced it. No keys are
            recovered and no decryption is attempted.
          </p>
        </div>

        <div className="how-grid">
          <div className="how-step">
            <p className="how-title">1. Dataset Generation</p>
            <p className="how-text">
              Random plaintext sizes (256 to 2048 bytes) are encrypted using
              AES, DES, 3DES, RC4, ChaCha20, and RSA. Each sample is labeled with
              its algorithm.
            </p>
          </div>
          <div className="how-step">
            <p className="how-title">2. Feature Extraction</p>
            <p className="how-text">
              Each ciphertext is converted into a 264-length feature vector,
              including entropy, chi-square, index of coincidence, length
              properties, block repetition ratios, and 256 byte-frequency values.
            </p>
          </div>
          <div className="how-step">
            <p className="how-title">3. Model Training</p>
            <p className="how-text">
              A Random Forest classifier learns the feature patterns that are
              characteristic of each algorithm. The trained model is stored for
              real-time inference.
            </p>
          </div>
          <div className="how-step">
            <p className="how-title">4. Real-Time Inference</p>
            <p className="how-text">
              When you upload a file, the same features are extracted and passed
              to the model. The API returns the top predictions with calibrated
              confidence. If confidence is below the threshold, the output is
              labeled as Unknown.
            </p>
          </div>
        </div>

        <div className="how-note">
          <p className="how-title">Ethics and Limitations</p>
          <p className="how-text">
            This project performs statistical classification only. It does not
            attempt to break encryption, recover keys, or bypass protections.
          </p>
        </div>
      </div>
    </div>
  );
}

export default HowItWorks;
