import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import Groups from "./pages/Groups";
import UpdateProfile from "./pages/UpdateProfile";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          {/* <Route path="/login/profile/:username" element={<Profile />} /> */}
          <Route path="/register" element={<Register />} />
          <Route path="/profile/:username" element={<Profile />} />
          <Route path="/groups" element={<Groups />} />
          <Route path="/profile/:username/update" element={<UpdateProfile />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
