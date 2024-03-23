import { TournamentsAPI } from "/static/js/api/tournaments_api.js";


async function set_tournament_info(tournament_id) {
    let tournament = await TournamentsAPI.get(tournament_id);

    let name = document.createElement("h3");
    name.classList.add("card-title");
    name.textContent = tournament.name;

    let start_date = document.createElement("p");
    start_date.classList.add("card-text");
    start_date.textContent = "Начало: " +
        TournamentsAPI.transform_time(tournament.start_date);

    let end_date = document.createElement("p");
    end_date.classList.add("card-text");
    end_date.textContent = "Конец: " +
        TournamentsAPI.transform_time(tournament.end_date);

    let id = document.createElement("p");
    id.classList.add("card-text");
    id.textContent = "ID: " + tournament.id;

    let container = document.querySelector("#tournament_info");
    container.appendChild(name);
    container.appendChild(start_date);
    container.appendChild(end_date);
    container.appendChild(id);
}


window.addEventListener("load", async function () {
    let query = window.location.pathname.split("/");
    let tournament_id = +query[query.length - 1];
    await set_tournament_info(tournament_id);
});
