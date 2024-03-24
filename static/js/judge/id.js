import { MatchesAPI } from "/static/js/api/matches_api.js";


async function update_scores(match, team_1, team_2) {
    try {
        await MatchesAPI.score(match.id, team_1, team_2);
    } catch (e) {
        return alert(e);
    }
    match.score_1 += team_1;
    match.score_2 += team_2;

    document.querySelector("#scores").textContent = match.score_1 + " - " + match.score_2;
}

async function end_match(match) {
    await MatchesAPI.end(match.id);
    window.location.href = "/judge";
}


window.addEventListener("load", async function () {
    let raw_query = window.location.href.split("/");
    let match = await MatchesAPI.get(+raw_query[raw_query.length - 1]);

    document.querySelector("#t").textContent = match.tournament.name;

    document.querySelector("#u_1").textContent = "Команда #" + match.team_1.id;
    document.querySelector("#u_2").textContent = "Команда #" + match.team_2.id;

    document.querySelector("#u_1_1").textContent = match.team_1.user_1.fio;
    document.querySelector("#u_1_2").textContent = match.team_1.user_2.fio;
    document.querySelector("#u_2_1").textContent = match.team_2.user_1.fio;
    document.querySelector("#u_2_2").textContent = match.team_2.user_2.fio;

    document.querySelector("#scores").textContent = match.score_1 + " - " + match.score_2;

    document.querySelector("#team_1_add").onclick = async _ => await update_scores(match, 1, 0);
    document.querySelector("#team_1_decrease").onclick = async _ => await update_scores(match, -1, 0);
    document.querySelector("#team_2_add").onclick = async _ => await update_scores(match, 0, 1);
    document.querySelector("#team_2_decrease").onclick = async _ => await update_scores(match, 0, -1);

    document.querySelector("#stop").onclick = async _ => await end_match(match);
});
