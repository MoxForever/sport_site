import { UserAPI } from "/static/js/api/users_api.js"

async function logIn() {
    let form = document.querySelector("#login_data");
    let user;
    try {
        user = await UserAPI.logIn(
            form.elements["email"].value,
            form.elements["password"].value,
        );
    } catch (e) {
        if (e instanceof UserAPI.InvalidFields) {
            for (let i of e.invalid_fields) {
                form.elements[i].classList.add('is-invalid');
            }
        }
        else document.querySelector("#invalid_data").textContent = e;
        return;
    }

    if (user.user_type == "ADMIN") window.location.href = "/admin";
}

window.addEventListener("load", function () {
    document.querySelector('#login_data').addEventListener('submit', logIn);
});
