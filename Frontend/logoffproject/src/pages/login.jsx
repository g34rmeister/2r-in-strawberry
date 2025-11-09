import { useState } from "react";
import { login } from "../components/auth";
//Define AuthLogin component
const AuthLogin = () => {
  const [username, setUsernmae] = useState("");
  const [password, setPassword] = useState("");


  // Function to handle sign in
  async function handleLogin() {
    //Check if username and password are not empty
    if (username && password){
      try {
        const data = await login(username, password);//Wait for external login function reply
        setUsernmae("");
        setPassword("");
      } catch (error) {
        //If somthing in try failed, default to here
        console.error(error);
      }
    }
  };

  // Function to handle sign out
  const handleSignOut = async () => {
    try {
      // TODO: send sign-out request to backend
      console.log("Signing out:", username);
    } catch (error) {
      console.error("Sign out failed:", error);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
      <input
        type="username"
        placeholder="enter username"
        value={username}
        onChange={(e) => setUsernmae(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password..."
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Sign In</button>
      <button onClick={handleSignOut}>Sign Out</button>
    </div>

  );
};

export default AuthLogin;