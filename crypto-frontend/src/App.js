import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import FileUpload from "./components/FileUpload";
import HowItWorks from "./components/HowItWorks";
import "./App.css";

function App() {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    document.body.dataset.theme = theme;
  }, [theme]);

  const handleToggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <FileUpload
                theme={theme}
                onToggleTheme={handleToggleTheme}
              />
            }
          />
          <Route
            path="/how-it-works"
            element={
              <HowItWorks
                theme={theme}
                onToggleTheme={handleToggleTheme}
              />
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
