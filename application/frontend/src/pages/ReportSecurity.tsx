import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import { loadGoogleMapsScript } from "../utils/loadGoogleMapsScript";
import GoogleMap from "../components/Googlemap";
import Footer from "../components/Footer";
import style from "../styles/ReportSecurity.module.css";

const ReportSecurity: React.FC = () => {
  const [countys, setCountys] = useState<{ details: any[] }>({ details: [] });
  const [users, setUsers] = useState<{ details: any[] }>({ details: [] });
  const [selectedCounty, setSelectedCounty] = useState("");
  const [selectedDept, setSelectedDept] = useState("");
  const [nameOfSecurity, setNameOfSecurity] = useState<string>("");
  const [causeOfSecurity, setCauseOfSecurity] = useState<string>("");
  const [dateOfSecurity, setDateOfSecurity] = useState<string | undefined>(
    undefined
  );
  const [instructions, setInstructions] = useState<string>("");

  useEffect(() => {
    axios
      .get("http://44.228.29.165:8000/api/users")
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
    console.log("Reporting security concerns:", {
      nameOfSecurity,
      causeOfSecurity,
      dateOfSecurity,
      instructions,
    });
  };

  return (
    <div>
      <Navbar />
      <div className={style.ReportContainer}>
        <div className={style.leftHalf}>
          <h1>Report Security</h1>

          <div className={style.ReportList}>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>1. Location of the concern</span>
              <input
                className={style.deptInput}
                type="name"
                value={nameOfSecurity}
                onChange={(e) => setNameOfSecurity(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>2. Cause of the concern</span>
              <input
                className={style.deptInput}
                type="text"
                value={causeOfSecurity}
                onChange={(e) => setCauseOfSecurity(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>3. Begin date of the fire</span>
              <input
                className={style.deptInput}
                type="date"
                value={dateOfSecurity !== undefined ? dateOfSecurity : ""}
                onChange={(e) => setDateOfSecurity(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>
                4. Instructions to the public
              </span>
              <input
                className={style.deptInput}
                type="text"
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
              />
            </div>
          </div>
          <button
            className={style.reportButton}
            onClick={handleReportButtonClick}
          >
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

export default ReportSecurity;
