import React, { useState, useEffect } from "react";
import IconMenu from "../assets/images/icon-menu.png";
import IconProfile from "../assets/images/icon-avatar.png";
import style from "../styles/Navbar.module.css";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/Auth";

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  useEffect(() => {
    // This code will run whenever the `user` state changes.

    if (user) {
      console.log("User is logged in:", user.last_name);
      // Here you can add any logic you need to execute when the user logs in.
      // For example, fetching additional user data, updating the UI, etc.
    } else {
      console.log("No user is logged in.");
      // Add any logic you need for when there is no logged-in user.
    }
  }, [user]);
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const toggleDropdown = () => {
    if (user) {
      setIsDropdownOpen((prev) => !prev);
    }
  };

  const handleDropdownItemClick = (path: string) => {
    navigate(path);
    setIsDropdownOpen(false);
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };
  const isAdmin = user && (user.isAdmin || user.account_type_name === "Admin");

  return (
    <div className={style.navbar}>
      <div className={style.navbarLeft}>
        <div className={style.dropdown}>
          <img
            src={IconMenu}
            alt="Menu"
            className={style.iconMenu}
            onClick={toggleDropdown}
          />
          {isDropdownOpen && (
            <div className={style.dropdownContent}>
              <span onClick={() => handleDropdownItemClick("/")}>Home</span>
              {isAdmin && (
                <span onClick={() => handleDropdownItemClick("/admin")}>
                  Admin
                </span>
              )}
              <span onClick={() => handleDropdownItemClick("/notification")}>
                Notifications
              </span>
              <span onClick={() => handleDropdownItemClick("/report-deaths")}>
                Report Deaths
              </span>
              <span
                onClick={() => handleDropdownItemClick("/report-blockedroads")}
              >
                Report Blocked Roads
              </span>
              <span
                onClick={() => handleDropdownItemClick("/report-wildfires")}
              >
                Report Wild Fires
              </span>
              <span onClick={() => handleDropdownItemClick("/report-security")}>
                Report Security Concerns
              </span>
              <span onClick={() => handleDropdownItemClick("/report-covid")}>
                Report Covid19 Cases
              </span>
            </div>
          )}
        </div>
        <span className={style.emergencyTrack} onClick={() => navigate("/")}>
          EmergencyTrack
        </span>
      </div>
      <div className={style.navbarRight}>
        {user ? (
          <>
            <span className={style.username}>
              {user.first_name} {user.last_name}
            </span>
            <button className={style.profileButton} onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <button
            className={style.profileButton}
            onClick={() => navigate("/login")}
          >
            <img
              src={IconProfile}
              alt="Profile"
              className={style.iconProfile}
            />
            Profile
          </button>
        )}
      </div>
    </div>
  );
};

export default Navbar;
