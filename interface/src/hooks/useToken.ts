import { useEffect, useState } from "react";
import { TokenModel, server } from "../utils";

export function useToken() {
  const [data, setData] = useState<TokenModel>();
  const [error, setError] = useState<any>();
  const fetchData = async () => {
    try {
      const response = await fetch(server + "start");
      const json = await response.json();
      setData(json);
    } catch (error) {
      setError(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { data, error };
}
