// Name: Oliver Fox & Filippos Solomonidis
// All functions involved for authentication of the website including: logging in, signing up, verifying input fields
// when signing up with showing errors and showing the loading circle for when the user submits the login/sign up.

/**
 * Checks the user has entered valid details then logs the user in to the website and then redirects to the home page.
 *
 * @param {string} email    The email the user has entered
 * @param {string} password The password the user has entered
 */
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

// Do various validation checks for when the user tries to sign up with an email and password including: checking a name
// has been entered, password matches given regex and the repeated passwords match, they have selected a school and they
// have selected a role.
function verifySignUp() {
    let valid = false;
    let emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    let passwordRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
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
        passwordError.textContent = "Password must contain at least 8 characters, 1 upper and lowercase character, 1 number and 1 special character";
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

/**
 * Animate in an error message from below the given input field.
 *
 * @param {string} error The name of the error element that should be displayed
 */
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

/**
 * Remove the error from the dialog box if an input has been amended.
 *
 * @param {string} error The name of the error element that should be hidden
 */
function hideError(error) {
    if (document.getElementById(error).style.marginTop !== "-35px") {
        let showError = anime({
            targets: "#" + error,
            marginTop: ['0px', "-35px"],
            opacity: ['100%', '0%'],
            duration: 1000,
            easing: 'easeInOutQuad'
        });

        showError.finished.then(removeError);

        function removeError() {
            document.getElementById(error).style.display = "none"
        }
    }
}
/**
Randomly assign a coloured picture from a directory of custom made profile pictures for a user when they sign up with
 an email and password.
 @return {string}: image url
  */
function getRandomPic(){
    const pics = [
        "15ff4c-user.png",
        "6ac492-user.png",
        "e20090-user.png",
        "ff1515-user.png",
        "ff15f3-user.png",
        "ff7315-user.png",
        "ffdc15-user.png"
    ];
    return "../static/images/default_icons/" + pics[Math.floor(Math.random() * pics.length)]
}

/**
 Create an account with Firebase authentication then add their details to the database.
 * @param {string} firstname
 * @param {string} lastname
 * @param {string} course
 * @param {string} role
 * @param {string} email
 * @param {string} password
 */
function signUp(firstname, lastname, course, role, email, password) {
    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((user) => {
            //Set the values added on sign up screen to firebase
            firebase.database().ref('users/' + firebase.auth().currentUser.uid).set({
                name: firstname + " " + lastname,
                email: email,
                course: course,
                role: role,
                uid: firebase.auth().currentUser.uid,
                profilePicture: getRandomPic(),
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

            // Check the user's email at this stage to prevent spam of people trying to find whether an email is already registered with the site.
            if (error.code === "auth/email-already-in-use") {
                document.getElementById("emailError").textContent = "Email address already in use";
                showError("emailError");
            }
        });
}

/**
Log the user out of the session and redirect to the home page (refresh).
 */
function logout() {
    fetch('/sessionLogout').then(()=> {
        window.location.assign('/');
    })
}

/**
 *  Add the session cookie to give Flask the user's information
 *  @return {Boolean}
 */
function addCookieRedirect() {
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE);
    //Login with firebase auth token
    firebase.auth().currentUser.getIdToken(true).then(idToken => {
        //Send Details to frontend along with the request
        fetch('/sessionLogin?idToken=' + idToken).then(()=> {
        window.location.assign('/');
        return firebase.auth().signOut();})
    });
}

/**
 * Display the loading circle for when the user submits their information for either logging in or signing up.
 *
 * @param {string} type Refers to either login or register page
 */
function showLoading(type) {
    var loadingIcon = document.getElementById(type + "Loading");
    let showError = anime({
        targets: "#" + type + "Loading",
        marginTop: ['-25%', '0%'],
        opacity: ['0%', '100%'], duration: 1000,
        easing: 'easeInOutQuad'
    });
}

/**
 * Function that uses Firebase's inbuilt feature to send an email to the given user and display a reset password field.
 *
 * @param {string} email The email the user entered in the forgot password input field
 */
function forgotPassword(email) {
    firebase.auth().sendPasswordResetEmail(email).then(() => {
        showError("emailSent"); // Even though it says "showError" I'm using this function for the animation functionality.
    });
}