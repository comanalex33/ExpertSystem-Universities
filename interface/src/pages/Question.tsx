import { Button, Link } from "@mui/material";
import { useQuestion } from "../hooks/useQuestion";
import { useLocation, useNavigate } from "react-router-dom";
import "./style.css";

export function Question() {
  const navigate = useNavigate();
  const location = useLocation();
  const token = location.state.token;
  const question = useQuestion(token);

  if (question.data?.question === false) {
    navigate("/result", { state: { token: token } });
  }

  return (
    <div className="question-container">
      <div className="question-content">
        <h3 className="start-title">{question.data?.text}</h3>
        <div
          style={{
            display: "flex",
            gap: "16px",
            justifyContent: "center",
            marginTop: "50px",
          }}
        >
          <Button
            className="question-button"
            variant="contained"
            style={{ backgroundColor: "black" }}
            onClick={() => question.onClick(true)}
          >
            Da
          </Button>

          <Button
            className="question-button"
            variant="outlined"
            style={{ color: "black", border: " 1px solid black" }}
            onClick={() => question.onClick(false)}
          >
            Nu
          </Button>
        </div>
      </div>
    </div>
  );
}
