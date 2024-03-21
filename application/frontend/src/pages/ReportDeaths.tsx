import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import { loadGoogleMapsScript } from "../utils/loadGoogleMapsScript";
import GoogleMap from "../components/Googlemap";
import Footer from "../components/Footer";
import style from "../styles/ReportDeaths.module.css";

const ReportDeaths: React.FC = () => {
  const [countys, setCountys] = useState<{ details: any[] }>({ details: [] });
  const [users, setUsers] = useState<{ details: any[] }>({ details: [] });
  const [selectedCounty, setSelectedCounty] = useState("");
  const [selectedDept, setSelectedDept] = useState("");
  const [numberOfDeaths, setNumberOfDeaths] = useState<number | undefined>(undefined);
  const [causeOfDeaths, setCauseOfDeaths] = useState<string>("");
  const [dateOfDeaths, setDateOfDeaths] = useState<string | undefined>(undefined);

  useEffect(() => {
    loadGoogleMapsScript(
        process.env.REACT_APP_GOOGLE_MAPS_API_KEY!,
        "initGoogleMap"
    );

    axios
      .get("http://localhost:8000")
      .then((res) => {
        setCountys({
          details: res.data,
        });
      })
      .catch((err) => {
        console.error(err);
      });

    axios
      .get("http://localhost:8000/api/users")
      .then((res) => {
        setUsers({
          details: res.data,
        });
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  const handleReportButtonClick = () => {
    console.log("Reporting deaths:", {
      numberOfDeaths,
      causeOfDeaths,
      dateOfDeaths,
    });
  };

  return (
    <div>
      <Navbar />
      <div className={style.ReportContainer}>
        <div className={style.leftHalf}>
          <h1>Report Deaths</h1>

          <div className={style.ReportList}>
              <div className={style.ReportItem}>
                <span className={style.deptSpan}>1. Number of deaths</span>
                <input
                  className={style.deptInput}
                  type="number"
                  value={numberOfDeaths !== undefined ? numberOfDeaths : ""}
                  onChange={(e) => setNumberOfDeaths(Number(e.target.value))}
                />
              </div>
              <div className={style.ReportItem}>
                <span className={style.deptSpan}>2. Cause of deaths</span>
                <input
                  className={style.deptInput}
                  type="text"
                  value={causeOfDeaths}
                  onChange={(e) => setCauseOfDeaths(e.target.value)}
                />
              </div>
              <div className={style.ReportItem}>
                <span className={style.deptSpan}>3. Date of deaths</span>
                <input
                  className={style.deptInput}
                  type="date"
                  value={dateOfDeaths !== undefined ? dateOfDeaths : ""}
                  onChange={(e) => setDateOfDeaths(e.target.value)}
                />
              </div>
          </div>
          <button className={style.reportButton} onClick={handleReportButtonClick}>
            Report
          </button>
        </div>

        <div className={style.rightHalf}>
          <GoogleMap />
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ReportDeaths;