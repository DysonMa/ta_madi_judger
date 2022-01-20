import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react"
import axios from "axios"

function App() {

  const [message, setMessage] = useState({})

  useEffect(()=>{
    axios.get("http://localhost:5000/run").then(res => {
      console.log(res)
      setMessage(res)
    }).catch(err => console.log(err))
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          {message?.status ?? "none"}
        </a>
      </header>
    </div>
  );
}

export default App;
