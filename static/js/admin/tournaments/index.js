import { TournamentsAPI } from "/static/js/api/tournaments_api.js";


window.addEventListener("load", async function () {
    let list = document.querySelector("#tournaments_list");
    for (let i of await TournamentsAPI.fetch()) {
        let a = document.createElement("a");
        let li = document.createElement("li");

        a.textContent = i.name;
        a.href = "/admin/tournaments/" + i.id;
        li.classList.add("list-group-item");

        li.appendChild(a);
        list.appendChild(li);
    }
});
