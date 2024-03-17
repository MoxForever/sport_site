export const CitiesAPI = {
    cities: {},
    delete: async function (id) {
        let r = await fetch("/api/admin/cities/delete", {
            method: "POST",
            body: JSON.stringify({ id: id }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        if (r.status == 200) delete CitiesAPI.cities[id];
        else {
            let data = await r.json();
            throw data.detail;
        }
    },
    add: async function (name) {
        let r = await fetch("/api/admin/cities/create", {
            method: "POST",
            body: JSON.stringify({ name: name }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        let data = await r.json();
        if (r.status == 200) CitiesAPI.cities[data.id] = data;
        else throw data.detail;
    },
    fetch: async function () {
        if (Object.keys(CitiesAPI.cities).length > 0) return CitiesAPI.cities;
        let r = await fetch("/api/data/cities");
        let data = await r.json();
        if (r.status == 200) {
            for (let i of data) CitiesAPI.cities[i.id] = i;
            return CitiesAPI.cities;
        }
        else throw data.detail;
    }
}
