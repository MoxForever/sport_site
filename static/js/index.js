function tournament_card(tournament) {
    let container = document.createElement("div");
    container.classList.add("carousel-item");

    let title = document.createElement("h2")
    title.classList.add("text-center", "py-3");
    title.textContent = "Соревнование";

    let table = document.createElement("table");
    table.classList.add("table", "table-bordered");

    container.append(title);
    container.appendChild(table);
    return container;
}


window.addEventListener("load", async function () {
    let container = document.querySelector("#tournament_list");
    let first = tournament_card();
    first.classList.add("active")
    container.appendChild(first);
    container.appendChild(tournament_card());
    container.appendChild(tournament_card());
    container.appendChild(tournament_card());
})