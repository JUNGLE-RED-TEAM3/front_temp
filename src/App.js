import './App.css';
import GameDalgona from './GameDalgona';
import GameHibiscus from './GameHibiscus';
import React,{useEffect, useState} from 'react';


function App() {

    useEffect(() => {
      fetch("/").then(
        // response 객체의 json() 이용하여 json 데이터를 객체로 변화
        res => res.json()
      )
    },[])

  return (
   
    <div className="App">
      <GameDalgona />
      {/* <GameHibiscus/> */}
    </div>

 
  );
}

export default App;
