import { useState } from "react";
import "../styles/Register.css";
function RegisterPage() {
    const [formData, setFormData] = useState({
        username: "",
        first_name: "",
        last_name: "",
        email: "",
        role: "student",
        password: "",
    });
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };
    const handleRegister = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage("");
        try {
            const response = await fetch(
                "http://127.0.0.1:8000/api/register/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(formData),
                }
            );
            const data = await response.json();
            console.log("Backend response:", data);
            if (response.ok) {
                setMessage("Registration successful!");
                // clear form
                setFormData({
                    username: "",
                    first_name: "",
                    last_name: "",
                    email: "",
                    role: "student",
                    password: "",
                });
            } else {
                setMessage(
                    data.detail ||
                    data.message ||
                    "Registration failed"
                );
            }
        } catch (error) {
            console.error("Error:", error);
            setMessage(
                "Cannot connect to Django backend"
            );
        } finally {
            setLoading(false);
        }
    };
    return (
        <div className="register-container">
            <form className="register-form"onSubmit={handleRegister}>
                <h2>Create Account</h2>
                {/* USERNAME */}
                <div className="input-box">
                    <input
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        required/>
                    <label>Username</label>
                </div>
                {/* FIRST NAME */}
                <div className="input-box">
                    <input
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}/>

                    <label>First Name</label>

                </div>


                {/* LAST NAME */}
                <div className="input-box">

                    <input
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                    />

                    <label>Last Name</label>

                </div>


                {/* EMAIL */}
                <div className="input-box">

                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                    />

                    <label>Email Address</label>

                </div>


                {/* ROLE */}
                <div className="input-box">

                    <select
                        name="role"
                        value={formData.role}
                        onChange={handleChange}
                    >

                        <option value="student">
                            Student
                        </option>

                        <option value="hostel_owner">
                            Hostel Owner
                        </option>

                        <option value="admin">
                            Admin
                        </option>

                    </select>

                    <label>Role</label>

                </div>


                {/* PASSWORD */}
                <div className="input-box">

                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />

                    <label>Password</label>

                </div>


                {/* MESSAGE */}
                {message && (
                    <p className="register-message">
                        {message}
                    </p>
                )}


                {/* BUTTON */}
                <button
                    type="submit"
                    disabled={loading}
                >

                    {loading
                        ? "Registering..."
                        : "Register"
                    }

                </button>


                <p className="login-link">

                    Already have an account?{" "}

                    <a href="/">
                        Login
                    </a>

                </p>

            </form>

        </div>
    );
}

export default RegisterPage;