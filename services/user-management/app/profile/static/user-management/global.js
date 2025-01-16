function setBottomMargins(className) {
    const elements = document.querySelectorAll(className);
    const navbar = document.getElementById('nav');
    const navBarHeight = navbar.offsetHeight 
                       + parseInt(getComputedStyle(navbar).marginBottom) 
                       + parseInt(getComputedStyle(navbar).marginTop);

    elements.forEach((element) => {
        element.style.setProperty('--bottom-margin', navBarHeight + 'px');
        // element.style.setProperty('margin-bottom', navBarHeight + 'px');
        // element.style.marginBottom = navBarHeight + 'px';

    });
}

setBottomMargins('.user-management-margin-bottom');