<script>
    import {browser} from "$app/env";

    let currentPage = 0;
    let skip = 0;
    let limit = 10;
    let selection = [];
    let total = 1;
    let maxPage = 1;
    let pages = [0];
    let creatingUser = false;

    let user_data = [];

    async function getUsers(params) {
        if (browser) {
            let urlParams = new URLSearchParams(params).toString();
            const data = await fetch(`/settings/users?${urlParams}`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            user_data = await data.json();
        }
    }

    async function modifyUser(event) {
        console.log(event);
        let checked = event.target.checked;
        let user_id = event.target.value;
        let field = event.target.name;
        await fetch(`/settings/users`, {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'user_id': user_id, 'updated_user': {[field]: checked}})
        })
        await getUsers();
    }

    async function deleteUsers(event) {
        if (confirm("Please confirm user deletion")) {
            selection.forEach((async value => {
                await fetch(`/settings/users`, {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"user_id": value})
                })
            }))
            selection = [];
            await getUsers();
        }
    }

    async function changePage(event) {
        user_data = {"incidents": [], "total": 0};
        let newPage;
        switch (event.target.innerHTML) {
            case "Previous":
                newPage = currentPage - 1;
                break;
            case "Next":
                newPage = currentPage + 1;
                break;
            default:
                newPage = parseInt(event.target.innerHTML) - 1;
        }
        currentPage = newPage;
        skip = newPage * limit;
        document.getElementById('allSelector').checked = false;
    }

    async function changeLimit(event) {
        limit = parseInt(event.target.innerHTML);
        if (currentPage > (total / limit >> 0)) {
            await changePage({'target': {'innerHTML': "1"}})
        }
    }

    async function toggleSelectAll(event) {
        let checkboxes = document.getElementsByName('row');
        for (let i = 0, n = checkboxes.length; i < n; i++) {
            let checkValue = checkboxes[i].value
            if (event.target.checked) {
                if (!selection.includes(checkValue)) {
                    selection.push(checkValue);
                }
            } else {
                selection = selection.filter(id => id !== checkValue);
            }
        }
        selection.sort((a, b) => (a - b));
        selection = selection;
    }

    async function addUser() {
        let displayName = document.getElementById("newUserDisplayName").value;
        let email = document.getElementById("newUserEmail").value;
        let newUser = {
            "display_name": displayName,
            "email": email
        }
        const password = await fetch(`/settings/users`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newUser)
        }).then(r => r.text())
        alert(`Temporary password: ${password}`)
        await getUsers();
        creatingUser = false;
    }

    getUsers();

    $: adminCount = user_data.filter(user => user.is_superuser).length
    $: adminsSelected = user_data.filter(user => user.is_superuser && selection.includes(user.id)).length
</script>

<div class="columns is-centered">
    <div class="column">
        <div class="box has-background-light">
            <div class="is-pulled-right columns" style="padding: 1.25em;">
                <button class="button is-small" on:click={changeLimit}>10</button>
                <button class="button is-small" on:click={changeLimit}>25</button>
                <button class="button is-small" on:click={changeLimit}>50</button>
                <button class="button is-small" on:click={changeLimit}>100</button>
            </div>
            <table class="table has-background-light">
                <thead>
                <tr>
                    <th class="has-text-centered"><input type="checkbox" id="allSelector"
                                                         on:click={toggleSelectAll}></th>
                    <th>Display Name</th>
                    <th>Email</th>
                    <th>Active</th>
                    <th>Admin</th>
                    <th class="is-hidden">ID</th>
                </tr>
                </thead>
                <tbody>
                {#if user_data}
                    {#each user_data as user}
                        <tr class='{selection.includes(user.id) ? "is-selected" : ""}'>
                            <td class="has-text-centered"><input type="checkbox" name="row"
                                                                 value="{user.id}"
                                                                 bind:group={selection}></td>
                            <td>{user.display_name ? user.display_name : user.email}</td>
                            <td>{user.email}</td>
                            <td><input type="checkbox" name="is_active" value="{user.id}"
                                       bind:checked={user.is_active} on:click={modifyUser}></td>
                            <td><input type="checkbox" name="is_superuser" value="{user.id}"
                                       bind:checked={user.is_superuser} on:click={modifyUser}></td>
                            <td class="is-hidden">{user.id}</td>
                        </tr>
                    {/each}
                {/if}
                {#if creatingUser}
                    <tr>
                        <td>
                            <button class="button has-background-light is-normal" style="border-width: 0" on:click={() => creatingUser = false}>
                                <span class="icon has-text-danger">
                                    <i class="fas fa-times-circle"></i>
                                </span>
                            </button>
                        </td>
                        <td>
                            <input type="text" id="newUserDisplayName" class="input is-normal">
                        </td>
                        <td>
                            <input type="text" id="newUserEmail" class="input is-normal">
                        </td>
                        <td></td>
                        <td></td>
                        <td>
                            <input type="button" value="Submit" class="button input is-normal is-success" on:click={addUser}>
                        </td>
                    </tr>
                {/if}
                {#if selection.length === 0 && !creatingUser}
                    <button class="button has-background-light" style="border-width: 0" on:click={() => creatingUser = true}>
                        <span class="icon has-text-success">
                            <i class="fas fa-plus-circle"></i>
                        </span>
                    </button>
                {/if}
                </tbody>
            </table>
            {#if selection.length > 0}
                {#if adminCount - adminsSelected === 0}
                    <button class="button is-danger" title="Cannot delete all admins" disabled>
                        Delete
                    </button>
                {:else}
                    <button class="button is-danger" on:click={deleteUsers}>
                        Delete
                    </button>
                {/if}
            {/if}
        </div>
        <nav class="pagination" role="navigation" aria-label="pagination">
            {#if (currentPage === 0)}
                <button class="button pagination-previous has-background-white"
                        disabled>Previous
                </button>
            {:else}
                <button class="button pagination-previous has-background-white"
                        on:click={changePage}>Previous
                </button>
            {/if}
            {#if (currentPage === maxPage)}
                <button class="button pagination-next has-background-white"
                        disabled>Next
                </button>
            {:else}
                <button class="button pagination-next has-background-white"
                        on:click={changePage}>Next
                </button>
            {/if}
            <ul class="pagination-list">
                {#each pages as page}
                    {#if (page === currentPage)}
                        <li>
                            <button class="button pagination-link is-current"
                                    aria-label="Page {page+1}" aria-current="page"
                                    on:click={changePage}>{page + 1}</button>
                        </li>
                    {:else}
                        <li>
                            <button class="button pagination-link has-background-white"
                                    aria-label="Goto page {page+1}"
                                    on:click={changePage}>{page + 1}</button>
                        </li>
                    {/if}
                {/each}
            </ul>
        </nav>
    </div>
</div>