<script>
    let status;
    async function submit(event) {
        let jsonData = {};
        let data = new FormData(event.target);
        data.forEach((value, key) => jsonData[key] = value);
        if (jsonData["new_password"] === jsonData["confirm_password"]) {
            const response = await fetch(`/profile/me`, {
                method: 'PATCH',
                credentials: 'include',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({password: jsonData["new_password"]}),
            }).then(r => {status = r.ok; document.getElementById("change_password").reset()});
        } else {
            alert("Passwords do not match. Please try again.")
        }
    }
</script>

<div class="columns is-centered">
    <div class="column is-5-tablet is-4-desktop is-3-widescreen">
        <div class="box">
            <form id="change_password" on:submit|preventDefault={submit}>
                <div class="field">
                    <label for="new_password" class="label">New Password</label>
                    <input type="password" id="new_password" class="input" name="new_password"
                           required>
                </div>
                <div class="field">
                    <label for="confirm_password" class="label">Confirm Password</label>
                    <input type="password" id="confirm_password" class="input"
                           name="confirm_password" required>
                </div>
                {#if status === true}
                    <p class="help is-success block">New password set</p>
                {:else if status === false}
                    <p class="help is-danger block">Failed to set new password</p>
                {/if}
                <div class="field">
                    <button type="submit" class="button is-success">
                        Submit
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>