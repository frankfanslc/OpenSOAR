const backend = "http://webserver-backend.default.svc.cluster.local"

export async function get(request) {
    let headers = request.headers
    const data = await fetch(`${backend}/users?${request.query.toString()}`, {
        method: 'GET',
        credentials: 'include',
        headers: headers
    }).then((r) => r.json())
    return {
        body: data
    }
}

export async function patch(request) {
    let headers = request.headers;
    let body = request.body;
    const response = await fetch(`${backend}/users/${body.user_id}`, {
        method: 'PATCH',
        credentials: 'include',
        headers: headers,
        body: JSON.stringify(body.updated_user)
    })
    return {
        "status": response.status
    }
}

export async function del(request) {
    let headers = request.headers;
    let body = request.body;
    const response = await fetch(`${backend}/users/${body.user_id}`, {
        method: 'DELETE',
        credentials: 'include',
        headers: headers
    })
    return {
        "status": response.status
    }
}

export async function post(request) {
    let headers = request.headers;
    let body = request.body;
    let crypto = require("crypto");
    let password = crypto.randomBytes(20).toString('hex');
    body.password = password;
    await fetch(`${backend}/auth/register`, {
        method: 'POST',
        credentials: 'include',
        headers: headers,
        body: JSON.stringify(body)
    })
    return {
        "body": password
    }
}