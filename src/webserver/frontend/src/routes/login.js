export async function post(request) {
    let credentials = request.body;
    let headers = request.headers;
    headers["content-type"] = "application/x-www-form-urlencoded"
    if (!request.locals.jwt) {
        const body = await fetch('http://webserver-backend.default.svc.cluster.local/auth/jwt/login', {
            method: 'POST',
            credentials: 'include',
            headers: headers,
            body: `username=${encodeURIComponent(credentials.username)}&password=${encodeURIComponent(credentials.password)}`
        }).then((r) => r.json());
        if (!body.access_token) {
            return {status: 400, body};
        }
        headers['Authorization'] = `Bearer ${body.access_token}`
        const user = await fetch('http://webserver-backend.default.svc.cluster.local/users/me', {
            method: 'GET',
            credentials: 'include',
            headers: headers
        }).then((r) => r.json());
        delete user.incidents;
        let user_cookie = btoa(JSON.stringify(user));
        return {
            headers: {
                'set-cookie': [
                    `jwt=${body.access_token}; HttpOnly; Max-Age=3600; Path=/; SameSite=lax; Secure`,
                    `opensoar_user=${user_cookie}; Max-Age=3600; Path=/; SameSite=lax; Secure`
                ]
            },
            body: {
                "user": user,
                "jwt": body.access_token
            }
        }
    }
    return {};
}
