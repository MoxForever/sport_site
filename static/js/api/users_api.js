export const UserAPI = {
    InvalidFields: class extends Error {
        constructor(invalid_fields) {
            super(invalid_fields.join(", "));
            this.name = 'InvalidFields';
            this.invalid_fields = invalid_fields;
        }
    },
    logOut: function () {
        document.cookie = 'user=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        sessionStorage.removeItem("me");
    },
    logIn: async function (email, password) {
        let r = await fetch("/api/users/log_in", {
            method: "POST",
            body: JSON.stringify({ email: email, password: password }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        let data = await r.json();
        if (r.status == 200) return data;
        else if (r.status == 400) throw data.detail;
    },
    register: async function (fio, email, password, user_type) {
        let r = await fetch("/api/users/register", {
            method: "POST",
            body: JSON.stringify({
                fio: fio,
                email: email,
                password: password,
                user_type: user_type
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        let data = await r.json();

        if (r.status == 200) return true;
        else if (r.status == 400) throw "Error: " + data.detail;
        else if (r.status == 422) {
            let invalid_fields = [];
            for (let e of data.detail) invalid_fields.push(e.loc[1]);
            throw new UserAPI.InvalidFields(invalid_fields);
        }
    },
    me: async function () {
        let buffered = sessionStorage.getItem("me");
        if (buffered !== null) {
            return JSON.parse(buffered);
        }

        let r = await fetch("/api/users/me");
        let data = await r.json();

        let me;
        if (r.status == 200) me = data;
        else if (r.status == 400) {
            sessionStorage.removeItem("me");
            UserAPI.logOut();
            return null;
        }
        else me = null;

        sessionStorage.setItem("me", JSON.stringify(me));
        return me;
    }
};
