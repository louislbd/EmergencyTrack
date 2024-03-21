import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/Register.css";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/Auth";

type UserFormState = {
  firstName: string;
  lastName: string;
  emailAddress: string;
  county: string;
  password: string;
  confirmPassword: string;
  status: "public" | "countyDirector" | "";
};

interface County {
  county_id: number;
  county_name: string;
  county_population: number;
}

const RegistrationForm: React.FC = () => {
  const [formData, setFormData] = useState<UserFormState>({
    firstName: "",
    lastName: "",
    emailAddress: "",
    county: "",
    password: "",
    confirmPassword: "",
    status: "",
  });
  const statusCode =
    formData.status === "public"
      ? 0
      : formData.status === "countyDirector"
      ? 1
      : null;
  const [counties, setCounties] = useState<County[]>([]);
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    const fetchCounties = async () => {
      try {
        const response = await axios.get(
          "http://44.228.29.165:8000/api/countys"
        );
        setCounties(response.data); // Assuming the response is an array of county objects
      } catch (error) {
        console.error("Error fetching counties: ", error);
        // Handle error
      }
    };

    fetchCounties();
  }, []); // Empty dependency array to run only once on mount

  const handleInputChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };
  const { login } = useAuth();
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const statusCode =
      formData.status === "public"
        ? 0
        : formData.status === "countyDirector"
        ? 1
        : null;
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    if (!formData.status) {
      alert("Please select either Public or County Director!");
      return;
    }

    // Registration API Call
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/register", {
        first_name: formData.firstName,
        last_name: formData.lastName,
        email: formData.emailAddress,
        password: formData.password,
        account_type: statusCode,
      });
      const { user, token } = response.data;
      login(user, token);
      alert("Registration successful");
      // Navigate based on the user role
      if (formData.status === "countyDirector") {
        navigate("/upload");
      } else {
        navigate("/");
      }
    } catch (error) {
      console.error("Registration Error: ", error);
      alert("Registration failed");
    }
  };

  const handleLoginSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    // Login API Call
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login", {
        email: formData.emailAddress,
        password: formData.password,
      });
      const { user, access_token } = response.data;
      login(user, access_token);
      console.log(user);
      alert("Login successful");
      navigate("/");
    } catch (error) {
      console.error("Login Error: ", error);
      alert("Login failed");
    }
  };
  // Animation
  const [isRightPanelActive, setIsRightPanelActive] = useState(false);

  // Register Sign up button
  const handleSignUpClick = () => {
    setIsRightPanelActive(true);
  };

  // Register Sign up function
  const handleSignInClick = () => {
    setIsRightPanelActive(false);
  };

  return (
    <div
      className={`container ${isRightPanelActive ? "right-panel-active" : ""}`}
      id="container"
    >
      {/* Registration Form */}
      <div className="form-container sign-up-container">
        <form onSubmit={handleSubmit}>
          <h1>Register</h1>
          <div>
            <label>First Name</label>
            <input
              type="text"
              name="firstName"
              value={formData.firstName}
              onChange={handleInputChange}
              maxLength={40}
            />
          </div>
          <div>
            <label>Last Name</label>
            <input
              type="text"
              name="lastName"
              value={formData.lastName}
              onChange={handleInputChange}
              maxLength={40}
            />
          </div>
          <div>
            <label>Email Address</label>
            <input
              type="email"
              name="emailAddress"
              value={formData.emailAddress}
              onChange={handleInputChange}
              maxLength={40}
            />
          </div>
          <div className="select-county">
            <label>County</label>
            <select
              name="county"
              value={formData.county}
              onChange={handleInputChange}
            >
              <option value="" disabled>
                Select a County
              </option>
              {counties.map((county) => (
                <option value={county.county_name} key={county.county_id}>
                  {county.county_name}
                </option>
              ))}
            </select>
          </div>
          <div className="radio-group">
            <label>
              Public
              <input
                type="radio"
                name="status"
                value="public"
                checked={formData.status === "public"}
                onChange={handleInputChange}
                maxLength={40}
              />
            </label>
            <label>
              County Director
              <input
                type="radio"
                name="status"
                value="countyDirector"
                checked={formData.status === "countyDirector"}
                onChange={handleInputChange}
                maxLength={40}
              />
            </label>
          </div>
          <div>
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              maxLength={40}
            />
          </div>
          <div>
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              maxLength={40}
            />
          </div>
          <button type="submit">Register</button>
        </form>
      </div>

      {/* Login Form */}
      <div className="form-container sign-in-container">
        <form onSubmit={handleLoginSubmit}>
          <h1>Sign in</h1>
          <span>or use your account</span>
          <input
            type="email"
            name="emailAddress"
            placeholder="Email"
            value={formData.emailAddress}
            onChange={handleInputChange}
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleInputChange}
          />
          <a href="forgot-password">Forgot your password?</a>
          <button type="submit">Sign In</button>
        </form>
      </div>
      <div className="overlay-container">
        <div className="overlay">
          <div className="overlay-panel overlay-left">
            <h1>Welcome Back!</h1>
            <p>please login with your personal info</p>
            <button className="ghost" id="signIn" onClick={handleSignInClick}>
              Sign In
            </button>
          </div>
          <div className="overlay-panel overlay-right">
            <h1>Hello, Friend!</h1>
            <p>start journey with us</p>
            <button className="ghost" id="signUp" onClick={handleSignUpClick}>
              Sign Up
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegistrationForm;
