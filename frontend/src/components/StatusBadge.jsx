
function StatusBadge({ outcome }) {

    const normalizedOutcome = {
        "test passed": "passed",
        "test failed": "failed",
        "test errored": "errored",
        "no result": "none"
    };

    const statusStyles = {
        passed: {
            label: "Passed",
            background: "#dcfce7",
            color: "#166534"
        },

        failed: {
            label: "Failed",
            background: "#fee2e2",
            color: "#991b1b"
        },

        errored: {
            label: "Errored",
            background: "#ffedd5",
            color: "#9a3412"
        },

        none: {
            label: "No Result",
            background: "#e5e7eb",
            color: "#374151"
        }
    };

    const key = normalizedOutcome[outcome] || outcome;
    const status = statusStyles[key] || statusStyles.none;

    return (
        <span
            style={{
                backgroundColor: status.background,
                color: status.color,
                padding: "5px 10px",
                borderRadius: "6px",
                fontSize: "13px",
                fontWeight: "600",
                display: "inline-block"
            }}
        >
            {status.label}
        </span>
    );
}

export default StatusBadge;
