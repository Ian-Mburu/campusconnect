import React,{ useState, useContext } from "react"
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";




const Login = () => {
    const { loginUser } = useContext(AuthContext);
    const [ username, setUsername ] = useState('');
    const [ password, setPassword ] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await loginUser(username, password);
        if (success) {
            navigate('profile/' + username);
        } else {
            alert('Login failed. Please check your credentials.');
        }
    };


    return (
        <div className="login-container">
            <h2>Login</h2>
        <form onSubmit={handleSubmit}>
            <input className="input-field" type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
            <input className="input-field" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <button className="submit-button" type="submit">Login</button>
        </form>
        </div>
    );
};

export default Login;