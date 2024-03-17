export const CitiesAPI = {
    delete: async function (id) {
        let r = await fetch("/api/admin/cities/delete", {
            method: "POST",
            body: JSON.stringify({ id: id }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        if (r.status == 200) {
            let cities = JSON.parse(sessionStorage.getItem("cities"));
            delete cities[id];
            sessionStorage.setItem("cities", JSON.stringify(cities));
        }
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
        if (r.status == 200) {
            let cities = JSON.parse(sessionStorage.getItem("cities"));
            cities[data.id] = data;
            sessionStorage.setItem("cities", JSON.stringify(cities));
        }
        else throw data.detail;
    },
    fetch: async function () {
        let buffered = sessionStorage.getItem("cities");
        if (buffered !== null) {
            return JSON.parse(buffered);
        }

        let r = await fetch("/api/data/cities");
        let data = await r.json();

        let cities = {};
        if (r.status == 200) {
            for (let i of data) cities[i.id] = i;
            sessionStorage.setItem("cities", JSON.stringify(cities));
            return cities;
        }
        else throw data.detail;
    }
}
