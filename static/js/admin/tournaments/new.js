import { CitiesAPI } from "/static/js/api/cities_api.js";
import { TournamentsAPI } from "/static/js/api/tournaments_api.js";


async function new_tournament() {
    let form = document.querySelector("#new_tournament");
    let tournament = null;
    console.log(form.elements["start_date"].value);
    try {
        tournament = await TournamentsAPI.create(
            form.elements["name"].value,
            +form.elements["city_id"].value,
            new Date(form.elements["start_date"].value),
            new Date(form.elements["end_date"].value),
        )
    } catch (e) {
        document.querySelector("#invalid_data").textContent = e;
    }
    if (tournament !== null) {
        window.location.href = "/admin/tournaments/" + tournament.id;
    }
}


window.addEventListener("load", async function () {
    let city_select = document.querySelector("#city_id");
    let cities = await CitiesAPI.fetch();
    for (let i in cities) {
        let option = document.createElement("option");
        option.value = cities[i].id;
        option.textContent = cities[i].name;
        city_select.appendChild(option);
    }
    document.querySelector('#new_tournament').addEventListener('submit', new_tournament);
});
