import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function Profile() {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

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
      <p><strong>Skills:</strong> {profile.skills?.map(s => s.name).join(", ") || "None"}</p>
      <p><strong>Interests:</strong> {profile.interests?.map(i => i.name).join(", ") || "None"}</p>
      <p><strong>Location:</strong> {profile.location || "Not set"}</p>
    </div>
  );
}

export default Profile;
