export const RequestsAPI = {
    users: {},
    fetch: async function () {
        if (Object.keys(RequestsAPI.users).length > 0) return RequestsAPI.users;
        let r = await fetch("/api/admin/requests/list");
        let data = await r.json();
        if (r.status == 200) {
            for (let i of data) RequestsAPI.users[i.id] = i;
            return RequestsAPI.users;
        }
        else throw data.detail;
    },
    process: async function (user_id, confirmed) {
        let r = await fetch("/api/admin/requests/process", {
            method: "POST",
            body: JSON.stringify({ user_id: user_id, confirmed: confirmed }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        if (r.status == 400) {
            let data = await r.json();
            throw data.detail;
        }
    }
}
