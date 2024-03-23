import { UserAPI } from "/static/js/api/users_api.js";

async function register() {
    let form = document.querySelector("#register_data");
    try {
        await UserAPI.register(
            form.elements["fio"].value,
            form.elements["email"].value,
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
    document.querySelector('#register_data').addEventListener('submit', register);
});
