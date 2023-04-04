import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useToken } from "../hooks/useToken";
import "./style.css";

export function Start() {
  const navigate = useNavigate();
  const token = useToken();
  return (
    <div className="start-container">
      <header className="start-content">
        <div className="start">
          <h4 className="start-title">Welcome to Faculty Quiz!</h4>
          <Button
            variant="contained"
            style={{ backgroundColor: "#0c0303" }}
            onClick={() =>
              navigate("/question", { state: { token: token.data } })
            }
          >
            Start
          </Button>
        </div>
      </header>
    </div>
  );
}
