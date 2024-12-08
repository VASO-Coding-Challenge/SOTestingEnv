import { Link } from "react-router-dom";
const ThankYouPage = () => {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Thank You</h1>
      <p>Your progress has been saved, and you’ve been logged out.</p>
      <Link to="/" style={{ textDecoration: "none", color: "#1976d2" }}>
        Go Back to Home
      </Link>
    </div>
  );
};

export default ThankYouPage;
