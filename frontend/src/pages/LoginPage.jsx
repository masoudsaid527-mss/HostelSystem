import { useState } from "react";
import "../styles/LoginPage.css";
function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(
                "http://127.0.0.1:8000/api/auth/login/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password,
                    }),
                }
            );
            const data = await response.json();
            console.log("Backend response:", data);
            if (response.ok) {
                alert("Login successful");
                // kama backend inarudisha JWT
                if (data.access) {
                    localStorage.setItem(
                        "access_token",
                        data.access
                    );
                }
                if (data.refresh) {
                    localStorage.setItem(
                        "refresh_token",
                        data.refresh
                    );
                }
            } else {
                alert(
                    data.detail ||
                    data.message ||
                    "Login failed"
                );
            }
        } catch (error) {
            console.error("Login error:", error);
            alert("Cannot connect to backend");
        }
    };
    return (
        <div className="login-container">
            <form
                className="login-form"
                onSubmit={handleLogin}>
                <h2>Welcome Back!</h2>
                <div className="input-box">
                    <input
                        type="text"
                        name="username"
                        value={username}
                        onChange={(e) =>setUsername(e.target.value)}required/><label>
                        Username
                    </label>

                </div>

                <div className="input-box">

                    <input
                        type="password"
                        name="password"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                        required
                    />

                    <label>
                        Password
                    </label>

                </div>

                <button type="submit">
                    Login
                </button>
                <p>You don't have an account? <a href="/Register">Register</a></p>

            </form>

        </div>
    );
}

export default LoginPage;