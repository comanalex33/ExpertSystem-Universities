import { useEffect, useState } from "react";
import { QuestionModel, ResultModel, TokenModel, server } from "../utils";

export function useQuestion(token: TokenModel) {
  const [data, setData] = useState<QuestionModel>();

  const [error, setError] = useState<any>();
  const fetchFirstQuestion = async () => {
    try {
      const response = await fetch(server + `execute?token=${token.token}`);
      const json = await response.json();
      setData(json);
    } catch (error) {
      setError(error);
    }
  };

  const fetchNextQuestion = async (answer: boolean) => {
    try {
      const response = await fetch(
        server + `execute?token=${token.token}&answer=${answer}`
      );
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err);
    }
  };

  useEffect(() => {
    fetchFirstQuestion();
  }, []);

  return {
    data,
    error,
    onClick: fetchNextQuestion,
  };
}
