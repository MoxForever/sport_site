import { MatchesAPI } from "/static/js/api/matches_api.js";


window.addEventListener("load", async function () {
    let container = document.querySelector("#matches");
    for (let i of await MatchesAPI.list_judge()) {
        console.log(i);

        let row = document.createElement("li");
        row.classList.add("list-group-item");

        let a = this.document.createElement("a");
        a.href = "/judge/" + i.id;
        a.textContent = "Матч #" + i.id;
        if (i.start !== null) a.textContent += ", " + i.start.replace("T", " ").replace("Z", " ");
        
        row.appendChild(a);
        container.appendChild(row);
    }
})