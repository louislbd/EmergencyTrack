import React, { useRef, useState, useEffect } from "react";
import axios from "axios";
import { loadGoogleMapsScript } from "../utils/loadGoogleMapsScript";
import style from "../styles/Homepage.module.css";
import wildFiresMarkers from "../assets/images/marker-wildfires.png";
import securityMarkers from "../assets/images/marker-security.png";
import weatherMarkers from "../assets/images/marker-weather.png";
import blockedRoadMarkers from "../assets/images/marker-blockedRoad.png";
import SearchResultTable from "./SearchResultTable";
import Popup from "./Popup";
import { useLocation } from "react-router-dom";

const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;

declare global {
  interface Window {
    initGoogleMap?: () => void;
  }
}
interface Location {
  location_y_coordinate: number;
  location_x_coordinate: number;
  department: string;
  county_name: string;
  dataset_id: string;
  [key: string]: any;
}
// Define the type for the departmentMarkers object
type DepartmentMarkerMap = {
  [key: string]: string; // This allows indexing with a string to get a string result
};

const departmentMarkers: DepartmentMarkerMap = {
  blocked_roads: blockedRoadMarkers,
  security: securityMarkers,
  weather: weatherMarkers,
  wildfires: wildFiresMarkers,
};

const GoogleMap: React.FC = () => {
  const googleMapRef = useRef<HTMLDivElement>(null);
  const [googleMap, setGoogleMap] = useState<google.maps.Map>();
  const [selectedCounty, setSelectedCounty] = useState("");
  const [selectedDept, setSelectedDept] = useState("all");
  const [markers, setMarkers] = useState<google.maps.Marker[]>([]);
  const [tableData, setTableData] = useState<Location[]>([]);
  const location = useLocation();

  //for Popup result
  const [showPopup, setShowPopup] = useState(false);
  const [popupData, setPopupData] = useState({
    department: "",
    county_name: "",
    dataset_id: "",
  });
  useEffect(() => {
    // Initialize Google Map
    window.initGoogleMap = () => {
      const map = new google.maps.Map(googleMapRef.current!, {
        center: { lat: 36.7783, lng: -119.4179 }, // Coordinates for California
        zoom: 7,
      });
      setGoogleMap(map);
    };

    // Load the Google Maps script only if it's not already loaded
    if (!window.google || !window.google.maps) {
      loadGoogleMapsScript(apiKey!, "initGoogleMap");
    } else {
      window.initGoogleMap();
    }

    // Cleanup function
    return () => {
      // Remove the global function
      delete window.initGoogleMap;
    };
  }, []);

  // Clears all markers from the map and state
  const clearMarkers = () => {
    markers.forEach((marker) => marker.setMap(null));
    setMarkers([]);
  };

  // Function to call the unified API and add markers to the map
  const handleSearch = async () => {
    // Ensure both county and department are selected
    clearMarkers(); // Clear existing markers before setting new ones
    try {
      // Construct the API endpoint with query parameters
      const apiEndpoint = `http://44.228.29.165:8000/api/locations/?county=${encodeURIComponent(
        selectedCounty
      )}&department=${encodeURIComponent(selectedDept)}`;

      // Fetch data from the API
      const response = await axios.get(apiEndpoint);
      const locations = response.data; // Response should be an array of location objects
      console.log(response.data);

      // Check if googleMap is initialized
      if (!googleMap) {
        console.error("The googleMap is not initialized yet.");
        return;
      }

      // Create new markers and add to map
      const newMarkers = locations.map((location: Location) => {
        const lat = Number(location.location_x_coordinate);
        const lng = Number(location.location_y_coordinate);
        const icon = {
          url: departmentMarkers[
            location.department as keyof typeof departmentMarkers
          ],
          scaledSize: new google.maps.Size(30, 30),
        };

        const marker = new google.maps.Marker({
          position: { lat, lng },
          map: googleMap,
          title: selectedDept,
          icon: icon,
        });

        marker.addListener("click", () => {
          setPopupData({
            department: location.department,
            county_name: location.county_name,
            dataset_id: location.dataset_id || "No dataset ID",
          });
          setShowPopup(true);
        });

        return marker;
      });

      // Update state with new markers
      setMarkers(newMarkers);
      // Set Search Result Table
      setTableData(locations);
    } catch (error) {
      console.error("Error fetching locations:", error);
      // Handle error (e.g., show alert to user)
    }
  };

  const handleCountyChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedCounty(event.target.value);
  };

  const handleDeptChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedDept(event.target.value);
  };

  return (
    <>
      <div className={style.searchContainer}>
        <input
          type="text"
          placeholder="Enter county name"
          value={selectedCounty}
          onChange={handleCountyChange}
        />
        <select value={selectedDept} onChange={handleDeptChange}>
          <option value="all">All</option>
          <option value="blocked_roads">Blocked Roads</option>
          <option value="security">Security Concerns</option>
          <option value="weather">Weather Events</option>
          <option value="wildfires">Wildfires</option>
        </select>
        <button onClick={handleSearch}>Search</button>
      </div>
      <div ref={googleMapRef} style={{ width: "100%", height: "100%" }} />
      {showPopup && (
        <Popup
          department={popupData.department}
          county_name={popupData.county_name}
          dataset_id={popupData.dataset_id}
          onClose={() => setShowPopup(false)}
        />
      )}
    </>
  );
};

export default GoogleMap;
