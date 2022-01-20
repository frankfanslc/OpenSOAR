export async function get(request) {
    let installationStatus = await fetch(`http://webserver-backend.default.svc.cluster.local/install`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(r => r.json())
    return {
        body: installationStatus
    }
}