import React, { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function UpdateProfile() {
  const { username } = useParams();
  const navigate = useNavigate();
  const { authToken } = useContext(AuthContext);

  const [userType, setUserType] = useState(""); // student, lecturer, admin
  const [formData, setFormData] = useState({});

  useEffect(() => {
    const fetchProfile = async () => {
      let response = await fetch(
        `http://127.0.0.1:8000/api/profiles/${username}/`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );
      if (response.ok) {
        let data = await response.json();
        setUserType(data.user_type);

        // Prefill data based on profile type
        setFormData({
          department: data.profile?.department || "",
          year_of_study: data.profile?.year_of_study || "",
          subjects_taught: data.profile?.subjects_taught || "",
          research_interests: data.profile?.research_interests || "",
          role_description: data.profile?.role_description || "",
          office_location: data.profile?.office_location || "",
          skills: (data.profile?.skills || []).join(", "),
          interests: (data.profile?.interests || []).join(", "),
        });
      }
    };
    fetchProfile();
  }, [username, authToken]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Build payload dynamically
    const payload = {
      skills: formData.skills.split(",").map((s) => s.trim()).filter(Boolean),
      interests: formData.interests.split(",").map((i) => i.trim()).filter(Boolean),
    };

    if (userType === "student") {
      payload.department = formData.department;
      payload.year_of_study = formData.year_of_study;
    } else if (userType === "lecturer") {
      payload.department = formData.department;
      payload.subjects_taught = formData.subjects_taught;
      payload.research_interests = formData.research_interests;
    } else if (userType === "admin") {
      payload.role_description = formData.role_description;
      payload.office_location = formData.office_location;
    }

    let response = await fetch(
      `http://127.0.0.1:8000/api/profiles/${username}/`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify(payload),
      }
    );

    if (response.ok) {
      alert("Profile updated successfully!");
      navigate(`/profile/${username}`);
    } else {
      const errorData = await response.json();
      console.error("Update failed:", errorData);
      alert("Failed to update profile.");
    }
  };

  return (
    <div className="container mt-4">
      <h2>Update {userType} Profile</h2>
      <form onSubmit={handleSubmit}>
        {/* Fields for all */}
        <label>Skills (comma separated)</label>
        <input
          type="text"
          name="skills"
          value={formData.skills || ""}
          onChange={handleChange}
        />

        <label>Interests (comma separated)</label>
        <input
          type="text"
          name="interests"
          value={formData.interests || ""}
          onChange={handleChange}
        />

        {/* Student-specific */}
        {userType === "student" && (
          <>
            <label>Department</label>
            <input
              type="text"
              name="department"
              value={formData.department || ""}
              onChange={handleChange}
            />
            <label>Year of Study</label>
            <input
              type="text"
              name="year_of_study"
              value={formData.year_of_study || ""}
              onChange={handleChange}
            />
          </>
        )}

        {/* Lecturer-specific */}
        {userType === "lecturer" && (
          <>
            <label>Department</label>
            <input
              type="text"
              name="department"
              value={formData.department || ""}
              onChange={handleChange}
            />
            <label>Subjects Taught</label>
            <input
              type="text"
              name="subjects_taught"
              value={formData.subjects_taught || ""}
              onChange={handleChange}
            />
            <label>Research Interests</label>
            <textarea
              name="research_interests"
              value={formData.research_interests || ""}
              onChange={handleChange}
            />
          </>
        )}

        {/* Admin-specific */}
        {userType === "admin" && (
          <>
            <label>Department</label>
            <input
              type="text"
              name="department"
              value={formData.department || ""}
              onChange={handleChange}
            />
            <label>Role Description</label>
            <textarea
              name="role_description"
              value={formData.role_description || ""}
              onChange={handleChange}
            />
            <label>Office Location</label>
            <input
              type="text"
              name="office_location"
              value={formData.office_location || ""}
              onChange={handleChange}
            />
          </>
        )}

        <button type="submit" className="btn btn-success mt-3">
          Save Changes
        </button>
      </form>
    </div>
  );
}

export default UpdateProfile;
