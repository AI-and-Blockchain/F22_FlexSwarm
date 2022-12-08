// Account creation / Sign in by wallet connect
import React, {useState, useContext, useEffect, Suspense} from 'react';
import { useNavigate } from 'react-router-dom';
import "./Home.css";
import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';
import { Button } from 'react-bootstrap';
import { ClientContext } from '../../context/ClientContext';



const Home = () => {
  
  let navigate = useNavigate();
  const {pubKey, setPubKey} = useContext(ClientContext);
  const {priKey, setPriKey} = useContext(ClientContext);
  const {mneum, setMneum} = useContext(ClientContext);
  const {login, setLogin} = useContext(ClientContext);


  // connect with public key /or mneumonics
  // const loginCheck = async () => {
  //   // const res = await connect
  //   return 1;
  // };

  const createAccount = async (name) => {
    await axios.post('http://localhost:8888/generateAcnt', {'params': {'name': name}})
    .then( res => {
      let retData = res.data;
      console.log(retData.address, retData.private_key, retData.passphrase);
      setPubKey(retData.address);
      setPriKey(retData.private_key);
      setMneum(retData.passphrase);
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
          <div id="redirect">
            <button variant="primary" onClick={ () => {navigate('/modelupload');}}>Model Upload</button>
            <button variant="primary" onClick={ async () => {navigate('/modelrun');}}>Model Run</button>
          </div>
          <div id="login">
            Public key: {pubKey}
            <br></br>
            Private key: {priKey}
            <br></br>
            Mneumonics: {mneum}
            <p>
              Login by mneumonics, will be replaced by wallet connect using AlgoSigner at some point.
            </p>
          </div>
        </>
        :
        <>
          <div id="account">
            <button variant="primary" onClick={ async () => {await createAccount('Test'); setLogin(true);} }>
              Test Generate Account
            </button>
          </div>
        </>
      }
    </div>
    
  )
  //
}

export default Home;