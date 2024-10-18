import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import { BrowserRouter, Route, Routes, useLocation } from 'react-router-dom';
import Chatbot from './components/Chatbot.jsx';

function Main() {
  const location = useLocation();
  
  return (
    <>
      {/* avoiding chatbot in the "/" */}
      {location.pathname !== '/' && <Chatbot className="chatbot-container" />}
      {(location.pathname !== '/' && location.pathname !== '/signup') && <Navbar />}
      <Routes>
        <Route path="/" element={<App />} />
      </Routes>
    </>
  );
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Main /> 
    </BrowserRouter>
  </StrictMode>
);
