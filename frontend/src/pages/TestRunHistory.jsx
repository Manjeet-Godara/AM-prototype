import { useParams } from "react-router-dom";

function TestRunHistory() {

    const { testId } = useParams();

    return (
        <div>
            <h1>Test Run History</h1>
            <p>Test ID: {testId}</p>
        </div>
    );
}

export default TestRunHistory;