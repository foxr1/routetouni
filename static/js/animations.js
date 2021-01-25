var bTop, bBottom, bLeft, bRight = '0%'; // Position of bubble before being clicked.
var bImg; // Last bubble's image.
var bSize; // Size of bubble before click (mobile/desktop).

// Which ever bubble is clicked from the home page is stored temporarily so it can be referenced when the user clicks
// the back button.
var tempBubble;
var tempBubbleHtml;

let tl = anime.timeline({
    easing: 'easeOutExpo',
    duration: 500
});

// Timeline of all the bubbles animating in when the page loads in a ring around the Newcastle logo.
tl
.add({
    targets: '#universityHeading',
    scale: [0,1.5],
    borderRadius: '50%',
    easing: 'spring',
}, 100)
.add({
    targets: '#bubble1',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 300)
.add({
    targets: '#bubble2',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 400)
.add({
    targets: '#bubble3',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 500)
.add({
    targets: '#bubble4',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 600)
.add({
    targets: '#bubble6',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 700)
.add({
    targets: '#bubble7',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 800)
.add({
    targets: '#bubble8',
    scale: [0,1],
    borderRadius: '50%',
    easing: 'spring',
}, 900)
.add({
    targets: '#bubble5',
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

        function loadPage() {
            if (nextPage === "chat") {
                window.location.assign("/chat")
            } else {
                xhttp.send();
            }
        }
    }
}

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

function backPress() {
    let bubble1 = document.getElementById("bubble1");
    let bubble2 = document.getElementById("bubble2");
    let bubble3 = document.getElementById("bubble3");
    let bubble4 = document.getElementById("bubble4");
    let bubble5 = document.getElementById("bubble5");
    let bubble6 = document.getElementById("bubble6");
    let bubble7 = document.getElementById("bubble7");
    let bubble8 = document.getElementById("bubble8");
    let bubbles = [bubble1, bubble2, bubble3, bubble4, bubble5, bubble6, bubble7, bubble8];
    let bubblesIds = ["#bubble1", "#bubble2", "#bubble3", "#bubble4", "#bubble5", "#bubble6", "#bubble7", "#bubble8"];

    if (tempBubble != null) { // Check if the user has previously come from the home page.
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
        window.open("/", "_self");
    }
}

// Animate page to move off to the left and then redirect to login page which will animate on load.
function loginPageTransition(page1, page2) {
    let page1Transition = anime({
        targets: page1,
        left: '-110%', duration: 750,
        easing: 'easeInOutQuad'
    });

    page1Transition.finished.then(openNextPage);

    function openNextPage() {
        window.open(page2, "_self");
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