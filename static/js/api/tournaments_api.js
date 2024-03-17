import { CitiesAPI } from "/static/js/api/cities_api.js"


export const TournamentsAPI = {
    fetch: async function () {
        let r = await fetch("/api/admin/tournaments/list");
        let data = await r.json();

        let tournaments = [];
        for (let i of data) {
            tournaments.push({
                id: i.id,
                name: i.name,
                city: (await CitiesAPI.fetch())[i.city_id],
                start_date: new Date(i.start_date),
                end_date: new Date(i.end_date),
            })
        }

        return tournaments;
    },
    get: async function (id) {
        let r = await fetch("/api/admin/tournaments/get?id=" + id);
        let data = await r.json();

        if (r.status == 200) return {
            id: data.id,
            name: data.name,
            city: (await CitiesAPI.fetch())[data.city_id],
            start_date: new Date(data.start_date),
            end_date: new Date(data.end_date),
        }
        else throw data.detail;
    }
}