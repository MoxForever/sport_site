import { UserAPI } from "/static/js/api/users_api.js";
import { CitiesAPI } from "/static/js/api/cities_api.js";

async function register() {
    let form = document.querySelector("#register_data");
    try {
        await UserAPI.register(
            form.elements["fio"].value,
            form.elements["email"].value,
            +form.elements["city_id"].value,
            form.elements["password"].value,
            form.elements["user_type"].value,
        )
    } catch (e) {
        if (e instanceof UserAPI.InvalidFields) {
            for (let i of e.invalid_fields) {
                form.elements[i].classList.add('is-invalid');
            }
        }
        else document.querySelector("#invalid_data").textContent = e;

        return;
    }
    alert("Регистрация успешна! Ожидайте подтверждения от организатора");
    window.location.href = "/";
}

window.addEventListener("load", async function () {
    let city_select = document.querySelector("#city_id");
    let cities = await CitiesAPI.fetch();
    for (let i in cities) {
        let option = document.createElement("option");
        option.value = cities[i].id;
        option.textContent = cities[i].name;
        city_select.appendChild(option);
    }
    document.querySelector('#register_data').addEventListener('submit', register);
});
