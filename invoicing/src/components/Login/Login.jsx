import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://127.0.0.1:8000/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: username, password: password }),
            });
            const responseData = await response.json();
            console.log(responseData)
            if (!responseData.access_token) {
                alert("Login Failed");
            } else {
                localStorage.setItem("access_token", responseData.access_token);
                localStorage.setItem("refresh_token", responseData.refresh_token);
                navigate("/invoices");
            }
        } catch (error) {
            console.error("Error logging in:", error);
        }
    };

    return (
        <div
            className="container d-flex justify-content-center align-items-center vh-100"
            style={{ maxWidth: "700px" }}>
            <form className="p-4 border shadow w-100" onSubmit={handleLogin}>
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                        UserName:
                    </label>
                    <input
                        type="text"
                        id="email"
                        className="form-control"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                        Password:
                    </label>
                    <input
                        type="password"
                        id="password"
                        className="form-control"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit" className="btn btn-primary">
                    Login
                </button>
                <p>Don't have account? <a href="/signup">SignUp here</a></p>
            </form>
        </div>
    );
};

export default Login;
