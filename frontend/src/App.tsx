import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import FullForm from "./components/FullForm";
import OutputResponse from "./components/output-ui/OutputResponse";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/chatbot/" element={<FullForm />} />
        <Route path="/chatbot/output-response" element={<OutputResponse />} />
      </Routes>
    </Router>
  );
}

export default App;
