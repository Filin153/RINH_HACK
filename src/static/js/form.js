let nameInput = document.querySelector(".login");
let passInput = document.querySelector(".pass");
nameInput.addEventListener("focus", function() {
	if (this.placeholder == "Логин") {
		this.placeholder = "";
	}
});
nameInput.addEventListener("blur", function() {
	if (this.value == "") {
		this.placeholder = "Логин";
	}
});
passInput.addEventListener("focus", function() {
	if (this.placeholder == "Пароль") {
		this.placeholder = "";
	}
});
passInput.addEventListener("blur", function() {
	if (this.value == "") {
		this.placeholder = "Пароль";
	}
});

const loginForm = document.getElementById("form__id");
const loginButton = document.getElementById("button");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = document.getElementById('usernameInput').value;
    const password = document.getElementById('passwordInput').value;

    const url = `http://localhost:8000/user/getone?login=${username}&password=${password}`;

    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        const token = data.token;
        if (token !== '' && token !== undefined) {
            localStorage.setItem("token", token);
            window.location.href = `/main/${token}`;
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});