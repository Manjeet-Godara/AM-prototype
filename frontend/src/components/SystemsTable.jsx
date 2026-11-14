
import { useNavigate } from "react-router-dom";
import StatusBadge from "./StatusBadge";

function SystemsTable({ systems }) {

    const navigate = useNavigate();

    if (!systems || systems.length === 0) {
        return null;
    }

    return (
        <div style={{
            width: "100%",
            overflowX: "auto"
        }}>
            <table style={{
                width: "100%",
                borderCollapse: "collapse",
                textAlign: "left",
                minWidth: "850px"
            }}>

                <thead>
                    <tr style={{
                        borderBottom: "1px solid #e5e7eb",
                        backgroundColor: "#f9fafb"
                    }}>
                        <th style={thStyle}>System</th>
                        <th style={thStyle}>Environment</th>
                        <th style={thStyle}>Agents</th>
                        <th style={thStyle}>Tests</th>
                        <th style={thStyle}>Last Seen</th>
                        <th style={thStyle}>Latest Outcome</th>
                    </tr>
                </thead>

                <tbody>
                    {systems.map((system) => (

                        <tr
                            key={system.id}
                            onClick={() => navigate(`/systems/${system.id}`)}
                            style={{
                                borderBottom: "1px solid #e5e7eb",
                                cursor: "pointer"
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.backgroundColor = "#f9fafb";
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.backgroundColor = "transparent";
                            }}
                        >

                            {/* System slug */}
                            <td style={tdStyle}>
                                <strong>{system.system_slug}</strong>
                            </td>

                            {/* Environment */}
                            <td style={tdStyle}>
                                {system.environment}
                            </td>

                            {/* Agent IDs */}
                            <td style={tdStyle}>
                                <div style={{
                                    display: "flex",
                                    flexWrap: "wrap",
                                    gap: "5px"
                                }}>
                                    {system.agent_ids?.length > 0 ? (
                                        system.agent_ids.map((agentId) => (
                                            <span
                                                key={agentId}
                                                style={{
                                                    backgroundColor: "#f3f4f6",
                                                    padding: "3px 7px",
                                                    borderRadius: "4px",
                                                    fontSize: "12px"
                                                }}
                                            >
                                                {agentId}
                                            </span>
                                        ))
                                    ) : (
                                        <span>-</span>
                                    )}
                                </div>
                            </td>

                            {/* Test count */}
                            <td style={tdStyle}>
                                {system.test_count}
                            </td>

                            {/* Last seen */}
                            <td style={tdStyle}>
                                {system.last_seen_at
                                    ? new Date(system.last_seen_at).toLocaleString()
                                    : "Never"
                                }
                            </td>

                            {/* Latest outcome */}
                            <td style={tdStyle}>
                                <StatusBadge
                                    outcome={system.latest_run_outcome}
                                />
                            </td>

                        </tr>
                    ))}
                </tbody>

            </table>
        </div>
    );
}

const thStyle = {
    padding: "14px 16px",
    fontSize: "13px",
    fontWeight: "600",
    color: "#6b7280",
    whiteSpace: "nowrap"
};

const tdStyle = {
    padding: "16px",
    fontSize: "14px",
    color: "#374151"
};

export default SystemsTable;
