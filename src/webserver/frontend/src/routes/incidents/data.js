export async function get(request) {
    const backend = "http://webserver-backend.default.svc.cluster.local"
    let headers = request.headers
    const data = await fetch(`${backend}/incidents?${request.query.toString()}`, {
        method: 'GET',
        credentials: 'include',
        headers: headers
    }).then((r) => r.json())
    return {
        body: data
    }
}