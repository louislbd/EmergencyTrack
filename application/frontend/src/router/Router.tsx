import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Homepage from "../pages/Homepage";
import NotFound from "../pages/NotFound";
import RegistrationForm from "../pages/RegistrationForm";
import UploadPage from "../pages/UploadPage";
import AdminPage from "../pages/Adminpage";
import NotificationPage from "../pages/Notification";
import ProtectedRoute from "../components/ProtectedRoute";
import ReportDeaths from "../pages/ReportDeaths";
import ReportBlockedRoads from "../pages/ReportBlockedRoads";
import ReportWildFires from "../pages/ReportWildFires";
import ReportCovid from "../pages/ReportCovid";
import ReportSecurity from "../pages/ReportSecurity";
import Authpage from "../pages/Authpage";

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/login" element={<Authpage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="*" element={<NotFound />} />
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <AdminPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/notification"
          element={
            <ProtectedRoute>
              <NotificationPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/report-deaths"
          element={
            <ProtectedRoute>
              <ReportDeaths />
            </ProtectedRoute>
          }
        />
        <Route
          path="/report-blockedroads"
          element={
            <ProtectedRoute>
              <ReportBlockedRoads />
            </ProtectedRoute>
          }
        />
        <Route
          path="/report-wildfires"
          element={
            <ProtectedRoute>
              <ReportWildFires />
            </ProtectedRoute>
          }
        />
        <Route
          path="/report-covid"
          element={
            <ProtectedRoute>
              <ReportCovid />
            </ProtectedRoute>
          }
        />
        <Route
          path="/report-security"
          element={
            <ProtectedRoute>
              <ReportSecurity />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
