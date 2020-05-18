function dC(name) {
    document.getElementById("card-image").src = '../card-images/'.concat(name, '.jpg');
    document.getElementById("card-modal").style.display = "block";
}
