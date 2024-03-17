import { CitiesAPI } from "/static/js/api/cities_api.js"


async function recreateCities() {
    let cities_list = document.querySelector("#cities");
    for (let i = cities_list.children.length - 2; i >= 0; i--) {
        cities_list.children[0].remove();
    }

    let first_child = cities_list.firstChild;
    let cities = await CitiesAPI.fetch();

    for (let i of Object.values(cities)) {
        let li = document.createElement("li");
        let p = document.createElement("p");
        let btn = document.createElement("button");

        p.textContent = i.name;
        btn.textContent = "Удалить";
        btn.addEventListener("click", () => deleteCity(i.id));

        li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
        p.classList.add("mb-0");
        btn.classList.add("btn", "btn-danger");

        li.appendChild(p);
        li.appendChild(btn);
        cities_list.insertBefore(li, first_child);
    }
}

async function deleteCity(id) {
    await CitiesAPI.delete(id);
    await recreateCities();
}

async function newCity() {
    await CitiesAPI.add(document.querySelector("#new_city_input").value);
    await recreateCities();
}

window.addEventListener("load", async function () {
    await recreateCities();
    document.querySelector("#new_city_btn").addEventListener("click", newCity);
});
