import { useState } from "react";
import "./App.css";
import { FileUploadForm } from "./components/FileUploadForm";
import { FileList } from "./components/FileList";

function App() {
  const [reloadToken, setReloadToken] = useState(0);

  return (
    <div style={{ maxWidth: "800px", margin: "2rem auto", color: "#fff" }}>
      <h1>Smart File Storage</h1>
      <p>Upload files and view stored metadata from your cloud backend.</p>

      <FileUploadForm onUploaded={() => setReloadToken((t) => t + 1)} />

      <hr style={{ margin: "2rem 0" }} />

      <FileList reloadToken={reloadToken} />
    </div>
  );
}

export default App;