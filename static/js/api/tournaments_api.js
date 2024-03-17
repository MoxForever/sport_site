import { CitiesAPI } from "/static/js/api/cities_api.js"


export const TournamentsAPI = {
    _format_model: async function (data) {
        return {
            id: data.id,
            name: data.name,
            city: (await CitiesAPI.fetch())[data.city_id],
            start_date: new Date(data.start_date),
            end_date: new Date(data.end_date),
        }
    },
    fetch: async function () {
        let r = await fetch("/api/admin/tournaments/list");
        let data = await r.json();

        let tournaments = [];
        for (let i of data) {
            tournaments.push(await TournamentsAPI._format_model(i));
        }

        return tournaments;
    },
    get: async function (id) {
        let r = await fetch("/api/admin/tournaments/get?id=" + id);
        let data = await r.json();

        if (r.status == 200) {
            return await TournamentsAPI._format_model(data);
        }
        else throw data.detail;
    },
    create: async function (name, city_id, start_date, end_date) {
        function transform_time(date) {
            let day = String(date.getDate()).padStart(2, '0');
            let month = String(date.getMonth() + 1).padStart(2, '0');
            let year = String(date.getFullYear());

            return `${year}-${month}-${day}`;
        }
        let r = await fetch("/api/admin/tournaments/create", {
            method: "POST",
            body: JSON.stringify({
                name: name,
                city_id: city_id,
                start_date: transform_time(start_date),
                end_date: transform_time(end_date),
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        let data = await r.json();

        if (r.status == 200) {
            return await TournamentsAPI._format_model(data);
        }
        else throw data.detail;
    }
}