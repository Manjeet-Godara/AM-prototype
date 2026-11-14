function DataTable({ columns, data }) {

    return (
        <div style={{
            width: "100%",
            overflowX: "auto",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            backgroundColor: "white"
        }}>

            <table style={{
                width: "100%",
                borderCollapse: "collapse",
                textAlign: "left"
            }}>

                <thead>
                    <tr style={{ backgroundColor: "#f1f5f9" }}>

                        {columns.map((column) => (
                            <th
                                key={column.key}
                                style={{
                                    padding: "13px 16px",
                                    fontSize: "13px",
                                    color: "#475569",
                                    borderBottom: "1px solid #e2e8f0"
                                }}
                            >
                                {column.label}
                            </th>
                        ))}

                    </tr>
                </thead>

                <tbody>

                    {data.length === 0 ? (
                        <tr>
                            <td
                                colSpan={columns.length}
                                style={{
                                    padding: "24px",
                                    textAlign: "center",
                                    color: "#64748b"
                                }}
                            >
                                No records found
                            </td>
                        </tr>
                    ) : (

                        data.map((row, index) => (
                            <tr key={row.id ?? index}>

                                {columns.map((column) => (
                                    <td
                                        key={column.key}
                                        style={{
                                            padding: "13px 16px",
                                            fontSize: "14px",
                                            borderBottom: "1px solid #e2e8f0"
                                        }}
                                    >
                                        {column.render
                                            ? column.render(row)
                                            : row[column.key]
                                        }
                                    </td>
                                ))}

                            </tr>
                        ))

                    )}

                </tbody>

            </table>

        </div>
    );
}

export default DataTable;