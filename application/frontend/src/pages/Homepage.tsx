import { useState, useEffect } from "react";
import style from "../styles/Homepage.module.css";
import PaginationTable from "../components/PlaginationTable";
import axios from "axios";
import { loadGoogleMapsScript } from "../utils/loadGoogleMapsScript"; // Assume you've created this utility
import GoogleMap from "../components/Googlemap";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";

const Homepage: React.FC = () => {
  const [stateStatistics, setStateStatistics] = useState<{ details: any[] }>({
    details: [],
  });

  useEffect(() => {
    loadGoogleMapsScript(
      process.env.REACT_APP_GOOGLE_MAPS_API_KEY!,
      "initGoogleMap"
    );

    // Get the State statistics
    axios
      .get("http://44.228.29.165:8000/api/state_statistics/6")
      .then((res) => {
        setStateStatistics({
          details: res.data,
        });
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return (
    <div>
      <Navbar/>
      <div className={style.homepageContainer}>
        <div className={style.leftHalf}>
          <h1>California Metrics</h1>

          <table className={style.board}>
            <tbody>
              <tr>
                <td>Covid-19 Cases last 7 days per 100k</td>
                <td>Deaths last 7 days per 100k</td>
                <td>Wildfires</td>
                <td>Blocked Roads</td>
                <td>Security concerns</td>
                <td>Weather events</td>
              </tr>
              {stateStatistics.details.map((stateStats, id) => (
                <tr key={id}>
                  <td>{stateStats.covid_cases_7_days_per_100k}</td>
                  <td>{stateStats.deaths_7_days_per_100k}</td>
                  <td>{stateStats.wildfires}</td>
                  <td>{stateStats.blocked_roads}</td>
                  <td>{stateStats.security_concerns}</td>
                  <td>{stateStats.weather_events}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <PaginationTable />
        </div>

        <div className={style.rightHalf}>
          <GoogleMap />
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default Homepage;
