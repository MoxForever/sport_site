import { UserAPI } from "/static/js/api/users_api.js";


function logOut() {
    UserAPI.logOut();
    window.location.href = "/";
}

async function lkRedirect() {
    let user = await UserAPI.me();
    if (user?.user_type == "ADMIN") window.location.href = "/admin";
    else if (user?.user_type == "JUDGE") window.location.href = "/judge";
}

window.addEventListener("load", function () {
    let is_login = false;
    for (let i of document.cookie.split("; ")) {
        let data = i.split("=", 1);
        if (data[0] == "user") {
            is_login = true;
            break;
        }
    }
    if (is_login) document.getElementById("login").classList.remove("d-none");
    else document.getElementById("no_login").classList.remove("d-none");

    document.querySelector("#log_out").addEventListener("click", logOut);
    document.querySelector("#lk").addEventListener("click", lkRedirect);
});
