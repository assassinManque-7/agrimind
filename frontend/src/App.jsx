import { useState } from "react";

function App(){
  const [city, setCity] = useState("");
  const [crop, setCrop] = useState("");

  return (
    <>

      <h1>Agrimind</h1>
      <input placeholder = "city" value = {city} onChange = {(event) => setCity(event.target.value)}/>
      <input placeholder = "crop" value = {crop} onChange = {(event) => setCrop(event.target.value)}/>
      <button onClick = {() => setCity("")}>get recommendation</button>
    
    </>
  );
}

export default App;