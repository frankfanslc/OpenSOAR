import * as cookie from 'cookie';

export async function handle({request, resolve}) {
    const publicPages = ['/', '/login'];

    const cookies = cookie.parse(request.headers.cookie || '');
    const jwt = cookies.jwt;
    const user = cookies.opensoar_user && Buffer.from(cookies.opensoar_user, "base64").toString("utf-8")
    request.locals.jwt = jwt ? jwt : false;
    request.locals.user = user ? JSON.parse(user) : null;
    if (!request.locals.jwt && !publicPages.includes(request.path)) {
        return {
            status: 301,
            headers: {
                location: '/'
            }
        };
    }
    return await resolve(request);
}

export async function getSession({ locals }) {
    return {
        user: locals.user,
        jwt: locals.jwt
    }
}