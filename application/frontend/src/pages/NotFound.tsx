import React from "react";
import Sad from '../assets/images/pepe-crying.gif'
import { useNavigate } from "react-router-dom";
import style from "../styles/NotFound.module.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const NotFound: React.FC = () => {
    const navigate = useNavigate()

    const teleport = () => {
        navigate('/')
    }

    return (
        <div>
            <Navbar/>
            <div className={style.notFoundContainer}>
                <h2 className={style.h2}>404 NotFound</h2>
                <img className={style.img} alt="Sad Pepega" src={Sad}/>
                <p className={style.p}>The page you're looking for doesn't exist. Return to the right path.</p>
                <button className={style.button} onClick={teleport}>Teleport Me !</button>
            </div>
            <Footer />
        </div>
    );
}

export default NotFound