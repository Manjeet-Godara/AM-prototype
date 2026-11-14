function LastUpdated({ lastUpdated, error }) {

    function formatTime(timestamp) {
        if (!timestamp) {
            return "Never";
        }

        return new Date(timestamp).toLocaleString();
    }

    return (
        <div style={{ fontSize: "13px" }}>

            <span style={{ color: "#64748b" }}>
                Last updated: {formatTime(lastUpdated)}
            </span>

            {error && (
                <span
                    style={{
                        color: "#dc2626",
                        marginLeft: "12px",
                        fontWeight: "600"
                    }}
                >
                    ⚠ Last poll failed
                </span>
            )}

        </div>
    );
}

export default LastUpdated;