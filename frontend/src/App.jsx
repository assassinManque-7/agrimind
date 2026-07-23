import { useState, useEffect } from "react"

function App(){

  const [city, setCity] = useState("");
  const [crop, setCrop] = useState("");

  const [res, setRes] = useState("");

  const inpd = {city, crop};

  const sendinp = async (inp) =>{
    const resp = await fetch(
      "http://127.0.0.1:8000/recom",
      {
        method : "POST",
        headers : {"Content-Type" : "application/json"},
        body : JSON.stringify(inp),

      }
    )

    console.log(resp.status)

    const data = await resp.json();

    console.log(data)

    setRes(JSON.stringify(data, null, 4));

  }

  return (

    <>
      <input
        value = {city}
        onChange = {(e) => setCity(e.target.value)}
        placeholder = "enter city"
      />

      <input
        value = {crop}
        onChange = {(e) => setCrop(e.target.value)}
        placeholder = "enter crop"
      />

      <button onClick = {() => sendinp(inpd)}>
        recommend
      </button>

      <textarea 
        value = {res}
      />

    </>
  )
}

export default App;

