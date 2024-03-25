function process_tournament_info(data) {
    let matches_info = {};
    for (let i of data.matches) {
        matches_info[i.team_1.id + "-" + i.team_2.id] = i.score_1 + " - " + i.score_2;
        matches_info[i.team_2.id + "-" + i.team_1.id] = i.score_2 + " - " + i.score_1;
    }

    document.querySelector("#t_name").textContent = data.tournament.name;
    let table = document.querySelector("#table");
    table.innerHTML = "";

    let row = table.insertRow();
    row.insertCell(0).textContent = "№";
    row.insertCell(1).textContent = "Имена";
    for (let i = 1; i <= data.teams.length; i++) {
        row.insertCell(i + 1).textContent = i;
    }

    for (let i = 1; i <= data.teams.length; i++) {
        let row = table.insertRow();
        row.insertCell(0).textContent = i;
        row.insertCell(1).textContent =
            data.teams[i - 1].user_1.fio + " - " + data.teams[i - 1].user_2.fio;

        for (let j = 1; j <= data.teams.length; j++) {
            let cell = row.insertCell(j + 1);
            if (j == i) {
                cell.textContent = "x";
            } else {
                cell.textContent = matches_info[i + "-" + j];
            }
        }
    }

    let container = document.querySelector("#matches");
    container.innerHTML = "";
    for (let i of data.matches) {
        let card = document.createElement("div");
        card.classList.add("card");

        let body = document.createElement("div");
        body.classList.add("card-body");

        let title = document.createElement("h5");
        title.classList.add("card-title");
        title.textContent = "№" + i.team_1.id + " - №" + i.team_2.id;

        let time_start = document.createElement("p");
        time_start.classList.add("card-text");
        time_start.textContent = "Время начала: "
        if (i.start === null) time_start.textContent += "Неизвестно";
        else time_start.textContent += i.start.replace("T", " ").replace("Z", "").split(".")[0];

        let time_end = document.createElement("p");
        time_end.classList.add("card-text");
        time_end.textContent = "Время окончания: "
        if (i.end === null) time_end.textContent += "Неизвестно";
        else time_end.textContent += i.end.replace("T", " ").replace("Z", "").split(".")[0];

        let score = document.createElement("h3");
        score.classList.add("card-text");
        score.textContent = i.score_1 + " - " + i.score_2;

        body.appendChild(title);
        body.appendChild(time_start);
        body.appendChild(time_end);
        body.appendChild(score);
        card.appendChild(body);
        
        container.appendChild(card);
    }
}


window.addEventListener("load", async function () {
    let event_source = new EventSource("/api/data");
    event_source.onmessage = e => process_tournament_info(JSON.parse(e.data));
});
