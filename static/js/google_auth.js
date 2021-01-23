// Followed these instructions for Google sign in:
//https://firebase.google.com/docs/auth/web/google-signin#advanced-handle-the-sign-in-flow-manually
function handleAuthClick() {
    var provider = new firebase.auth.GoogleAuthProvider();
    provider.addScope('profile');
    provider.addScope('email');

firebase.auth().signInWithPopup(provider).then(function(result) {
    var user = result.user;
    var isNewUser = result.additionalUserInfo.isNewUser;
    onSignIn(user, isNewUser);
}).catch(function(error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // The email of the user's account used.
        var email = error.email;
        // The firebase.auth.AuthCredential type that was used.
        var credential = error.credential;
    });
}

function onSignIn(googleUser, isNewUser) {
    console.log('Google Auth Response', googleUser);
    // We need to register an Observer on Firebase Auth to make sure auth is initialized.
    var unsubscribe = firebase.auth().onAuthStateChanged((firebaseUser) => {
        unsubscribe();
        // Check if we are already signed-in Firebase with the correct user.
        if (!isUserEqual(googleUser, firebaseUser)) {
            // Build Firebase credential with the Google ID token.
            var credential = firebase.auth.GoogleAuthProvider.credential(googleUser.getAuthResponse().id_token);

            // Sign in with credential from the Google user.
            firebase.auth().signInWithCredential(credential).catch((error) => {
                // Handle Errors here.
                var errorCode = error.code;
                var errorMessage = error.message;
                // The email of the user's account used.
                var email = error.email;
                // The firebase.auth.AuthCredential type that was used.
                var credential = error.credential;
                // ...
            });
            addCookieRedirect();

        } else {
            console.log('User already signed-in Firebase.');
            if (isNewUser) {
                sessionStorage.setItem("name", googleUser.displayName);
                sessionStorage.setItem('email', googleUser.email);
                sessionStorage.setItem('uid', googleUser.uid);
                sessionStorage.setItem('picture', googleUser.photoURL);

                window.location.assign('/gregister');
            } else {
                // User already has signed in with Google previously so redirect to home page.
                addCookieRedirect();
            }
        }
    });
}

function addCookieRedirect(){
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.NONE);
    firebase.auth().currentUser.getIdToken(true).then(idToken => {
    fetch('/sessionLogin?idToken=' + idToken).then(()=> {
        window.location.assign('/');
        return firebase.auth().signOut();})
    });
}

function isUserEqual(googleUser, firebaseUser) {
    if (firebaseUser) {
        var providerData = firebaseUser.providerData;
        for (var i = 0; i < providerData.length; i++) {
            if (providerData[i].providerId === firebase.auth.GoogleAuthProvider.PROVIDER_ID &&
                    providerData[i].uid === googleUser.providerData[i].uid) {
                return true;
            }
        }
    }
    return false;
}