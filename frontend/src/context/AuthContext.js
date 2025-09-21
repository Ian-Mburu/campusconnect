import React, { createContext, useState } from 'react';
import axiosInstance from '../api/axios';


export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [authToken, setAuthToken] = useState(localStorage.getItem('authToken') || null);
    const [user, setUser] = useState(null)


    // Register User

    const registerUser = async (username, password, email, userType) => {
        try {
          let response = await fetch("http://127.0.0.1:8000/api/register/", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              username: username,
              password: password,
              email: email,
              user_type: userType
            })
          });
      
          let data = await response.json();
    if (response.status === 201) {
      return { success: true, message: data.message || "Registration successful!" };
    } else {
      return { success: false, message: data.message || "Registration failed" };
    }
  } catch (error) {
    return { success: false, message: "Registration error. Please try again." };
  }
};
      
    // Login user and store token

    const loginUser = async (username, password) => {
        try {
            const response = await axiosInstance.post('token/', { username, password });
            localStorage.setItem('authToken', response.data.access);
            setAuthToken(response.data.access);
            return true;
        } catch (error) {
            console.error('Login failed:', error);
            return false;
        }
    };


    // Logout user and clear token

    const logoutUser = () => {
        localStorage.removeItem('authToken');
        setAuthToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ authToken, user, setUser, loginUser, registerUser, logoutUser }}>
            {children}
        </AuthContext.Provider>
    );
};


// whats happening here is that we are creating a context for authentication using React's Context API. This context will provide authentication-related functions and state to the rest of the application.