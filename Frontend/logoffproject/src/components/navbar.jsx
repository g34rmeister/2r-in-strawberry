import { useState} from "react";
import {PlusCircleFill, BookmarkFill, BarChartFill, PersonFill} from 'react-bootstrap-icons'; 
import { useNavigate } from "react-router-dom";

const Navbar = () => {
    const [isOpen, setIsopen] = useState(false);
    const navigate = useNavigate();

    return(
        <div className="navbar">
            <div className="nav-container">
                <a className="nav-icon" onClick={() => navigate('/start-challenge')}>
                    <PlusCircleFill style={{color: 'white'}}/>
                </a>
            </div>
            <div className="nav-container">
                <a className="nav-icon" onClick={() => navigate('/history')}>
                    <BookmarkFill style={{color: 'white'}}/>
                </a>
            </div>
            <div className="nav-container">
                <a className="nav-icon" onClick={() => navigate('/leaderboardCardExample')}>
                    <BarChartFill style={{color: 'white'}}/>
                </a>
            </div>
            <div className="nav-container">
                <a className="nav-icon" href="#">
                    <PersonFill style={{color: 'white'}}/>
                </a>
            </div>
        </div>
    );
}

export default Navbar;