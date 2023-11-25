// Выпадающий список
let buttonImgs = document.querySelectorAll('.server__header-img');
let serverVirtuals = document.querySelectorAll('.server__virtual');
let rotationAngles = Array(buttonImgs.length).fill(0);
let rotated = Array(buttonImgs.length).fill(false);

for (let i = 0; i < buttonImgs.length; i++) {
  buttonImgs[i].addEventListener('click', function() {
    if (!rotated[i]) {
      serverVirtuals[i].style.display = 'block';
      buttonImgs[i].style.transform = 'rotate(360deg)';
    } else {
      serverVirtuals[i].style.display = 'none';
      buttonImgs[i].style.transform = 'rotate(270deg)';
    }
    rotated[i] = !rotated[i];
  });
}

// Удаление сервера
const serverRemove = document.querySelectorAll('.server__header-remove');
const server = document.querySelectorAll('.server')

for (let i = 0; i < serverRemove.length; i++) {
  serverRemove[i].addEventListener('click', function() {
    server[i].remove();
  });
}

// Удаление виртуальной машины
const contentRemove = document.querySelectorAll('.content__remove');
const virtualMachine = document.querySelectorAll('.virtual-machine__body')

for (let i = 0; i < contentRemove.length; i++) {
  contentRemove[i].addEventListener('click', function() {
   virtualMachine[i].remove();
  });
}

// Модалка

const buttonAdd = document.querySelector('.button__add');
const modal = document.getElementById('modal');
const closeModalBtn = document.querySelector('.close');

buttonAdd.addEventListener('click', function() {
	modal.style.display = 'block';
});

closeModalBtn.addEventListener('click', function() {
	modal.style.display = 'none';
});
