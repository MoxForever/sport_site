import { UserAPI } from "/static/js/api/users_api.js";


window.addEventListener("load", async function () {
    let user = await UserAPI.me();
    if (user?.user_type != "ADMIN") window.location.href = "/";
});
