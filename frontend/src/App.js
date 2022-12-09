import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { ClientContext } from './context/ClientContext';
import Home from './pages/home/Home';
import ModelRun from './pages/model-run/ModelRun';
import ModelUpload from './pages/model-upload/ModelUpload';
import NavBar from './components/NavBar/NavBar';

function App() {

  const [website] = useState('http://localhost:8888')
  const [user, setUser] = useState()
  const [login, setLogin] = useState(false);
  const [pubKey, setPubKey] = useState();
  const [priKey, setPriKey] = useState();
  const [mneum, setMneum] = useState();

  return (
    <ClientContext.Provider value={{
      user, setUser,
      login, setLogin,
      pubKey, setPubKey,
      priKey, setPriKey,
      mneum, setMneum,
      website
    }}>


    <div className="App">
      
      <NavBar/>
      <div className="content">
        <h5>Swarm Learning with Flexible Labels Simulation</h5>
        <hr></hr>
        <Router>
          <Routes>
            <Route path='/' element={<Home/>} />
            <Route path='/modelupload' element={<ModelUpload/>} />
            <Route path='/modelrun' element={<ModelRun/>} />
          </Routes>
        </Router>
      </div>
    </div>
    </ClientContext.Provider>
  );
}

export default App;
