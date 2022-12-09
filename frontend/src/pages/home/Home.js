// Account creation / Sign in by wallet connect
import React, {useState, useContext, useEffect, Suspense} from 'react';
import { useNavigate } from 'react-router-dom';
import "./Home.css";
import NavBar from '../../components/NavBar/NavBar';
import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';
import { ClientContext } from '../../context/ClientContext';



const Home = () => {
  
  let navigate = useNavigate();
  const {pubKey, setPubKey} = useContext(ClientContext);
  const {priKey, setPriKey} = useContext(ClientContext);
  const {mneum, setMneum} = useContext(ClientContext);
  const {login, setLogin} = useContext(ClientContext);
  const { website } = useContext(ClientContext);

  const createAccount = async (name) => {
    await axios.post(`${website}/generateAcnt`, {'params': {'name': name}})
    .then( res => {
      let retData = res.data;
      console.log(retData.address, retData.private_key, retData.passphrase);
      setPubKey(retData.address);
      setPriKey(retData.private_key);
      setMneum(retData.passphrase);
      setLogin(true);
    })
    .catch( (err) => {
      console.error(err);
    })
  };

  useEffect( () => {
    // test();
  }, []);

  return (
    <div id='home' className='content content-center'>
      {
        login ? 
        // if logged in (i.e. public key bound), present two options to proceed
        <>
          <div id="login">
            Public key: {pubKey}
            <br></br>
            {/* Private key: {priKey}
            <br></br> */}
            Mneumonics: {mneum}
            <p>
              Login by mneumonics, will be replaced by wallet connect using AlgoSigner at some point.
            </p>
          </div>
          <div id="redirect">
            <button id="tmp" type="button" className="btn btn-secondary btn-inline" 
              onClick={ () => {navigate('/modelupload');}
            }>Upload Model</button>
            <button type="button" className="btn btn-secondary btn-inline" 
              onClick={ () => {navigate('/modelrun');}
            }>Run Model</button>
          </div>
        </>
        :
        <>
          <div id="account" className="justify-content-between">

            {/* <small>Or</small> */}
            <form id="connectAlgoAcnt" className="form-inline">
              <input className="form-control mr-sm-2" placeholder="Algorand Mneumonics"/>
              <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Connect</button>
            </form>

            <div id="sep"><span>Or</span></div>

            <button type="button" className="btn btn-outline-warning my-2 my-sm-0" 
              onClick={ async () => {await createAccount('Test');} }>
              Generate Algorand Account
            </button>
          </div>
        </>
      }
    </div>
    
  )
  //
}

export default Home;