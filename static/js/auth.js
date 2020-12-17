function login(email, password) {
firebase.auth().signInWithEmailAndPassword(email, password)
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

})}

function signUp(firstname, lastname, course, role, email, password) {
    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((user) => {
            firebase.database().ref('users/' + firebase.auth().currentUser.uid).set({
                firstname: firstname,
                lastname: lastname,
                email: email,
                course: course,
                role: role,
                uid: firebase.auth().currentUser.uid
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
            apiKey: "AIzaSyCl6CgDwOVVxdvQou38U-v71tZHoH9Fx-k",
            client_id: "1081173404847-ddjfjkqhfj79u9qiv7lrsajibo3vtgqc.apps.googleusercontent.com"
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

