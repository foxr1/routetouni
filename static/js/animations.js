// Name: Oliver Fox
// All the functions involved with the animations on the website, including: the initial landing page animation of the
// bubbles appearing in a circle around the Newcastle University logo, bubbles expanding on click on the home screen,
// slight expansions of bubbles when a mouse hovers over them, transition for clicking the login button from the home
// screen and switching between login, sign up and forgot password from the login page.

// Global variables for the bubbles attributes to be accessed from various functions within this file.
var bTop, bBottom, bLeft, bRight = '0%'; // Position of bubble before being clicked.
var bImg; // Last bubble's image from home screen.
var bSize; // Size of bubble before click (mobile/desktop).

// Which ever bubble is clicked from the home page is stored temporarily so it can be referenced when the user clicks
// the back button.
var tempBubble;
var tempBubbleHtml;

// Timeline of all the bubbles animating in when the page loads in a ring around the Newcastle logo.
let tl = anime.timeline({
    easing: 'easeOutExpo',
    duration: 500
});

tl
.add({
    targets: '#universityHeading',
    scale: [0,1.5],
    borderRadius: '50%',
    easing: 'spring',
}, 100)
.add({
    targets: '#chatBubble',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 300)
.add({
    targets: '#newsBubble',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 400)
.add({
    targets: '#pubsBubble',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 500)
.add({
    targets: '#mapBubble',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 600)
.add({
    targets: '#healthBubble',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 700)
.add({
    targets: '#societiesBubble',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 800)
.add({
    targets: '#revisionBubble',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 900)
.add({
    targets: '#accommBubble',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 1000)
.add({
    targets: '#login',
    scale: [0,1],
    easing: 'spring',
}, 1100)
.add({
    targets: '#adminBtn',
    scale: [0,1],
    easing: 'spring',
}, 1200);


/**
 * Function to expand the bubble to fill the screen then change the contents of the bubble to which ever page the user
 * has selected.
 *
 * @param {string} bubble   The name of the bubble that the user has clicked
 * @param {string} img      The name of the image variable for the bubble that has been selected
 * @param {string} nextPage The page that the bubble is to go to after the animation completes
 */
function bubbleClick(bubble, img, nextPage) {
    let bubbleEl = document.getElementById(bubble)
    let bubbleStyles = window.getComputedStyle(document.querySelector('#' + bubble));
    if (bubbleStyles.zIndex === '0') {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        bubbleEl.style.zIndex = '2'; // Move circle to front
        bTop = bubbleStyles.top;
        bBottom = bubbleStyles.bottom;
        bLeft = bubbleStyles.left;
        bRight = bubbleStyles.right;
        bImg = img;
        bSize = bubbleStyles.height;

        let fadeImg = anime({
            targets: img,
            opacity: ['100%', '0%'],
            easing: 'easeInOutQuad'
        })

        // Create an XML request to get the contents of the page being clicked so it can display the page without having
        // to do a redirect, making for a smoother experience.
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                tempBubbleHtml = document.getElementById(bubble).innerHTML;
                tempBubble = document.getElementById(bubble);
                document.getElementById(bubble).innerHTML = this.responseText;
            }
        };
        xhttp.open("GET", '/' + nextPage, true);
        xhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');

        // Expand the bubble to fill the size of the page, then change shape to a rectangle so the page's contents can
        // be added correctly.
        let expandBubble = anime({
            targets: '#' + bubble,
            keyframes: [
                {scale: 30, duration: 1000},
                {height: '100%'},
                {width: '100%'},
                {top: '0%'},
                {bottom: '0%'},
                {left: '0%'},
                {right: '0%'},
                {borderRadius: '0%'},
                {scale: 1}
            ],
            duration: 100,
            easing: 'easeInOutQuad'
        });

        expandBubble.finished.then(loadPage);

        // Only redirect if the chat has been selected as there are specific functions that need to be executed from a
        // separate page.
        function loadPage() {
            if (nextPage === "chat") {
                window.location.assign("/chat")
            } else {
                xhttp.send();
            }
        }
    }
}

/**
 * Enlarge the bubble slightly when the user hovers over the bubble with their mouse.
 *
 * @param {string} bubble The name of the bubble that the user has hovered over
 */
function bubbleHover(bubble) {
    let bubbleStyles = window.getComputedStyle(document.querySelector(bubble));
    if (bubbleStyles.zIndex === '0') {
        let hoverBubble = anime({
            targets: bubble,
            scale: 1.5, duration: 250,
            easing: 'easeInOutQuad'
        });
    }
}

/**
 * Shrink the bubble back when the user's mouse is not hovered over the bubble.
 *
 * @param {string} bubble The name of the bubble the user's mouse has left
 */
function bubbleLeave(bubble) {
    let bubbleStyles = window.getComputedStyle(document.querySelector(bubble));
    if (bubbleStyles.zIndex === '0') {
        let leaveBubble = anime({
            targets: bubble,
            scale: 1, duration: 250,
            easing: 'easeInOutQuad'
        });
    }
}

// If the user has pressed a bubble from the home screen, pressing the back button within the navigation bar will shrink
// the bubble back down to it's original size and position on the home screen, if they have been directed to a page from
// the navigation bar buttons they will simply be redirected to the home page.
function backPress() {
    let bubble1 = document.getElementById("chatBubble");
    let bubble2 = document.getElementById("newsBubble");
    let bubble3 = document.getElementById("pubsBubble");
    let bubble4 = document.getElementById("mapBubble");
    let bubble5 = document.getElementById("accommBubble");
    let bubble6 = document.getElementById("healthBubble");
    let bubble7 = document.getElementById("societiesBubble");
    let bubble8 = document.getElementById("revisionBubble");
    let bubbles = [bubble1, bubble2, bubble3, bubble4, bubble5, bubble6, bubble7, bubble8];
    let bubblesIds = ["#chatBubble", "#newsBubble", "#pubsBubble", "#mapBubble", "#accommBubble", "#healthBubble", "#societiesBubble", "#revisionBubble"];

    if (tempBubble != null) { // Check if the user has previously come from the home page.
        // Loop through all bubbles to check which one is at the front of the page, i.e. which page the user is currently on
        for (let i = 0; i < 8; i++) {
            if (bubbles[i].style.zIndex === '2') {
                bubbles[i].style.top = bTop;
                bubbles[i].style.bottom = bBottom;
                bubbles[i].style.left = bLeft;
                bubbles[i].style.right = bRight;

                document.getElementById(bubbles[i].id).innerHTML = tempBubbleHtml;
                bubbles[i] = tempBubble;
                let revealImg = anime({
                    targets: bImg,
                    opacity: ['0%', '100%'], duration: 1750,
                    easing: 'easeInOutQuad'
                });

                let decreaseBubble = anime({
                    targets: bubblesIds[i],
                    borderRadius: '50%',
                    height: bSize,
                    width: bSize,
                    scale: [20, 1],
                    easing: 'easeInOutQuad'
                });

                setTimeout(function() {
                    bubbles[i].style.zIndex = '0';
                }, 1000);
                break;
            }
        }
    } else { // If they have redirected from the navigation bar then do a redirect back to the home page.
        window.location.assign("/")
    }
}

// Animate page to move off to the left and then redirect to login page which will animate on load.
function loginPageTransition() {
    let homePageTransition = anime({
        targets: '#homeLayout',
        left: '-110%', duration: 750,
        easing: 'easeInOutQuad'
    });

    homePageTransition.finished.then(openLoginPage);

    function openLoginPage() {
        window.location.assign("/login");
    }
}

// Animate login box to move to the right and move sign up box in from the left.
function getSignUp() {
    let loginAnim = anime({
        targets: '#loginDialog',
        translateX: [0, 1500], duration: 750,
        easing: 'easeInOutQuad'
    });

    let signUpAnim = anime({
        targets: '#signUpDialog',
        translateX: [-1500, 0], duration: 750,
        easing: 'easeInOutQuad'
    });
}

// Animated forgot password dialog screen to the right and the login dialog back in from the left.
function getLoginFromForgot() {
    let loginAnim = anime({
        targets: '#loginDialog',
        translateX: [-1500, 0], duration: 750,
        easing: 'easeInOutQuad'
    });

    let forgotAnim = anime({
        targets: '#forgotDialog',
        translateX: [0, 1500], duration: 750,
        easing: 'easeInOutQuad'
    });
}

// Animate sign up box to move to the left and move login box from the right.
function getLogin() {
    let signUpAnim = anime({
        targets: '#signUpDialog',
        translateX: [0, -1500], duration: 750,
        easing: 'easeInOutQuad'
    });

    let loginAnim = anime({
        targets: '#loginDialog',
        translateX: [1500, 0], duration: 750,
        easing: 'easeInOutQuad'
    });
}

// Animate login box to move to the left and move forgot password field in from the right.
function getForgotPassword() {
    let forgotAnim = anime({
        targets: '#forgotDialog',
        translateX: [1500, 0], duration: 750,
        easing: 'easeInOutQuad'
    });

    let loginAnim = anime({
        targets: '#loginDialog',
        translateX: [0, -1500], duration: 750,
        easing: 'easeInOutQuad'
    });
}