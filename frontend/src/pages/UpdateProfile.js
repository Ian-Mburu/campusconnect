import React, { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function UpdateProfile() {
  const { username } = useParams();
  const navigate = useNavigate();
  const { authToken } = useContext(AuthContext);

  const [formData, setFormData] = useState({
    department: "",
    year_of_study: "",
    location: "",
    skills: "",
    interests: "",
    bio: "",
    avatar: null,
    birth_date: "",
    contact_number: "",
    address: "",
    linkedin_profile: "",
    github_profile: "",
    twitter_profile: "",
    facebook_profile: "",
    personal_website: "",
    achievements: "",
    courses: "",
  });

  useEffect(() => {
    const fetchProfile = async () => {
      let response = await fetch(
        `http://127.0.0.1:8000/api/userprofiles/${username}/`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );
      if (response.ok) {
        let data = await response.json();
        setFormData({
          department: data.department || "",
          year_of_study: data.year_of_study || "",
          location: data.location || "",
          skills: (data.skills || []).map(s => s.name).join(", "),
          interests: (data.interests || []).map(i => i.name).join(", "),
          birth_date: data.birth_date || "",
          contact_number: data.contact_number || "",
          address: data.address || "",
          linkedin_profile: data.linkedin_profile || "",
          github_profile: data.github_profile || "",
          twitter_profile: data.twitter_profile || "",
          facebook_profile: data.facebook_profile || "",
          personal_website: data.personal_website || "",
          achievements: data.achievements || "",
          courses: (data.Courses || []).map(c => c.title).join(", "),
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

    const form = new FormData();
    for (const key in formData) {
      if (key === "skills") {
        formData.skills.split(",").forEach(s => form.append("skills", s.trim()));
      } else if (key === "interests") {
        formData.interests.split(",").forEach(i => form.append("interests", i.trim()));
      } else if (key === "courses") {
        formData.courses.split(",").forEach(c => form.append("Courses", c.trim()));
      } else if (key === "avatar" && formData.avatar) {
        form.append("avatar", formData.avatar);
      } else if (formData[key]) {
        form.append(key, formData[key]);
      }
    }

    let response = await fetch(
      `http://127.0.0.1:8000/api/userprofiles/${username}/`,
      {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
        body: form,
      }
    );

    if (response.ok) {
      alert("Profile updated successfully!");
      navigate(`/profile/${username}`);
    } else {
      alert("Failed to update profile.");
    }
  };

  return (
    <div className="container mt-4">
      <h2>Update Profile</h2>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <label>Department</label>
        <input type="text" name="department" value={formData.department} onChange={handleChange} />

        <label>Year of Study</label>
        <input type="text" name="year_of_study" value={formData.year_of_study} onChange={handleChange} />

        <label>Location</label>
        <input type="text" name="location" value={formData.location} onChange={handleChange} />

        <label>Skills (comma separated)</label>
        <input type="text" name="skills" value={formData.skills} onChange={handleChange} />

        <label>Interests (comma separated)</label>
        <input type="text" name="interests" value={formData.interests} onChange={handleChange} />

        <label>Birth Date</label>
        <input type="date" name="birth_date" value={formData.birth_date} onChange={handleChange} />

        <label>Contact Number</label>
        <input type="text" name="contact_number" value={formData.contact_number} onChange={handleChange} />

        <label>Address</label>
        <textarea name="address" value={formData.address} onChange={handleChange}></textarea>

        <label>LinkedIn</label>
        <input type="url" name="linkedin_profile" value={formData.linkedin_profile} onChange={handleChange} />

        <label>GitHub</label>
        <input type="url" name="github_profile" value={formData.github_profile} onChange={handleChange} />

        <label>Twitter</label>
        <input type="url" name="twitter_profile" value={formData.twitter_profile} onChange={handleChange} />

        <label>Facebook</label>
        <input type="url" name="facebook_profile" value={formData.facebook_profile} onChange={handleChange} />

        <label>Personal Website</label>
        <input type="url" name="personal_website" value={formData.personal_website} onChange={handleChange} />

        <label>Achievements</label>
        <textarea name="achievements" value={formData.achievements} onChange={handleChange}></textarea>

        <label>Courses (comma separated)</label>
        <input type="text" name="courses" value={formData.courses} onChange={handleChange} />

        <button type="submit" className="btn btn-success mt-3">Save Changes</button>
      </form>
    </div>
  );
}

export default UpdateProfile;
