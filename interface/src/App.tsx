import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Start } from "./pages/Start";
import { Question } from "./pages/Question";
import { Result } from "./pages/Result";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Start />} />
        <Route path="/question" element={<Question />} />
        <Route path="/result" element={<Result />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
