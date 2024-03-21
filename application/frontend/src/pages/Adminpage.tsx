import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import GoogleMap from "../components/Googlemap";
import Footer from "../components/Footer";
import style from "../styles/Adminpage.module.css";
import { useAuth } from "../context/Auth";

interface User {
  user_id: string;
  first_name: string;
  last_name: string;
  email: string;
  account_type: number;
}

const AdminPage: React.FC = () => {
  const [users, setUsers] = useState<{ details: any[] }>({ details: [] });
  const { getToken } = useAuth();

  const fetchUsers = () => {
    axios
      .get("http://44.228.29.165:8000/api/pending_officers", {
        withCredentials: true, // Ensures cookies are sent with the request
      })
      .then((res) => {
        //console.log(res);
        // Handle success
        setUsers({
          details: res.data,
        });
      })
      .catch((err) => {
        // Handle error
        console.error(err);
      });
  };
  useEffect(() => {
    fetchUsers();
  }, []);

  const acceptUser = (user: User) => {
    axios
      .put(
        `http://44.228.29.165:8000/api/users/${user.user_id}`,
        {
          user_id: user.user_id,
          first_name: user.first_name,
          last_name: user.last_name,
          email: user.email,
          account_type: 2.0, // Update the account_type to 2.0 for accepting
        },
        {
          withCredentials: true,
        }
      )
      .then(() => {
        fetchUsers();
      })
      .catch((err) => {
        console.error(err);
      });
  };

  const deleteUser = (user: User) => {
    axios
      .put(`http://44.228.29.165:8000/api/users/${user.user_id}`, {
        data: {
          // If your API requires sending data in delete request, include it here
          user_id: user.user_id,
          first_name: user.first_name,
          last_name: user.last_name,
          email: user.email,
          account_type: 1.0,
        },
        withCredentials: true,
      })
      .then(() => {
        fetchUsers();
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return (
    <div>
      <Navbar />
      <div className={style.adminpageContainer}>
        <div className={style.leftHalf}>
          <h1>Manage Accounts</h1>
          <table className={style.board}>
            <thead>
              <tr>
                <th>Name</th>
                <th>County</th>
                <th>Role</th>
                <th>email</th>
                <th>Accept</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              {users.details.map((user, id) => (
                <tr key={id}>
                  <td>{user.user_id}</td>
                  <td>{user.first_name}</td>
                  <td>{user.last_name}</td>
                  <td>{user.email}</td>
                  <td>
                    <button onClick={() => acceptUser(user)}>Accept</button>
                  </td>
                  <td>
                    <button onClick={() => deleteUser(user)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className={style.rightHalf}>
          <GoogleMap />
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default AdminPage;
