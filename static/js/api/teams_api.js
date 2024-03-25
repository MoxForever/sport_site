export const TeamsAPI = {
    _candidates_cache: [],
    candidates: async function () {
        if (TeamsAPI._candidates_cache.length > 0) return TeamsAPI._candidates_cache;
        let r = await fetch("/api/admin/teams/candidates");
        let data = await r.json();

        if (r.status == 200) {
            TeamsAPI._candidates_cache = data;
            return data;
        }
        else throw data.detail;
    },
    list: async function (tournament_id) {
        let r = await fetch("/api/admin/teams/list?tournament_id=" + tournament_id);
        let data = await r.json();

        if (r.status == 200) return data;
        else throw data.detail;
    },
    create: async function (tournament_id, user_1_id, user_2_id) {
        let r = await fetch("/api/admin/teams/create", {
            method: "POST",
            body: JSON.stringify({
                tournament_id: tournament_id,
                user_1_id: user_1_id,
                user_2_id: user_2_id
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        let data = await r.json();

        if (r.status == 200) return data;
        else throw data.detail;
    },
    edit: async function (id, user_1_id, user_2_id) {
        let r = await fetch("/api/admin/teams/edit", {
            method: "POST",
            body: JSON.stringify({
                id: id,
                user_1_id: user_1_id,
                user_2_id: user_2_id
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        let data = await r.json();

        if (r.status == 200) return data;
        else throw data.detail;
    },
    delete: async function (id) {
        let r = await fetch("/api/admin/teams/delete", {
            method: "POST",
            body: JSON.stringify({ id: id }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });

        if (r.status == 200) return;
        else {
            let data = await r.json();
            throw data.detail;
        }
    }
}
