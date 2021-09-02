import * as cookie from 'cookie';

export async function handle({request, resolve}) {
    const cookies = cookie.parse(request.headers.cookie || '');
    const jwt = cookies.jwt;
    // todo: create a server side check that the user/token are still valid
    const user = cookies.opensoar_user && Buffer.from(cookies.opensoar_user, "base64").toString("utf-8")
    request.locals.jwt = jwt ? jwt : false;
    if (request.locals.jwt) {
        request.headers['Authorization'] = `Bearer ${jwt}`
    }
    request.locals.user = user ? JSON.parse(user) : null;
    return await resolve(request);
}

export async function getSession({ locals }) {
    return {
        user: locals.user,
        jwt: locals.jwt
    }
}