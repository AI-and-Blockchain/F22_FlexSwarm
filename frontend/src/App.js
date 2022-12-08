import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { ClientContext } from './context/ClientContext';
import Home from './pages/home/Home';
import ModelRun from './pages/model-run/ModelRun';
import ModelUpload from './pages/model-upload/ModelUpload';

function App() {

  const [user, setUser] = useState()

  return (
    <ClientContext.Provider value={{
      user, setUser
    }}>


    <div className="App">
      Swarm Learning with Flexible Labels Simulation
      <hr></hr>
      <Router>
        <Routes>
          <Route path='/home' element={<Home/>} />
          <Route path='/modelupload' element={<ModelUpload/>} />
          <Route path='/modelrun' element={<ModelRun/>} />
        </Routes>
      </Router>
    </div>
    </ClientContext.Provider>
  );
}

export default App;
