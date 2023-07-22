import React from 'react';
import './GameDalgona.css';
import GameTimer from './GameTimer';

const GameDalgona = () => {
    return( 
    <div>
        <div className='DalgonaHeader'>
            <h1>SQUID-CANVAS 달고나 게임</h1>
        </div>
        <div className='DalgonaNav'>
            <div className='DalgonaNavTimer'>
                <GameTimer/>
            </div>
            <div className='DalgonaNavStartCount'>시작인원 수</div>
            <div className='DalgonaNavSurviveCount'>생존인원 수</div>
        </div>
        <div className="DalgonaFrame">
            <div className='DalgonaBox'>
                <h2>달고나 이미지화면</h2>
            </div>
            <div className='WebcamBox'>
                <img src='http://localhost:5000/video_feed' alt="video_feed" />
            </div>
        </div>
    </div>)
}

export default GameDalgona;
