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
        const response = await fetch(`http://127.0.0.1:8000/api/userprofiles/${username}/`);
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
      <h2>{profile.user?.username}'s Profile</h2>
      <p><strong>Email:</strong> {profile.user?.email}</p>
      <p><strong>Department:</strong> {profile.department || "Not set"}</p>
      <p><strong>Year of Study:</strong> {profile.year_of_study || "Not set"}</p>
      <p><strong>Skills:</strong> {profile.skills || "None"}</p>
      <p><strong>Interests:</strong> {profile.interests || "None"}</p>
      <p><strong>Location:</strong> {profile.location || "Not set"}</p>
      <p><strong>Birth date:</strong> {profile.birth_date || "Not set"}</p>
      <p><strong>Contact no:</strong> {profile.contact_number || "Not set"}</p>
      <p><strong>Address:</strong> {profile.address || "Not set"}</p>
      <p><strong>LinkedIn:</strong> {profile.linkedin_profile || "Not set"}</p>
      <p><strong>Github:</strong> {profile.github_profile || "Not set"}</p>
      <p><strong>Twitter:</strong> {profile.twitter_profile || "Not set"}</p>
      <p><strong>Facebook:</strong> {profile.facebook_profile || "Not set"}</p>
      <p><strong>Website:</strong> {profile.personal_website || "Not set"}</p>
      <p><strong>Achievements:</strong> {profile.achievements || "Not set"}</p>
      <p><strong>Courses:</strong> {profile.courses || "Not set"}</p>


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
