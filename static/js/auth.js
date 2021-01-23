function login(email, password) {
    // As httpOnly cookies are to be used, do not persist any state client side.
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE);
    firebase.auth().signInWithEmailAndPassword(email, password).then(user => {
      return firebase.auth().currentUser.getIdToken(true).then(idToken => {
        fetch('/sessionLogin?idToken=' + idToken).then(()=> {
            return firebase.auth().signOut();
          }).then(() => {
              window.location.assign('/');
        })
      })
    });
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
                emailInUse(true);
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
