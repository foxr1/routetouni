var bTop, bBottom, bLeft, bRight = '0%'; // Position of bubble before being clicked.
var bImg; // Last bubble's image.
var bSize; // Size of bubble before click (mobile/desktop).
var tempBubble;
var tempBubbleHtml;

let tl = anime.timeline({
    easing: 'easeOutExpo',
    duration: 500
});

tl
.add({
    targets: '#universityHeading',
    scale: [0,1.5],
    easing: 'spring',
}, 100)
.add({
    targets: '#bubble1',
    scale: [0,1],
    easing: 'spring',
}, 300)
.add({
    targets: '#bubble2',
    scale: [0,1],
    easing: 'spring',
}, 400)
.add({
    targets: '#bubble3',
    scale: [0,1],
    easing: 'spring',
}, 500)
.add({
    targets: '#bubble4',
    scale: [0,1],
    easing: 'spring',
}, 600)
.add({
    targets: '#bubble6',
    scale: [0,1],
    easing: 'spring',
}, 700)
.add({
    targets: '#bubble7',
    scale: [0,1],
    easing: 'spring',
}, 800)
.add({
    targets: '#bubble8',
    scale: [0,1],
    easing: 'spring',
}, 900)
.add({
    targets: '#bubble5',
    scale: [0,1],
    easing: 'spring',
}, 1000)
.add({
    targets: '#login',
    scale: [0,1],
    easing: 'spring',
}, 1100);

function bubbleClick(bubble, img, nextPage) {
    let bubbleEl = document.getElementById(bubble)
    let bubbleStyles = window.getComputedStyle(document.querySelector('#' + bubble));
    if (bubbleStyles.borderRadius === '50%' && bubbleStyles.transform <= "matrix(1.5, 0, 0, 1.5, 0, 0)") {
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
        let expandBubble = anime({
            targets: '#' + bubble,
            keyframes: [
                {scale: 30, duration: 1000},
                {borderRadius: '0%'},
                {height: '100%'},
                {width: '100%'},
                {top: '0%'},
                {bottom: '0%'},
                {left: '0%'},
                {right: '0%'},
                {scale: 1}

            ],
            duration: 100,
            easing: 'easeInOutQuad',
            update: function(anim) {
                if (anim.progress === 100) {
                    xhttp.send();
                    // window.location.assign();
                }
            }
        });

        let back = anime({
           targets: "#back",
           left: '15px',
           easing: 'easeInOutQuad'
        });
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

    let hideBack = anime({
        targets: "#back",
        left: '-100px',
        easing: 'easeInOutQuad'
    });

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
}

function loginPageTransition(page1, page2) {
    let page1Transition = anime({
        targets: page1,
        left: '-100%', duration: 750,
        easing: 'easeInOutQuad'
    });

    page1Transition.finished.then(openNextPage);

    function openNextPage() {
        window.open(page2, "_self");
    }
}

function onPageLoaded() {
    var redBox = document.createElement('span');
    redBox.id = "redBox"
    redBox.style.borderRadius = '50%';
    redBox.style.width = '2000px';
    redBox.style.height = '2000px';
    redBox.style.position = 'absolute';
    redBox.style.left = '50%';
    redBox.style.top = '-90%';
    redBox.style.transform = 'translateX(-50%)';
    redBox.style.margin = '0 auto';
    redBox.style.backgroundColor = '#d91a35';
    document.body.insertBefore(redBox, document.body.firstChild);
}

function openSignUp() {
    let signUpAnim = anime({
        targets: "#signUp",
        left: '50%',
        top: '50%',

        easing: 'easeInOutQuad'
    });
}