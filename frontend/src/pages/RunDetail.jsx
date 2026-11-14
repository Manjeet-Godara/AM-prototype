import { useParams } from "react-router-dom";

function RunDetail() {

    const { runId } = useParams();

    return (
        <div>
            <h1>Run Details</h1>
            <p>Run ID: {runId}</p>
        </div>
    );
}

export default RunDetail;