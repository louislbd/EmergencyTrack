import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import { loadGoogleMapsScript } from "../utils/loadGoogleMapsScript";
import GoogleMap from "../components/Googlemap";
import Footer from "../components/Footer";
import style from "../styles/ReportCovid.module.css";

const ReportCovid: React.FC = () => {
  const [countys, setCountys] = useState<{ details: any[] }>({ details: [] });
  const [users, setUsers] = useState<{ details: any[] }>({ details: [] });
  const [selectedCounty, setSelectedCounty] = useState("");
  const [selectedDept, setSelectedDept] = useState("");
  const [numberOfCovid, setNumberOfCovid] = useState<number | undefined>(undefined);
  const [dateOfCovid, setDateOfCovid] = useState<string | undefined>(undefined);

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
    console.log("Reporting covid19 cases:", {
      numberOfCovid,
      dateOfCovid,
    });
  };

  return (
    <div>
      <Navbar />
      <div className={style.ReportContainer}>
        <div className={style.leftHalf}>
          <h1>Report Covid</h1>

          <div className={style.ReportList}>
              <div className={style.ReportItem}>
                <span className={style.deptSpan}>1. Number of Covid19 Cases</span>
                <input
                  className={style.deptInput}
                  type="number"
                  value={numberOfCovid}
                  onChange={(e) => setNumberOfCovid(Number(e.target.value))}
                />
              </div>
              <div className={style.ReportItem}>
                <span className={style.deptSpan}>2. Cause of Covid19 Cases</span>
                <input
                  className={style.deptInput}
                  type="date"
                  value={dateOfCovid}
                  onChange={(e) => setDateOfCovid(e.target.value)}
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

export default ReportCovid;