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
