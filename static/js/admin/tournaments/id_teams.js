import { TeamsAPI } from "/static/js/api/teams_api.js";


async function getUserSelect(user_selected_id = null) {
    let users = await TeamsAPI.candidates();

    let select = document.createElement("select");
    select.classList.add("form-control");

    if (user_selected_id === null) {
        let option = document.createElement("option");
        option.selected = true;
        option.disabled = true;
        option.hidden = true;
        option.textContent = "...";
        option.value = "null";
        select.appendChild(option);
    }

    for (let i of users) {
        let option = document.createElement("option");
        option.textContent = i.fio;
        option.value = i.id;
        option.selected = (user_selected_id == i.id);
        select.appendChild(option);
    }
    return select;
}


async function deleteTeamCard(element) {
    let id = element.getAttribute('data-id');
    if (id !== null) await TeamsAPI.delete(+id);
    element.remove();
}


async function editTeamCard(element, tournament_id) {
    let user_1_id = element.querySelector("#user_1").value;
    let user_2_id = element.querySelector("#user_2").value;

    if (user_1_id == "null" || user_2_id == "null") return;
    else {
        user_1_id = +user_1_id;
        user_2_id = +user_2_id;
    }

    let id = element.getAttribute('data-id');
    if (id !== null) id = +id;

    if (id === null) {
        let team = await TeamsAPI.create(tournament_id, user_1_id, user_2_id);
        element.querySelector("#card_title").textContent = "Команда #" + team.id;
        element.setAttribute('data-id', team.id);
    }
    else await TeamsAPI.edit(id, user_1_id, user_2_id);
}


async function createTeamCard(tournament_id, id = null, user_1_id, user_2_id) {
    let card = document.createElement("div");
    card.classList.add("card");
    if (id !== null) card.setAttribute("data-id", id);
    card.setAttribute("data-tournament-id", tournament_id);

    let body = document.createElement("div");
    body.classList.add("card-body");

    let title = document.createElement("h5");
    if (id === null) title.textContent = "Новая команда";
    else title.textContent = "Команда #" + id;
    title.classList.add("card-title");
    title.id = "card_title";

    let form = document.createElement("form");

    let user_1_label = document.createElement("label");
    let user_1_select = await getUserSelect(user_1_id);
    user_1_label.htmlFor = "user_1";
    user_1_label.textContent = "Участник 1";
    user_1_select.id = "user_1";
    user_1_select.onchange = async _ => await editTeamCard(card, tournament_id);

    let user_2_label = document.createElement("label");
    let user_2_select = await getUserSelect(user_2_id);
    user_2_label.htmlFor = "user_2";
    user_2_label.textContent = "Участник 2";
    user_2_select.id = "user_2";
    user_2_select.onchange = async _ => await editTeamCard(card, tournament_id);

    let delete_btn = document.createElement("button")
    delete_btn.classList.add("btn", "btn-danger", "mt-2");
    delete_btn.textContent = "Удалить";
    delete_btn.onclick = async _ => await deleteTeamCard(card,);

    form.appendChild(user_1_label);
    form.appendChild(user_1_select);
    form.appendChild(user_2_label);
    form.appendChild(user_2_select);
    body.appendChild(title);
    body.appendChild(form);
    body.appendChild(delete_btn);
    card.appendChild(body);

    return card;
}

window.addEventListener("load", async function () {
    let query = window.location.pathname.split("/");
    let tournament_id = +query[query.length - 1];
    let teams_cards = document.querySelector("#teams_cards");

    for (let i of await TeamsAPI.list(tournament_id)) {
        teams_cards.appendChild(await createTeamCard(
            tournament_id, i.id, i.user_1_id, i.user_2_id));
    }

    document.querySelector("#new_btn").addEventListener("click", async function () {
        teams_cards.appendChild(await createTeamCard(tournament_id));
    });
});
