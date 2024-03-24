export const MatchesAPI = {
    _judges_cache: [],
    list: async function (tournament_id) {
        let r = await fetch("/api/admin/matches/list?tournament_id=" + tournament_id);
        let data = await r.json()
        if (r.status == 200) return data;
        else throw data.detail;
    },
    get: async function (match_id) {
        let r = await fetch("/api/admin/matches/get?match_id=" + match_id);
        let data = await r.json();
        if (r.status == 200) return data;
        else throw data.detail;
    },
    score: async function (match_id, team_1, team_2) {
        let r = await fetch("/api/admin/matches/score", {
            method: "POST",
            body: JSON.stringify({
                id: match_id,
                team_1: team_1,
                team_2: team_2,
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        if (r.status == 400) {
            let data = await r.json();
            throw data.detail;
        }
    },
    list_judge: async function () {
        let r = await fetch("/api/admin/matches/list_judge");
        let data = await r.json();
        if (r.status == 200) return data;
        else throw data.detail;
    },
    judges: async function () {
        if (MatchesAPI._judges_cache.length > 0) return MatchesAPI._judges_cache;
        let r = await fetch("/api/admin/matches/judges");
        let data = await r.json();
        if (r.status == 200) {
            MatchesAPI._judges_cache = data;
            return data;
        }
        else throw data.detail;
    },
    edit: async function (match_id, judge_id, time) {
        if (time == "") time = null;
        let r = await fetch("/api/admin/matches/edit", {
            method: "POST",
            body: JSON.stringify({
                id: match_id,
                judge_id: judge_id,
                start: time,
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        if (r.status == 400) {
            let data = await r.json();
            throw data.detail;
        }
    },
    end: async function (match_id) {
        let r = await fetch("/api/admin/matches/end", {
            method: "POST",
            body: JSON.stringify({
                id: match_id
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        if (r.status == 400) {
            let data = await r.json();
            throw data.detail;
        }
    }
}