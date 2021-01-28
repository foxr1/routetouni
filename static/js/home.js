// Name: Oliver Fox
// All functions involved when using the home page including: checking the user is logged in, redirecting to login page,
// check if they are an admin to display admin button and showing and hiding the account box.

// Check if a user is logged in.
var loginBtn = document.getElementById("login");
var adminBtn = document.getElementById("adminBtn");
var accountPicture = document.getElementById("accountPicture");
var loggedIn = false;

// Create an object for the user to pull information like name, email, role, school and profile picture.
var user = JSON.parse($('#user').html());

// If a user is logged in, the login button is removed and their account picture is displayed, if not then the login
// button is shown.
if (user) {
    loginBtn.style.background = 'none';
    accountPicture.src = user.picture;
    accountPicture.style.display = "block";
    loggedIn = true;
} else {
    loginBtn.style.padding = "15px";
    loginBtn.textContent = "Login";
    loggedIn = false;

    // If the user is not logged in disable the chat bubble.
    var chatBubble = document.getElementById("chatBubble");
    chatBubble.style.backgroundColor = "grey";
    chatBubble.onclick = function () {
        alert("You must be logged in to access the chat.");
    }
    chatBubble.onmouseover = null;
}

// Change function of button depending on whether a user is logged in, if they are it displays the account screen,
// if not they are redirected to the login screen.
function checkLogin() {
    if (loggedIn) {
        showAccount();
    } else {
        loginPageTransition();
    }
}

// If user is an admin, display the button to get to admin page, else remove it.
if (user != null && user.role === "admin") {
    adminBtn.style.display = "block";
} else {
    adminBtn.style.display = "none";
}

var image = document.getElementById("changePicture");
image.onchange = function (event) {
    var fr = new FileReader();
    var profilePicture = document.getElementById("profilePicture");
    fr.onload = function () {
        profilePicture.src = fr.result;
    }
    fr.readAsDataURL(image.files[0])
}

// Function responsible for changing the users profile picture, the image they have selected is uploaded to the Firebase
// Storage and the link to that image is then updated within the user's 'profilePicture' attribute in the database.
function changePicture() {
    if (image.files != null) {
        var storageRef = firebase.storage().ref();
        var imageRef = storageRef.child('Profile Pictures/' + user.uid + '.jpg');
        imageRef.put(image.files[0]).then(function (snapshot) {
            snapshot.ref.getDownloadURL().then(function(downloadURL) {
                database.ref("users/" + user.uid).update({
                    profilePicture: downloadURL
                }).then(function () {
                    location.reload();
                });
            });
        })
    } else {
        hideAccount();
    }
}

// This function animated and displays the account screen for when a user is logged in.
function showAccount() {
    var accountBox = document.getElementById("accountBox");
    var span = document.getElementsByClassName("close")[0];
    var name = document.getElementById("name");
    var emailText = document.getElementById("email");
    var profilePicture = document.getElementById("profilePicture");
    var schoolText = document.getElementById("course");

    accountBox.style.display = "block";
    name.textContent = user.name;
    emailText.textContent = user.email;
    profilePicture.src = user.picture;
    schoolText.textContent = user.school;

    let fadeBackground = anime({
        targets: '#accountBox',
        opacity: ['0%', '100%'], duration: 1000,
        easing: 'easeInOutQuad'
    });

    let showAccount = anime({
        targets: '#box',
        translateY: [-250, 0],
        easing: 'easeInOutQuad'
    });

    // Checks if the user has selected an image and not saved, then hides the account screen.
    span.onclick = function() {
        if (image.files[0] != null) {
            if (window.confirm("You have unsaved changes, are you sure you want to leave?")) {
                image.value = ""; // Clear selected image
                hideAccount();
            }
        } else {
            hideAccount();
        }
    }

    // If user clicks outside of the account box, checks if the user has selected an image and not saved, then hides
    // the account screen.
    window.onclick = function(event) {
        if (event.target === accountBox) {
            if (image.files[0] != null) {
                if (window.confirm("You have unsaved changes, are you sure you want to leave?")) {
                    image.value = ""; // Clear selected image
                    hideAccount();
                }
            } else {
                hideAccount();
            }
        }
    }
}

// Remove the account box.
function hideAccount() {
    let fadeBackground = anime({
        targets: '#accountBox',
        opacity: ['100%', '0%'], duration: 1000,
        easing: 'easeInOutQuad'
    })

    let hideAccount = anime({
        targets: '#box',
        translateY: [0, -250],
        easing: 'easeInOutQuad',
        update: function(anim) {
            if (anim.progress === 100) {
                accountBox.style.display = "none";
            }
        }
    })
}