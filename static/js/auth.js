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
                    console.log(error);
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
    // First logout of Google.
    gapi.load('auth2', function() {
        gapi.auth2.init({
            client_id: "1081173404847-ddjfjkqhfj79u9qiv7lrsajibo3vtgqc.apps.googleusercontent.com",
        }).then(function(auth2) {
            auth2.signOut().then(function () {
                console.log('User signed out.');
                sessionStorage.clear();

                // Logout of Firebase.
                firebase.auth().signOut().then(function() {
                    window.open("/", "_self");
                }).catch(function(error) {
                    // An error happened.
                });
            });
        });
    });


}

