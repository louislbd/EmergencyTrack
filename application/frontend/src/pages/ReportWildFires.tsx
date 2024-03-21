import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import { loadGoogleMapsScript } from "../utils/loadGoogleMapsScript";
import GoogleMap from "../components/Googlemap";
import Footer from "../components/Footer";
import style from "../styles/ReportWildFires.module.css";

const ReportWildFires: React.FC = () => {
  const [countys, setCountys] = useState<{ details: any[] }>({ details: [] });
  const [users, setUsers] = useState<{ details: any[] }>({ details: [] });
  const [selectedCounty, setSelectedCounty] = useState("");
  const [selectedDept, setSelectedDept] = useState("");
  const [nameOfWildFires, setNameOfWildFires] = useState<string>("");
  const [causeOfWildFires, setCauseOfWildFires] = useState<string>("");
  const [beginDateOfWildFires, setBeginDateOfWildFires] = useState<
    string | undefined
  >(undefined);
  const [instructions, setInstructions] = useState<string>("");
  const [evacuationLevel, setEvacuationLevel] = useState<string>("");

  useEffect(() => {
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
    console.log("Reporting wild fires:", {
      nameOfWildFires,
      causeOfWildFires,
      beginDateOfWildFires,
      instructions,
      evacuationLevel,
    });
  };

  const handleEvacuationLevel = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setEvacuationLevel(e.target.value);
  };

  const EvacuationLevels = ["L1", "L2", "L3"];

  return (
    <div>
      <Navbar />
      <div className={style.ReportContainer}>
        <div className={style.leftHalf}>
          <h1>Report WildFires</h1>

          <div className={style.ReportList}>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>1. Location of the fire</span>
              <input
                className={style.deptInput}
                type="name"
                value={nameOfWildFires}
                onChange={(e) => setNameOfWildFires(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>2. Cause of the fire</span>
              <input
                className={style.deptInput}
                type="text"
                value={causeOfWildFires}
                onChange={(e) => setCauseOfWildFires(e.target.value)}
              />
            </div>
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>3. Begin date of the fire</span>
              <input
                className={style.deptInput}
                type="date"
                value={
                  beginDateOfWildFires !== undefined ? beginDateOfWildFires : ""
                }
                onChange={(e) => setBeginDateOfWildFires(e.target.value)}
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
            <div className={style.ReportItem}>
              <span className={style.deptSpan}>5. Evacuation level</span>
              <div className={style.scrollingButton}>
                <select
                  value={evacuationLevel}
                  onChange={handleEvacuationLevel}
                >
                  {EvacuationLevels.map((output, id) => (
                    <option key={id} value={output}>
                      {output}
                    </option>
                  ))}
                </select>
              </div>
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

export default ReportWildFires;
