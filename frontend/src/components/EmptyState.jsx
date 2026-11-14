
function EmptyState() {
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                padding: "70px 20px",
                textAlign: "center",
                border: "1px dashed #d1d5db",
                borderRadius: "10px",
                backgroundColor: "#f9fafb",
                marginTop: "20px"
            }}
        >
            <div
                style={{
                    fontSize: "42px",
                    marginBottom: "16px"
                }}
            >
                🖥️
            </div>

            <h3
                style={{
                    fontSize: "18px",
                    fontWeight: "600",
                    color: "#374151",
                    margin: "0 0 8px"
                }}
            >
                No systems registered yet
            </h3>

            <p
                style={{
                    fontSize: "14px",
                    color: "#6b7280",
                    maxWidth: "400px",
                    lineHeight: "1.6",
                    margin: 0
                }}
            >
                Your dashboard is currently empty. Once an agent
                registers a system with the AM server, it will
                appear here automatically.
            </p>
        </div>
    );
}

export default EmptyState;
