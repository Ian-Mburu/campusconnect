import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

function Profile() {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/profiles/${username}/`);
        if (!response.ok) throw new Error("Profile not found");
        const data = await response.json();
        setProfile(data);
      } catch (error) {
        console.error("Error fetching profile:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [username]);

  if (loading) return <p>Loading profile...</p>;
  if (!profile) return <p>Profile not found</p>;

  return (
    <div className="container mt-4">
      <h2>{profile.username}'s Profile</h2>
      <p><strong>Email:</strong> {profile.email}</p>

      {/* Show role-specific data */}
      {profile.user_type === "student" && profile.profile && (
        <div>
          <h3>Student Info</h3>
          <p>Department: {profile.profile.department || "Not set"}</p>
          <p>Year of Study: {profile.profile.year_of_study || "Not set"}</p>
          <p>Skills: {profile.profile.skills?.map(s => s.name).join(", ") || "None"}</p>
          <p>Interests: {profile.profile.interests?.map(i => i.name).join(", ") || "None"}</p>
        </div>
      )}

      {profile.user_type === "lecturer" && profile.profile && (
        <div>
          <h3>Lecturer Info</h3>
          <p>Department: {profile.profile.department || "Not set"}</p>
          <p>Subjects: {profile.profile.subjects || "Not set"}</p>
        </div>
      )}

      {profile.user_type === "admin" && profile.profile && (
        <div>
          <h3>Admin Info</h3>
          <p>Department: {profile.profile.department || "Not set"}</p>
          <p>Role: {profile.profile.role || "Not set"}</p>
        </div>
      )}

      <button
        className="btn btn-primary mt-3"
        onClick={() => navigate(`/profile/${username}/update`)}
      >
        Update Profile
      </button>
    </div>
  );
}

export default Profile;
