// const urls = {
//     home: "{% url 'home' %}",
//     localgame: "{% url 'localgame' %}",
//     lobby: "{% url 'lobby_index' %}",
// };

// const menuToggler = document.getElementsByClassName('navbar-toggler')
// document.addEventListener("on", (event) => {

// const bsCollapse = bootstrap.Collapse.getOrCreateInstance(menuToggle, {toggle: false})
// navLinks.forEach((l) => {
//     if (menuToggle.classList.contains('show')) {  // only fire on mobile
//         l.addEventListener('click', () => { 
//             bsCollapse.toggle() 
//         })
//     }
// })

// let windowSize = window.matchMedia("(max-width: 442px)")
// let expandContent = document.getElementsByClassName('expand-content');
// for (let i = 0; i < expandContent.length; i++) {
//   if (expandContent[i].style.display = "block" || expandContent[i].style.display === "") {
//     expandContent[i].style.display = "none";
//   }
// }
function expandMenu() {
  let expandContent = document.getElementsByClassName('expand-content');
  for (let i = 0; i < expandContent.length; i++) {
    if (expandContent[i].style.display === "none" || expandContent[i].style.display === "") {
      expandContent[i].style.display = "block";
    } else {
      expandContent[i].style.display = "none";
    }
  }
}

window.onresize = function () {
  if (window.innerWidth < 278)
    document.getElementById("expand-content-2").className += " expand-content";
    
  let expandContent = document.getElementsByClassName('expand-content');
  
  if (window.innerWidth > 278) {
    for (let i = 0; i < expandContent.length; i++) {
      expandContent[i].style.display = "";
    }
  }
};

// let debounceTimeout;
// let prevScrollpos = window.scrollY;

// function handleScroll() {
//   clearTimeout(debounceTimeout);
//   debounceTimeout = setTimeout(() => {
//     let currentScrollPos = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop;
//     if (prevScrollpos > currentScrollPos) {
//       document.getElementById("nav").style.bottom = "0";
//       // nav.classList.add("bounce");
//       // setTimeout(() => {
//       //   nav.classList.remove("bounce");
//       // }, 500);
//     } else {
//       document.getElementById("nav").style.bottom = "-100px";
//     }
//     prevScrollpos = currentScrollPos;
//   }, 50);
// }

// window.addEventListener("scroll", handleScroll);
// window.addEventListener("touchmove", handleScroll);
// // window.addEventListener("touchstart", handleScroll);
// // window.addEventListener("touchend", handleScroll);

let navBarManualOverride = false;
let debounceTimeout;
let inactivityTimeout;
let prevScrollpos = window.scrollY;

function handleScroll(secAmount) {
  if (navBarManualOverride) return;

  clearTimeout(debounceTimeout);
  clearTimeout(inactivityTimeout);

  debounceTimeout = setTimeout(() => {
    let currentScrollPos = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop;

    // Hide the navbar when scrolling down
    if (prevScrollpos > currentScrollPos) {
      document.getElementById("nav").style.bottom = "0";
    } else {
      document.getElementById("nav").style.bottom = "-100px";
    }

    prevScrollpos = currentScrollPos;

    inactivityTimeout = setTimeout(() => {
      document.getElementById("nav").style.bottom = "0";
    }, secAmount);
  }, 10); // Debounce timeout for scroll
}

// Reset inactivity timeout if there's any scroll or touch activity
// function resetInactivityTimer(secAmount) {
//   clearTimeout(inactivityTimeout);
//   inactivityTimeout = setTimeout(() => {
//     document.getElementById("nav").style.bottom = "0";
//   }, secAmount); // Reset the timer to show the navbar after seconds of inactivity
// }

// To ensure the navbar shows up after seconds of inactivity even if there is no initial scroll/touch
function setNavbarInactivityTimeout(secAmount) {
  if (navBarManualOverride) return;
  clearTimeout(inactivityTimeout);
  inactivityTimeout = setTimeout(() => {
    document.getElementById("nav").style.bottom = "0";
  }, secAmount);
}

// Add event listeners for scroll and touch
window.addEventListener("scroll", () => handleScroll(3000));
window.addEventListener("touchmove", () => handleScroll(3000), { passive: true });
window.addEventListener("touchstart", () => setNavbarInactivityTimeout(3000));
window.addEventListener("touchend", () => setNavbarInactivityTimeout(3000));

setNavbarInactivityTimeout(3000);