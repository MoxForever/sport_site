import { TournamentsAPI } from "/static/js/api/tournaments_api.js";


window.addEventListener("load", async function () {
    let query = window.location.pathname.split("/");
    let tournament = await TournamentsAPI.get(query[query.length - 1]);

    let name = document.createElement("h3");
    name.classList.add("card-title");
    name.textContent = tournament.name;

    let city = document.createElement("p");
    city.classList.add("card-text");
    city.textContent = "Город: " + tournament.city.name;

    let start_date = document.createElement("p");
    start_date.classList.add("card-text");
    start_date.textContent = "Начало: " + tournament.start_date;

    let end_date = document.createElement("p");
    end_date.classList.add("card-text");
    end_date.textContent = "Конец: " + tournament.end_date;
    
    let id = document.createElement("p");
    id.classList.add("card-text");
    id.textContent = "ID: " + tournament.id;
    
    let container = document.querySelector("#tournament_info");
    container.appendChild(name);
    container.appendChild(city);
    container.appendChild(start_date);
    container.appendChild(end_date);
    container.appendChild(id);
})