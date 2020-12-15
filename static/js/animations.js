var bTop, bBottom, bLeft, bRight = '0%'; // Position of bubble before being clicked.
var bImg; // Last bubble's image.
var bSize; // Size of bubble before click (mobile/desktop).

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
    targets: '#signUp',
    scale: [0,1],
    easing: 'spring',
}, 1100);

function bubbleClick(bubble, img) {
    let bubbleEl = document.getElementById(bubble)
    let bubbleStyles = window.getComputedStyle(document.querySelector('#' + bubble));
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
        easing: 'easeInOutQuad'
    });

    let back = anime({
       targets: "#back",
       left: '15px',
       easing: 'easeInOutQuad'
    });
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

    let revealImg = anime({
        targets: bImg,
        opacity: ['0%', '100%'],
        easing: 'easeInOutQuad'
    });

    for (let i = 0; i < 8; i++) {
        if (bubbles[i].style.zIndex === '2') {
            bubbles[i].style.top = bTop;
            bubbles[i].style.bottom = bBottom;
            bubbles[i].style.left = bLeft;
            bubbles[i].style.right = bRight;
            let decreaseBubble = anime({
                targets: bubblesIds[i],
                borderRadius: '50%',
                height: bSize,
                width: bSize,
                scale: [30, 1],
                easing: 'easeInOutQuad'
            });

            setTimeout(function() {
                bubbles[i].style.zIndex = '0';
            }, 1000);
            break;
        }
    }
}

function pageTransition(page1, page2) {
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

function openSignUp() {
    let signUpAnim = anime({
        targets: "#signUp",
        left: '50%',
        top: '50%',

        easing: 'easeInOutQuad'
    });
}