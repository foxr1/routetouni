function login() {
    let email = document.getElementById("loginEmail").value;
    let password = document.getElementById("password").value;
    firebase.auth().signInWithEmailAndPassword(email, password)
        .then(function() {
            hideDialog("signInDialog");
        }).catch(function(error) {
            console.log(error);
    });
}

function signUp() {
    let email = document.getElementById("signUpEmail").value;
    let password = document.getElementById("signUpPassword").value;
    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((user) => {
            hideDialog("signUpDialog");
        })
        .catch((error) => {
            var errorCode = error.code;
            var errorMessage = error.message;
        });
}

function logout() {
    firebase.auth().signOut().then(function() {
        localStorage.clear();
        hideDialog("accountDialog");
        location.reload();
        // Sign-out successful.
    }).catch(function(error) {
        // An error happened.
    });
}

function showLoginDialog() {
    let dialog = document.getElementById("signUpDialog");
    let span = document.getElementById("signUpClose");

    dialog.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        hideDialog("signUpDialog");
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target === dialog && dialog.style.display === "block") {
            hideDialog("signUpDialog");
        }
    }
}

function hideDialog(name) {
    let dialog = document.getElementById(name);
    setTimeout(function () {
        dialog.style.display = "none";
    }, 250);
}

