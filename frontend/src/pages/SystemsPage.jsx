import { usePolling } from "../hooks/usePolling";
import SystemsTable from "../components/SystemsTable";
import EmptyState from "../components/EmptyState";

function SystemsPage() {
    const {
        data,
        loading,
        error,
        lastUpdated,
        refetch
    } = usePolling("/systems/", 5000);

    const systems = data?.systems ?? [];

    if (loading) {
        return (
            <main className="page-container">
                <p>Loading systems...</p>
            </main>
        );
    }

    if (error && !data) {
        return (
            <main className="page-container">
                <div className="error-container">
                    <p>Unable to load systems: {error}</p>
                    <button onClick={refetch}>Retry</button>
                </div>
            </main>
        );
    }

    return (
        <main className="page-container">

            <div className="page-header">
                <div>
                    <h1>Systems</h1>
                    <p>Monitor all your registered systems and their health.</p>
                </div>

                <div className="last-updated">
                    <span className="live-indicator"></span>
                    Last updated: {lastUpdated?.toLocaleTimeString() || "—"}
                </div>
            </div>

            {error && (
                <p className="refresh-warning">
                    Unable to refresh data. Showing the last available results.
                </p>
            )}

            {systems.length === 0 ? (
                <EmptyState />
            ) : (
                <div className="table-container">
                    <SystemsTable systems={systems} />
                </div>
            )}

        </main>
    );
}

export default SystemsPage;