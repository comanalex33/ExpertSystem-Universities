import { useEffect, useState } from "react";
import { ResultModel, server, TokenModel } from "../utils";

export function useResult(token: TokenModel) {
  const [data, setData] = useState<ResultModel>();
  const [error, setError] = useState<any>();
  const fetchResult = async () => {
    try {
      const response = await fetch(server + `results?token=${token.token}`);
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err);
    }
  };
  useEffect(() => {
    fetchResult();
  }, []);

  return { data, error };
}
