// A implementer plus tard
// function applyTheme() {
//     let errorMsg = document.getElementById('error-msg');
//     if (errorMsg)
//         errorMsg.remove();

//     // const colorPicker = document.getElementById('color-picker');
//     const checkedRadio = document.querySelector('input[type="radio"]:checked');
//     if (!checkedRadio) {    
//         return;
//     }
//     const label = document.querySelector(`label[for="${checkedRadio.id}"]`);

//     const color1 = label.querySelector('#color1').value;
//     const color2 = label.querySelector('#color2').value;
//     const color3 = label.querySelector('#color3').value;

//     if ((color1 == color2) || (color1 == color3) ||
//         (color2 == color1) || (color2 == color3) ||
//         (color3 == color1) || (color3 == color2)) {
//             errorMsg.style.display = "block";
//         return;
//     }

//     document.documentElement.style.setProperty('--background-color', color1);
//     document.documentElement.style.setProperty('--secondary-color', color2);
//     document.documentElement.style.setProperty('--accent-color', color3);
//     document.documentElement.style.setProperty('--fourth-color', darkenColor(color1, 10));

//     // const submitContent = document.getElementById('submit-theme');
//     // submitContent.style.color = color2;
//     // submitContent.innerHTML = "Apply theme";

// }

// A implementer plus tard
// function applyDefaultTheme() {
//     // const submitContent = document.getElementById('submit-theme');
//     // submitContent.style.color = backgroundColor;
//     // submitContent.innerHTML = "Test the theme";
//     document.documentElement.style.setProperty('--background-color', backgroundColor);
//     document.documentElement.style.setProperty('--secondary-color', secondaryColor);
//     document.documentElement.style.setProperty('--accent-color', accentColor);
//     document.documentElement.style.setProperty('--fourth-color', darkenColor(backgroundColor, 10));
// }


function clickColor()
{
    let checkedRadio = document.querySelector('input[type="radio"]:checked');
    let label = document.querySelector(`label[for="${checkedRadio.id}"]`);
    
    const color1 = label.querySelector('.color1').value;
    const color2 = label.querySelector('.color2').value;
    const color3 = label.querySelector('.color3').value;    

    let errorMsg = document.getElementById("error-msg");
    if (new Set([color1, color2, color3]).size < 3) {
        if (errorMsg) errorMsg.style.display = "block";
        return;
    } else {
        if (errorMsg) errorMsg.style.display = "none";
    }

    // const colors = {
    //     '--background-color': backgroundColor,
    //     '--secondary-color': secondaryColor,
    //     '--accent-color': accentColor,
    //     '--fourth-color': fourthColor,
    // };

    // for (const [key, value] of Object.entries(colors)) {
    //     document.documentElement.style.setProperty(key, value);
    // }

    let backgroundColor = color1;
    let secondaryColor = color2;
    let accentColor = color3;
    let fourthColor = darkenColor(color1, 10);

    document.documentElement.style.setProperty('--background-color', backgroundColor);
    document.documentElement.style.setProperty('--secondary-color', secondaryColor);
    document.documentElement.style.setProperty('--accent-color', accentColor);
    document.documentElement.style.setProperty('--fourth-color', fourthColor);

    fetch(`/api/player/${document.querySelector('[name=playerId]').value}/theme/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            "theme": [accentColor.replace("#", "0x"), secondaryColor.replace("#", "0x"), backgroundColor.replace("#", "0x")]
        })
    })
}

function changeColor(inputElement) {
    const color = inputElement.value;
    const pillSection = inputElement.closest('.pill-section');
    if (pillSection) pillSection.style.backgroundColor = color;
}

function themeDestructor() {
    let colorPicker = document.getElementById('color-picker');
    if (colorPicker) colorPicker.removeEventListener("click", clickColor);
}

function themeMain() {
    // let colorschemes = document.getElementsByClassName('colorscheme');
    // for (let colorscheme of colorschemes) {
    //     colorscheme.addEventListener("mouseenter", applyTheme);
    //     colorscheme.addEventListener("mouseleave", applyDefaultTheme);
    // }
    let errorMsg = document.getElementById("error-msg");
    if (errorMsg) errorMsg.style.display = "none";
    let colorPicker = document.getElementById('color-picker');
    if (colorPicker) colorPicker.addEventListener("click", clickColor);

    destructors.push(themeDestructor);
}

addMain(themeMain);