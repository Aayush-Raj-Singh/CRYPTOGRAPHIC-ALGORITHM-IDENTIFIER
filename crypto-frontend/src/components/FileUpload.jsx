import { useState } from "react";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError("Please upload a file");
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
      setError("Error connecting to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Cryptographic Algorithm Identifier</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit">Analyze</button>
      </form>

      {loading && <p>Analyzing...</p>}

      {result && (
        <div className="result">
          <p><strong>Algorithm:</strong> {result.predicted_algorithm}</p>
          <p><strong>Confidence:</strong> {result.confidence}</p>
        </div>
      )}

      {error && <p className="error">{error}</p>}

      <p className="disclaimer">
        ⚠ This tool identifies encryption algorithms statistically.  
        It does NOT break encryption or recover keys.
      </p>
    </div>
  );
}

export default FileUpload;
