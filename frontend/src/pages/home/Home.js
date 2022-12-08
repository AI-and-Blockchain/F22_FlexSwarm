// Account creation / Sign in by wallet connect
import React, {useState, useContext, Suspense} from 'react';
import { useNavigate } from 'react-router-dom';
import "./Home.css";
import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';


const Home = () => {
  
  let navigate = useNavigate();
  const [PubKey, setPubKey] = useState(false);

  // connect with public key /or mneumonics
  const loginCheck = async () => {
    // const res = await connect
    return 1;
  }

  const createAccount = async () => {
    // const data = await axios.get('/account');
    return 1;
  }

  const test = async () => {
    // await axios.get()
    return 1;
  }

  //
}