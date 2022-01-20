<script>
    import {session} from '$app/stores';
    import {browser} from '$app/env';
    import {goto} from "$app/navigation";

    if (browser) {
        if ($session.jwt) {
            goto('/incidents');
        }
        fetch('/install/status', {
            method: 'GET',
            credentials: 'include',
            headers: {
                "Content-Type": "application/json"
            }
        })
            .then(r => r.json())
            .then(d => {
                if (!d.status) {
                    goto("/install")
                }
            });
    }

    let badLogin = false;

    async function submit(event) {
        let jsonData = {};
        let data = new FormData(event.target);
        data.forEach((value, key) => jsonData[key] = value);
        const response = await fetch(`/login`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jsonData),
        }).then((r) => r.ok ? r.json() : (badLogin = true));
        $session.user = response.user;
        $session.jwt = response.jwt;
        goto('/incidents');
    }
</script>

<div class="container has-text-centered">
    <img alt="OpenSOAR logo" src="/opensoar_logo.png" width="600"/>
</div>
<section class="is-fullheight">
    <div class="hero-body">
        <div class="container">
            <div class="columns is-centered">
                <div class="column is-5-tablet is-4-desktop is-3-widescreen">
                    <form on:submit|preventDefault={submit}>
                        <div class="field">
                            <label for="email" class="label">Email</label>
                            <div class="control">
                                <input type="text"
                                       id="email" class="input" name="email" required>
                            </div>
                        </div>
                        <div class="field">
                            <label for="password" class="label">Password</label>
                            <div class="control">
                                <input type="password" id="password" class="input" name="password" required>
                            </div>
                        </div>
                        {#if badLogin}
                            <p class="help is-danger block">Bad username or password</p>
                        {/if}
                        <div class="field">
                            <button type="submit" class="button is-success">
                                Login
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</section>