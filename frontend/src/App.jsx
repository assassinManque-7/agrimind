import { useState, useEffect } from "react";

function App(){
  const [city, setCity] = useState("");
  const [crop, setCrop] = useState("");

  const [res, setRes] = useState(null);
  const [load, setLoad] = useState(true);
  const [err, setErr] = useState(null);
  
  const inpd = {city, crop};

  const sendinp = async (inputData) => {
    const resp = await fetch(
      "http://localhost:8000/recom",
      {
        method : "POST",

        headers : {
          "Content-Type" : "application/json"
        },

        body : JSON.stringify(inputData),
      }
    );

    const data = await resp.json();

    setRes(JSON.stringify(data, null, 2));
  }

  return (
    <>

      <h1>Agrimind</h1>
      <input placeholder = "city" value = {city} onChange = {(event) => setCity(event.target.value)}/>
      <input placeholder = "crop" value = {crop} onChange = {(event) => setCrop(event.target.value)}/>
      <button onClick = {() => sendinp(inpd)}>get recommendation</button>
      <textarea value = {res ?? ""} readOnly/>
    
    </>
  );
}

export default App;