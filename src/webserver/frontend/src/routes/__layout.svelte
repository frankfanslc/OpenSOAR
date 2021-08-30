<script context="module">
    const publicPages = ['/', '/login'];

    export async function load({page, session}) {
        const {path} = page;

        if (publicPages.includes(path)) {
            return {};
        }

        if (!session.jwt) {
            return {
                status: 301,
                redirect: '/'
            };
        }

        return {};
    }
</script>
<script>
    import {session} from '$app/stores';

</script>

{#if $session.user}
    <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="/">
                <img alt="OpenSOAR logo" src="/opensoar_logo.png"/>
            </a>
        </div>

        <div id="navbarPrimary" class="navbar-menu">
            <div class="navbar-start">
                <a class="navbar-item" href="/incidents">
                    Incidents
                </a>
                {#if $session.user.is_superuser}
                    <a class="navbar-item" href="/settings">
                        Settings
                    </a>
                {/if}
            </div>

            <div class="navbar-end">
                <div class="navbar-item">
                    <div class="buttons">
                        <a href="/logout" class="button is-light">
                            Log out
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </nav>
{/if}

<slot></slot>