function login(email, password) {
    // As httpOnly cookies are to be used, do not persist any state client side.
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE);
    firebase.auth().signInWithEmailAndPassword(email, password).then(user => {
        showLoading("login");
        return firebase.auth().currentUser.getIdToken(true).then(idToken => {
            fetch('/sessionLogin?idToken=' + idToken).then(()=> {
                return firebase.auth().signOut();
            }).then(() => {
                hideError("loginError");
                window.location.assign('/');
        })
      })
    })
    .catch((error) => {
        var errorCode = error.code;
        console.log(errorCode);
        document.getElementById("loginError").textContent = "Invalid email address or password";
        showError("loginError");
    });
}

function verifySignUp() {
    let valid = false;
    let emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    let passwordRegex = /^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/
    var firstname = document.getElementById("firstName");
    var lastname = document.getElementById("lastName");
    var nameError = document.getElementById("nameError");
    var email = document.getElementById("signUpEmail");
    var emailError = document.getElementById("emailError");
    var password = document.getElementById("signUpPassword");
    var passwordRepeat = document.getElementById("signUpPasswordRepeat");
    var passwordError = document.getElementById("passwordError");
    var school = document.getElementById("courses");
    var schoolOption = school.options[document.getElementById("courses").selectedIndex];
    var schoolError = document.getElementById("courseError");
    var roles = document.getElementById("roles");
    var roleOption = roles.options[document.getElementById("roles").selectedIndex];
    var roleError = document.getElementById("roleError");



    if (firstname.value !== "" && lastname.value !== "" && email.value.toLowerCase().match(emailRegex) && password.value === passwordRepeat.value &&
        password.value.match(passwordRegex) && schoolOption.value !== "blank" && roleOption.value !== "blank") {
        valid = true;
    }

    if (firstname.value === "") {
        showError("nameError");
        nameError.textContent = "Enter your first name"
        valid = false;
    } else {
        hideError("nameError");
    }

    if (lastname.value === "") {
        showError("nameError");
        nameError.textContent = "Enter your surname"
        valid = false;
    } else {
        hideError("nameError");
    }

    if (firstname.value === "" && lastname.value === "") {
        showError("nameError");
        nameError.textContent = "Enter your name"
        valid = false;
    } else {
        hideError("nameError");
    }

    if (!email.value.toLowerCase().match(emailRegex)) {
        showError("emailError");
        emailError.textContent = "Enter a valid email"
        valid = false;
    } else if (emailError.textContent === "Enter a valid email") {
        hideError("emailError");
    }

    if (!password.value.match(passwordRegex)) {
        showError("passwordError");
        passwordError.textContent = "Password must contain at least 8 characters, 1 upper and lowercase character and 1 number";
        valid = false;
    } else if (password.value === passwordRepeat.value) {
        hideError("passwordError");
    }

    if (password.value !== passwordRepeat.value) {
        showError("passwordError");
        passwordError.textContent = "Passwords do not match";
        valid = false;
    } else if (password.value.match(passwordRegex)) {
        hideError("passwordError");
    }

    if (schoolOption.value === "blank") {
        showError("courseError");
        schoolError.textContent = "Select a school";
        valid = false;
    } else {
        hideError("courseError");
    }

    if (roleOption.value === "blank") {
        showError("roleError");
        roleError.textContent = "Select a role";
        valid = false;
    } else {
        hideError("roleError");
    }

    if (valid) {
        signUp(firstname.value, lastname.value, schoolOption.text, roleOption.text, email.value, password.value);
    }
}

function showError(error) {
    if (document.getElementById(error).style.marginTop !== "0px") {
        document.getElementById(error).style.display = "block"
        let showError = anime({
            targets: "#" + error,
            marginTop: ['-35px', '0px'],
            opacity: ['0%', '100%'], duration: 1000,
            easing: 'easeInOutQuad'
        });
    }
}

function hideError(error) {
    if (document.getElementById(error).style.marginTop !== "-35px") {
        let showError = anime({
            targets: "#" + error,
            marginTop: ['0px', "-35px"], duration: 1000,
            opacity: ['100%', '0%'], duration: 1000,
            easing: 'easeInOutQuad'
        });

        showError.finished.then(removeError);

        function removeError() {
            document.getElementById(error).style.display = "none"
        }
    }
}

function get_random_pic(){
    const pics = [
        "15ff4c_user.png",
        "6ac492_user.png",
        "e20090_user.png",
        "ff1515_user.png",
        "ff15f3_user.png",
        "ff7315_user.png",
        "ffdc15_user.png"
    ];
    return "../static/images/default_icons/" + pics[Math.floor(Math.random() * pics.length)]
}

// Create an account with Firebase authentication then add their details to the database.
function signUp(firstname, lastname, course, role, email, password) {
    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((user) => {
            firebase.database().ref('users/' + firebase.auth().currentUser.uid).set({
                name: firstname + " " + lastname,
                email: email,
                course: course,
                role: role,
                uid: firebase.auth().currentUser.uid,
                profilePicture: get_random_pic(),
                mentor_verified: false
            }, (error) => {
                if (error) {
                    console.log(error);
                } else {
                    showLoading("signUp");
                    hideError("emailError");
                    console.log(firstname + " " + lastname)
                    addCookieRedirect();
                }
            });
        })
        .catch((error) => {
            var errorCode = error.code;
            console.log(errorCode);
            if (error.code === "auth/email-already-in-use") {
                document.getElementById("emailError").textContent = "Email address already in use";
                showError("emailError");
            }
        });
}

function logout() {
    fetch('/sessionLogout').then(()=> {
        window.location.assign('/');
    })
}

function addCookieRedirect(){
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE);
    firebase.auth().currentUser.getIdToken(true).then(idToken => {
    fetch('/sessionLogin?idToken=' + idToken).then(()=> {
        console.log(idToken);
        window.location.assign('/');
        return firebase.auth().signOut();})
    });
}

function showLoading(type) {
    var loadingIcon = document.getElementById(type + "Loading");
    loadingIcon.style.display = "block";
    let showError = anime({
        targets: "#" + type + "Loading",
        marginTop: ['-25%', '0%'],
        opacity: ['0%', '100%'], duration: 1000,
        easing: 'easeInOutQuad'
    });
}