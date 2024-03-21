import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import { loadGoogleMapsScript } from "../utils/loadGoogleMapsScript";
import GoogleMap from "../components/Googlemap";
import Footer from "../components/Footer";
import style from "../styles/ReportBlockedRoads.module.css";

const ReportBlockedRoads: React.FC = () => {
  const [countys, setCountys] = useState<{ details: any[] }>({ details: [] });
  const [users, setUsers] = useState<{ details: any[] }>({ details: [] });
  const [selectedCounty, setSelectedCounty] = useState("");
  const [selectedDept, setSelectedDept] = useState("");
  const [nameOfBlockedRoads, setNameOfBlockedRoads] = useState<string>("");
  const [causeOfBlockedRoads, setCauseOfBlockedRoads] = useState<string>("");
  const [startingPoint, setStartingPoint] = useState<string>("");
  const [endingPoint, setEndingPoint] = useState<string>("");
  const [beginDateOfBlockedRoads, setBeginDateOfBlockedRoads] = useState<
    string | undefined
  >(undefined);
  const [endDateOfBlockedRoads, setEndDateOfBlockedRoads] = useState<
    string | undefined
  >(undefined);

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
    console.log("Reporting blocked roads:", {
      nameOfBlockedRoads,
      causeOfBlockedRoads,
      startingPoint,
      endingPoint,
      beginDateOfBlockedRoads,
      endDateOfBlockedRoads,
    });
  };

  return (
    <div>
      <Navbar />
      <div className={style.ReportContainer}>
        <div className={style.leftHalf}>
          <h1>Report BlockedRoads</h1>

          <div className={style.ReportList}>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>
                1. Name of the blocked road
              </span>
              <input
                className={style.deptInput}
                type="name"
                value={nameOfBlockedRoads}
                onChange={(e) => setNameOfBlockedRoads(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>2. Cause of blocked roads</span>
              <input
                className={style.deptInput}
                type="text"
                value={causeOfBlockedRoads}
                onChange={(e) => setCauseOfBlockedRoads(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>3. Starting Intersection</span>
              <input
                className={style.deptInput}
                type="name"
                value={startingPoint}
                onChange={(e) => setStartingPoint(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>4. Ending Intersection</span>
              <input
                className={style.deptInput}
                type="name"
                value={endingPoint}
                onChange={(e) => setEndingPoint(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>5. Blockage beginning date</span>
              <input
                className={style.deptInput}
                type="date"
                value={
                  beginDateOfBlockedRoads !== undefined
                    ? beginDateOfBlockedRoads
                    : ""
                }
                onChange={(e) => setBeginDateOfBlockedRoads(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>6. Blockage ending date</span>
              <input
                className={style.deptInput}
                type="date"
                value={
                  endDateOfBlockedRoads !== undefined
                    ? endDateOfBlockedRoads
                    : ""
                }
                onChange={(e) => setEndDateOfBlockedRoads(e.target.value)}
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

export default ReportBlockedRoads;
