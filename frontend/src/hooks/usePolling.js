
import { useState, useEffect, useCallback, useRef } from "react";
import { apiFetch } from "../services/api";

export function usePolling(path, interval = 5000) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);

    const isFetching = useRef(false);

    const fetchData = useCallback(async () => {
        // Prevent overlapping requests
        if (isFetching.current) return;

        isFetching.current = true;

        try {
            const result = await apiFetch(path);

            if (result.error) {
                setError(result.error);
            } else {
                setData(result.data);
                setError(null);
                setLastUpdated(new Date());
            }
        } catch (err) {
            setError(err.message || "Something went wrong");
        } finally {
            setLoading(false);
            isFetching.current = false;
        }
    }, [path]);

    useEffect(() => {
        // Fetch immediately on page load
        fetchData();

        // Poll at the specified interval
        const intervalId = setInterval(fetchData, interval);

        // Cleanup when component unmounts
        return () => clearInterval(intervalId);

    }, [fetchData, interval]);

    return {
        data,
        loading,
        error,
        lastUpdated,
        refetch: fetchData
    };
}
