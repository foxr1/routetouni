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
})}

function signUp(firstname, lastname, course, role, email, password) {
    firebase.auth().createUserWithEmailAndPassword(email, password)
        .then((user) => {
            firebase.database().ref('users/' + firebase.auth().currentUser.uid).set({
                name: firstname + " " + lastname,
                email: email,
                course: course,
                role: role,
                uid: firebase.auth().currentUser.uid,
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
            var errorMessage = error.message;
            console.log(error);
        });}

function logout() {
    // First logout of Google.
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
