import { useState, useEffect } from "react";
import style from "../styles/Authpage.module.css";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import axios from "axios";
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

const Authpage: React.FC = () => {
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
      const response = await axios.post(
        "http://44.228.29.165:8000/api/register",
        {
          first_name: formData.firstName,
          last_name: formData.lastName,
          email: formData.emailAddress,
          password: formData.password,
          account_type: statusCode,
        }
      );
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
      const response = await axios.post("http://44.228.29.165:8000/api/login", {
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

  return (
    <div>
      <Navbar />
      <div className={style.homepageContainer}>
        <div className={style.leftHalf}>
          <h1 className={style.h1}>Login</h1>
          <form onSubmit={handleLoginSubmit}>
            <div className={style.centerIt}>
              <input
                className={style.input}
                type="email"
                name="emailAddress"
                placeholder="Email"
                value={formData.emailAddress}
                onChange={handleInputChange}
              />
            </div>
            <br />
            <div className={style.centerIt}>
              <input
                className={style.input}
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
              />
            </div>
            <br />
            <div className={style.centerIt}>
              <a className={style.a} href="forgot-password">
                Forgot your password?
              </a>
            </div>
            <br />
            <div className={style.centerIt}>
              <button className={style.button} type="submit">
                Sign In
              </button>
            </div>
          </form>
        </div>

        <div className={style.rightHalf}>
          <h1 className={style.h1}>Register</h1>
          <form className={style.form} onSubmit={handleSubmit}>
            <div className={style.centerIt}>
              <label className={style.label}>First Name</label>
              <br />
              <input
                className={style.input}
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleInputChange}
                maxLength={40}
              />
            </div>
            <div className={style.centerIt}>
              <label className={style.label}>Last Name</label>
              <br />
              <input
                className={style.input}
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleInputChange}
                maxLength={40}
              />
            </div>
            <div className={style.centerIt}>
              <label className={style.label}>Email Address</label>
              <br />
              <input
                className={style.input}
                type="email"
                name="emailAddress"
                value={formData.emailAddress}
                onChange={handleInputChange}
                maxLength={40}
              />
            </div>
            <div className={style.selectCounty}>
              <label className={style.label}>County</label>
              <br />
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
            <div className={style.radioGroup}>
              <label className={style.label}>
                Public
                <input
                  className={style.input}
                  type="radio"
                  name="status"
                  value="public"
                  checked={formData.status === "public"}
                  onChange={handleInputChange}
                  maxLength={40}
                />
              </label>
              <label className={style.label}>
                County Director
                <input
                  className={style.input}
                  type="radio"
                  name="status"
                  value="countyDirector"
                  checked={formData.status === "countyDirector"}
                  onChange={handleInputChange}
                  maxLength={40}
                />
              </label>
            </div>
            <div className={style.centerIt}>
              <label className={style.label}>Password</label>
              <br />
              <input
                className={style.input}
                type="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                maxLength={40}
              />
            </div>
            <div className={style.centerIt}>
              <label className={style.label}>Confirm Password</label>
              <br />
              <input
                className={style.input}
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                maxLength={40}
              />
            </div>
            <button className={style.button} type="submit">
              Register
            </button>
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Authpage;
