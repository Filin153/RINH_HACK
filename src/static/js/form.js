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

    fetch("http://localhost:8000/user/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("token", data.token);

        window.location.href = "/main";
    })
    .catch(error => {
        console.error("Error:", error);
    });
});