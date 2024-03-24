import { TeamsAPI } from "/static/js/api/teams_api.js";
import { MatchesAPI } from "/static/js/api/matches_api.js";


async function getJudgeSelect(user_selected_id = null) {
    let users = await MatchesAPI.judges();

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

async function editMatchCard(element, match_id) {
    await MatchesAPI.edit(
        match_id, 
        +element.querySelector("#judge").value,
        element.querySelector("#time").value
    );
}


async function createTeamCard(match) {
    let card = document.createElement("div");
    card.classList.add("card");

    let body = document.createElement("div");
    body.classList.add("card-body");

    let title = document.createElement("h5");
    title.textContent = "Матч";
    title.classList.add("card-title");

    let form = document.createElement("form");

    let team_1 = document.createElement("p");
    team_1.classList.add("card-text");
    team_1.textContent = "Команда #" + match.team_1.id + ": " +
        (await TeamsAPI.candidates()).find(
            element => element.id == match.team_1.user_1_id).fio + " - " +
        (await TeamsAPI.candidates()).find(
            element => element.id == match.team_1.user_2_id).fio

    let team_2 = document.createElement("p");
    team_2.classList.add("card-text");
    team_2.textContent = "Команда #" + match.team_2.id + ": " +
        (await TeamsAPI.candidates()).find(
            element => element.id == match.team_2.user_1_id).fio + " - " +
        (await TeamsAPI.candidates()).find(
            element => element.id == match.team_2.user_2_id).fio

    let judge_label = document.createElement("label");
    let judge_select = await getJudgeSelect(match.judge_id);
    judge_label.htmlFor = "judge";
    judge_label.textContent = "Судья";
    judge_select.id = "judge";
    judge_select.onchange = async _ => await editMatchCard(card, match.id);

    let time_label = document.createElement("label");
    let time_select = document.createElement("input");
    time_label.htmlFor = "time";
    time_label.textContent = "Время начала матча";
    if (match.start !== null) time_select.value = match.start.slice(0, -1);
    time_select.id = "time"
    time_select.type = "datetime-local";
    time_select.onchange = async _ => await editMatchCard(card, match.id);

    form.appendChild(team_1);
    form.appendChild(team_2);
    form.appendChild(judge_label);
    form.appendChild(judge_select);
    form.appendChild(time_label);
    form.appendChild(time_select);
    body.appendChild(title);
    body.appendChild(form);
    card.appendChild(body);

    return card;
}

window.addEventListener("load", async function () {
    let query = window.location.pathname.split("/");
    let tournament_id = +query[query.length - 1];
    let match_cards = document.querySelector("#match_cards");

    for (let i of await MatchesAPI.list(tournament_id)) {
        match_cards.appendChild(await createTeamCard(i));
    }
});
