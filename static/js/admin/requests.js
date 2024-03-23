import { RequestsAPI } from "/static/js/api/requests_api.js";


async function createCard(user) {
    let card = document.createElement("div");
    card.classList.add("card");

    let body = document.createElement("div");
    body.classList.add("card-body");
    card.appendChild(body);

    let row = document.createElement("div");
    row.classList.add("row");
    body.appendChild(row);

    let user_info = document.createElement("div");
    user_info.classList.add("flex-fill");
    row.appendChild(user_info);

    let fio = document.createElement("h3");
    fio.classList.add("card-title");
    fio.textContent = user.fio;
    user_info.appendChild(fio);

    let email = document.createElement("p");
    email.classList.add("card-text");
    email.textContent = "Email: " + user.email;
    user_info.appendChild(email);

    let account_type = document.createElement("p");
    account_type.classList.add("card-text");
    account_type.textContent = "Тип аккаунта: " + {
        "ADMIN": "Администратор","JUDGE": "Судья","ATHLETE": "Участник"
    }[user.user_type];
    user_info.appendChild(account_type);

    async function process_click(confirm) {
        card.remove();
        await RequestsAPI.process(user.id, confirm)
    }

    let buttons = document.createElement("div");
    buttons.classList.add("d-flex", "flex-column");
    row.appendChild(buttons);

    let confirm = document.createElement("button");
    confirm.classList.add("btn", "btn-success", "mb-1");
    confirm.textContent = "Подтвердить";
    confirm.addEventListener("click", _ => process_click(true));
    buttons.appendChild(confirm);

    let reject = document.createElement("button");
    reject.classList.add("btn", "btn-danger");
    reject.textContent = "Отменить";
    reject.addEventListener("click", _ => process_click(false));
    buttons.appendChild(reject);

    return card;
}

async function recreateCards() {
    let cards_list = document.querySelector("#cards_list");
    for (let i = 0; i < cards_list.children.length; i++) {
        cards_list.firstChild.remove();
    }

    for (let i of Object.values(await RequestsAPI.fetch())) {
        cards_list.appendChild(await createCard(i));
    }
}


window.addEventListener("load", async function () {
    await recreateCards();
});
