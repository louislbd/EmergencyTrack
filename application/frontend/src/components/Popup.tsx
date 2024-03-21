import React, { useEffect, useState } from "react";
import axios from "axios";
import styles from "../styles/Popup.module.css";

interface PopupProps {
  department: string;
  county_name: string;
  dataset_id: string;
  onClose: () => void;
}
const departmentApiMap = {
  weather: "weather_events",
  wildfires: "wildfires",
  security: "security_concerns",
  blocked_roads: "blocked_roads",
};
const parseLevelOfEvacuation = (level: string): number | string => {
  try {
    const hexValue = level.match(/\\x([0-9A-Fa-f]+)/)?.[1];
    if (hexValue) {
      return parseInt(hexValue, 16); // Convert hex to decimal
    }
    return level; // Return original value if no match is found
  } catch (e) {
    console.error("Error parsing level_of_evacuation:", e);
    return level; // Return original value in case of error
  }
};

const popupContainerStyle: React.CSSProperties = {
  position: "relative",
  border: "2px solid black",
  padding: "10px",
  borderRadius: "5px",
  backgroundColor: "white",
};

const closeButtonStyle: React.CSSProperties = {
  position: "absolute",
  right: "10px",
  top: "10px",
  padding: "5px 10px",
  fontSize: "0.8rem",
};

const paragraphStyle = {
  margin: "1px 0",
  fontSize: "1rem",
};

const Popup: React.FC<PopupProps> = ({
  department,
  county_name,
  dataset_id,
  onClose,
}) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    setLoading(true);
    const apiEndpoint =
      departmentApiMap[department as keyof typeof departmentApiMap] ||
      department;

    axios
      .get(`http://44.228.29.165:8000/api/${apiEndpoint}/${dataset_id}`)
      .then((response) => {
        setData(response.data);
        setLoading(false);
        console.log(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setError("Failed to fetch data.");
        setLoading(false);
      });
  }, [department, dataset_id]);

  const renderData = () => {
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    if (!data) return <p>No data available for this department.</p>;

    switch (department) {
      case "blocked_roads":
        return (
          <div>
            <p>Road Name: {data.road_name}</p>
            <p>Reason: {data.reason}</p>
            <p>Intersection 1: {data.intersection1}</p>
            <p>Intersection 2: {data.intersection2}</p>
            <p>Start Time: {data.starting_datetime}</p>
            <p>End Time: {data.ending_datetime}</p>
            <p>Information: {data.informations_for_public}</p>
          </div>
        );
      case "security":
        return (
          <div>
            <p>Location Name: {data.location_name}</p>
            <p>Cause of Concern: {data.cause_of_concern}</p>
            <p>Reported Time: {data.reported_datetime}</p>
            <p>Instructions: {data.instructions_for_public}</p>
          </div>
        );
      case "weather":
        return (
          <div>
            <p>Location Name: {data.location_name}</p>
            <p>Event Type: {data.event_type}</p>
            <p>Estimated Date/Time: {data.estimated_datetime}</p>
            <p>Event Radius: {data.event_radius} km</p>
            <p>
              Level of Evacuation: level
              {parseLevelOfEvacuation(data.level_of_evacuation)}
            </p>
            <p>Instructions: {data.instructions_for_public}</p>
            <p>
              Event Status: {data.event_is_active ? "Active" : "Not Active"}
            </p>
          </div>
        );

      case "wildfires":
        return (
          <div>
            <p>Location Name: {data.location_name}</p>
            <p>Cause of Fire: {data.cause_of_fire}</p>
            <p>Reported Time: {data.date_of_fire}</p>
            <p>Instructions: {data.instructions_for_public}</p>
            <p>
              Level of Evacuation: level{" "}
              {parseLevelOfEvacuation(data.level_of_evacuation)}
            </p>
            <p>Fire Status: {data.fire_is_active ? "Active" : "Not Active"}</p>
          </div>
        );

      default:
        return <p>No data available for this department.</p>;
    }
  };

  return (
    <div style={popupContainerStyle}>
      <button style={closeButtonStyle} onClick={onClose}>
        Close
      </button>
      <h3>{department}</h3>
      <h4>County: {county_name}</h4>
      {renderData()}
    </div>
  );
};

export default Popup;
