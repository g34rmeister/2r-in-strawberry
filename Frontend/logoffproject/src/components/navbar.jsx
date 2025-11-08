import { useState} from "react";
import {PlusCircleFill, BookmarkFill, BarChartFill, PersonFill} from 'react-bootstrap-icons'; 

const Navbar = () => {
    const [isOpen, setIsopen] = useState(false);

    return(
        <div className="navbar">
            <div className="nav-container">
                <a className="nav-icon" href="#">
                    <PlusCircleFill style={{color: 'white'}}/>
                </a>
            </div>
            <div className="nav-container">
                <a className="nav-icon" href="#">
                    <BookmarkFill style={{color: 'white'}}/>
                </a>
            </div>
            <div className="nav-container">
                <a className="nav-icon" href="#">
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