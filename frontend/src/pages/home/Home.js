// Account creation / Sign in by wallet connect
import React, {useState, useContext, useEffect, Suspense} from 'react';
import { useNavigate } from 'react-router-dom';
import "./Home.css";
import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';
import { Button } from 'react-bootstrap';


const Home = () => {
  
  let navigate = useNavigate();
  const [pubKey, setPubKey] = useState();
  const [login, setLogin] = useState(false);
  const [testRes, setTestRes] = useState();

  // connect with public key /or mneumonics
  // const loginCheck = async () => {
  //   // const res = await connect
  //   return 1;
  // };

  const createAccount = async (name) => {
    await axios.post('http://localhost:8888/generateAcnt', {'params': {'name': name}})
    .then( res => {
      setTestRes(JSON.stringify(res.data));
      console.log(JSON.stringify(res.data));
    })
    .catch( (err) => {
      console.error(err);
    })
  };

  const test = async () => {
    await axios.get('http://localhost:8888')
    .then( res => {
      setTestRes(res.data.data);
    })
    .catch( (err) => {
      console.error(err);
    })
  };

  useEffect( () => {
    test();
  }, []);

  return (
    <div id='home' className='content content-center'>
      
      <div id="login">
        <button variant="primary" onClick={ () => {navigate('/modelupload');}}>Model Upload</button>
        <button variant="primary" onClick={ async () => {navigate('/modelrun');}}>Model Run</button>
        <button variant="primary" onClick={ async () => { await createAccount('Test')}}>Test Generate Account</button>
      </div>

      {
        test ? 
        <>
          <h3>Test Response</h3>
          <div>{testRes}</div>
        </>
        :
        <>
        <div>No results found</div>
        </>
      }
    </div>
    
  )
  //
}

export default Home;