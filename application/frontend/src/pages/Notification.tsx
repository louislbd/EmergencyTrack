import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import { loadGoogleMapsScript } from "../utils/loadGoogleMapsScript";
import GoogleMap from "../components/Googlemap";
import Footer from "../components/Footer";
import style from "../styles/Notification.module.css";
import BellOn from "../assets/images/bell-on.png";
import BellOff from "../assets/images/bell-off.png";
import CovidIcon from "../assets/images/bacteria.png";
import WeatherIcon from "../assets/images/marker-weather.png";
import WildfireIcon from "../assets/images/marker-wildfires.png";
import BlockedRoadIcon from "../assets/images/marker-blockedRoad.png";
import SecurityIcon from "../assets/images/marker-security.png";

const NotificationPage: React.FC = () => {
  const [countys, setCountys] = useState<{ details: any[] }>({ details: [] });
  const [selectedCounty, setSelectedCounty] = useState("");
  const [selectedDept, setSelectedDept] = useState("");

  useEffect(() => {
    axios
      .get("http://44.228.29.165:8000/api/countys")
      .then((res) => {
        setCountys({
          details: res.data,
        });
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  const handleCountyChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedCounty(event.target.value);
  };

  const handleDeptChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedDept(event.target.value);
  };
  const subscribeToNotifications = (department: String) => {
    axios
      .post("http://44.228.29.165:8000/api/subscription", {
        county: selectedCounty,
        department: department,
      })
      .then((response) => {
        // Handle success
        console.log("Subscribed successfully", response);
      })
      .catch((error) => {
        // Handle error
        console.error("Error subscribing", error);
      });
  };

  const unsubscribeFromNotifications = (department: String) => {
    axios
      .delete("http://44.228.29.165:8000/api/subscription", {
        data: {
          county: selectedCounty,
          department: department,
        },
      })
      .then((response) => {
        // Handle success
        console.log("Unsubscribed successfully", response);
      })
      .catch((error) => {
        // Handle error
        console.error("Error unsubscribing", error);
      });
  };

  return (
    <div>
      <Navbar />
      <div className={style.NotificationContainer}>
        <div className={style.leftHalf}>
          <h1>My Notifications</h1>
          <div className="county-selection">
            <h1>County</h1>
            <div className={style.scrollingButton}>
              <select value={selectedCounty} onChange={handleCountyChange}>
                {countys.details.map((output, id) => (
                  <option key={id} value={output.county_id}>
                    {output.county_name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className={style.notificationList}>
            <div className={style.notificationItem}>
              <img
                src={WeatherIcon}
                alt="Weather Icon"
                className={style.deptIcon}
              />
              <span className={style.deptSpan}>New Weather Events</span>
              <button
                className={style.emailButton}
                onClick={() => subscribeToNotifications("weather")}
              >
                Email
              </button>
              <img src={BellOn} alt="Bell Icon" className={style.bellIcon} />
              <img
                src={BellOff}
                alt="BellOff Icon"
                className={style.bellIcon}
                onClick={() => unsubscribeFromNotifications("weather")}
              />
            </div>
            <div className={style.notificationItem}>
              <img
                src={WildfireIcon}
                alt="Wildfire Icon"
                className={style.deptIcon}
              />
              <span className={style.deptSpan}>New Wildfire Events</span>
              <button
                className={style.emailButton}
                onClick={() => subscribeToNotifications("wildfire")}
              >
                Email
              </button>
              <img src={BellOn} alt="Bell Icon" className={style.bellIcon} />
              <img
                src={BellOff}
                alt="BellOff Icon"
                className={style.bellIcon}
                onClick={() => unsubscribeFromNotifications("wildfire")}
              />
            </div>
            <div className={style.notificationItem}>
              <img
                src={SecurityIcon}
                alt="Security Icon"
                className={style.deptIcon}
              />
              <span className={style.deptSpan}>New Security Concerns</span>
              <button
                className={style.emailButton}
                onClick={() => subscribeToNotifications("security")}
              >
                Email
              </button>
              <img src={BellOn} alt="Bell Icon" className={style.bellIcon} />
              <img
                src={BellOff}
                alt="BellOff Icon"
                className={style.bellIcon}
                onClick={() => unsubscribeFromNotifications("security")}
              />
            </div>
          </div>
        </div>

        <div className={style.rightHalf}>
          <GoogleMap />
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default NotificationPage;
