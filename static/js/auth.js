function login(email, password) {
    firebase.auth().signInWithEmailAndPassword(email, password)
        .then(function() {
            window.open("/", "_self");
        }).catch(function(error) {
            console.log(error);
    });
}

function signUp(firstname, lastname, course, email, password) {
    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((user) => {
            firebase.database().ref('users/' + firebase.auth().currentUser.uid).set({
                firstname: firstname,
                lastname: lastname,
                course: course,
                email: email
            }, (error) => {
                if (error) {
                    // The write failed...
                } else {
                    window.open("/", "_self");
                }
            });

        })
        .catch((error) => {
            var errorCode = error.code;
            var errorMessage = error.message;
            console.log(error);
        });
}

function logout() {
    firebase.auth().signOut().then(function() {
        // Sign-out successful.
    }).catch(function(error) {
        // An error happened.
    });
}

