import { Button } from "@mui/material";
import { useResult } from "../hooks/useResult";
import { useLocation, useNavigate } from "react-router-dom";
import "./style.css";

export function Result() {
  const navigate = useNavigate();
  const location = useLocation();
  const token = location.state.token;
  const result = useResult(token);
  return (
    <div className="question-container">
      <div className="question-content">
        <div>
          <h2>Rezultat</h2>
          <div style={{ display: "flex", justifyContent: "center" }}>
            {result.data?.programs !== undefined &&
              result.data?.programs.map((program, index) => (
                <h4 style={{ margin: "8px" }} key={index}>
                  {program}
                </h4>
              ))}
          </div>
          {result.data?.universities !== undefined &&
            result.data?.universities.map((university, index) => (
              <div key={index} className="result-container">
                <div className="index-container">
                  <h4 style={{ marginTop: "30px" }}>{index}</h4>
                </div>
                <div className="result-universities">
                  <div className="result-faculty"> {university.faculty}</div>
                  <div>
                    {university.name}
                    {", "}
                    {university.country}
                  </div>
                </div>
              </div>
            ))}
        </div>

        <div style={{ display: "flex", placeContent: "center" }}>
          <div style={{ marginTop: "8px" }}>Nu esti multumit de rezultat?</div>
          <Button
            variant="text"
            style={{ color: "#0757f9" }}
            onClick={() => navigate("/")}
          >
            Repeta testul
          </Button>
        </div>
      </div>
    </div>
  );
}
