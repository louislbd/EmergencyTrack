import React, { createContext, useState, useContext, ReactNode } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

interface AuthContextType {
  user: any;
  login: (userData: any, access_token: string) => void;
  logout: () => void;
  getToken: () => string | null;
}

const AuthContext = createContext<AuthContextType>(null!);

export const useAuth = () => useContext(AuthContext);

// Define a type for AuthProvider props
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  // 로컬 스토리지에서 사용자 데이터를 가져와 초기 상태 설정
  const [user, setUser] = useState(() => {
    const storedUserData = localStorage.getItem("user");
    return storedUserData ? JSON.parse(storedUserData) : null;
  });

  const login = (userData: any, access_token: string) => {
    if (typeof access_token !== "string" || access_token.trim() === "") {
      console.error("Invalid or empty token provided");
      return; // Optionally, handle this case further as needed
    }

    try {
      // Optionally decode token if needed for other purposes
      const decodedToken = jwtDecode(access_token) as { [key: string]: any };

      // Here, use the full userData to set the user state
      setUser(userData);

      localStorage.setItem("user", JSON.stringify(userData));
      localStorage.setItem("token", access_token);
      document.cookie = `access_token=${access_token}; path=/; max-age=9000; Secure`;

      // Attach token to every request using axios interceptor
      axios.interceptors.request.use((config) => {
        config.headers.Authorization = `Bearer ${access_token}`;
        return config;
      });
    } catch (error) {
      console.error("Error decoding token:", error);
    }
  };
  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
    localStorage.removeItem("token");

    // remove the token from axios interceptor
    axios.interceptors.request.use((config) => {
      delete config.headers.Authorization;
      return config;
    });
  };

  const getToken = () => {
    return localStorage.getItem("token");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, getToken }}>
      {children}
    </AuthContext.Provider>
  );
};
