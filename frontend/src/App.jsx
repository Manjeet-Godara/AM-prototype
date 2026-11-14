import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import SystemsPage from "./pages/SystemsPage";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/systems" />} />
                <Route path="/systems" element={<SystemsPage />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;