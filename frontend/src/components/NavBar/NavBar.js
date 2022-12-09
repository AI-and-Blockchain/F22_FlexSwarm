import React, {useState, useContext, useEffect, Suspense} from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import './NavBar.css'
import axios from 'axios';
import { ClientContext } from '../../context/ClientContext';
import logo from './logo.svg';


const NavBar = () => {

  // let navigate = useNavigate();

  const {pubKey, setPubKey} = useContext(ClientContext);
  const {priKey, setPriKey} = useContext(ClientContext);
  const {mneum, setMneum} = useContext(ClientContext);
  const {login, setLogin} = useContext(ClientContext);

  const disconnect = () => {
    setPubKey(null);
    setLogin(false);
    setPriKey(null);
    setMneum(null);
  }


  return (
    <nav id="navbar" className="navbar navbar-light bg-light justify-content-between">
      <img className="logo" src={logo} alt="logo"></img>
      {!login ? 
      <>
        
      </>
      :
      <>
        <div className="nav-item">{pubKey}</div>
        <button className="btn btn-outline-danger my-2 my-sm-0" type="submit" 
          onClick={() => {disconnect();}}>
          Disconnect
        </button>
      </>
      }
    </nav>
  )
  
}


export default NavBar;
