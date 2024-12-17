function applyTheme() {
    const errorMsg = document.getElementById('error-msg');
    if (errorMsg)
        errorMsg.remove();

    const colorPicker = document.getElementById('color-picker');
    const checkedRadio = document.querySelector('input[type="radio"]:checked');
    if (!checkedRadio) {    
        // alert("Please select a theme to apply.");
        return;
    }
    const label = document.querySelector(`label[for="${checkedRadio.id}"]`);

    const color1 = label.querySelector('#color1').value;
    const color2 = label.querySelector('#color2').value;
    const color3 = label.querySelector('#color3').value;

    if ((color1 == color2) || (color1 == color3) ||
        (color2 == color1) || (color2 == color3) ||
        (color3 == color1) || (color3 == color2)) {
        const newDiv = document.createElement("div");
        newDiv.setAttribute("id", "error-msg");
        newDiv.setAttribute("class", "mt-3");
        newDiv.innerHTML = "<p>Please choose three different colors ;)</p>";
        colorPicker.append(newDiv);
        return;
    }

    document.documentElement.style.setProperty('--background-color', color1);
    document.documentElement.style.setProperty('--secondary-color', color2);
    document.documentElement.style.setProperty('--accent-color', color3);
    document.documentElement.style.setProperty('--fourth-color', darkenColor(color1, 10));

    const submitContent = document.getElementById('submit-theme');
    submitContent.innerHTML = "Apply theme";

    colorPicker.addEventListener("click", () => {
        backgroundColor = color1;
        secondaryColor = color2;
        accentColor = color3;
        fourthColor = darkenColor(color1, 10);
    })
}

function applyDefaultTheme() {
    const submitContent = document.getElementById('submit-theme');
    submitContent.innerHTML = "Test the theme";
    document.documentElement.style.setProperty('--background-color', backgroundColor);
    document.documentElement.style.setProperty('--secondary-color', secondaryColor);
    document.documentElement.style.setProperty('--accent-color', accentColor);
    document.documentElement.style.setProperty('--fourth-color', darkenColor(backgroundColor, 10));
}

function changeColor(inputElement) {
    // Get the selected color from the input element
    const color = inputElement.value;

    // Get the parent div (pill) of the clicked color input
    const pillSection = inputElement.closest('.pill-section');

    // Change the background color of the pill section
    pillSection.style.backgroundColor = color;
}
