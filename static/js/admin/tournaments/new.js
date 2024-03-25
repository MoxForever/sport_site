import { TournamentsAPI } from "/static/js/api/tournaments_api.js";


async function new_tournament() {
    let form = document.querySelector("#new_tournament");
    let tournament = null;
    try {
        tournament = await TournamentsAPI.create(
            form.elements["name"].value,
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
    document.querySelector('#new_tournament').addEventListener('submit', new_tournament);
});
