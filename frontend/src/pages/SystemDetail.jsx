import { useParams } from "react-router-dom";

function SystemDetail() {

    const { systemId } = useParams();

    return (
        <div>
            <h1>System Details</h1>
            <p>System ID: {systemId}</p>
        </div>
    );
}

export default SystemDetail;