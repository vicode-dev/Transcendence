function applyTheme() {
    const errorMsg = document.getElementById('error-msg');
    if (errorMsg)
        errorMsg.remove();

    const colorPicker = document.getElementById('color-picker');
    const color1 = document.getElementById('color1').value;
    const color2 = document.getElementById('color2').value;
    const color3 = document.getElementById('color3').value;

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

    const submitContent = document.getElementById('submit-theme');
    submitContent.innerHTML = "Apply theme";

    colorPicker.addEventListener("click", () => {
        backgroundColor = color1;
        secondaryColor = color2;
        accentColor = color3;
    })
}

function applyDefaultTheme() {
    const submitContent = document.getElementById('submit-theme');
    submitContent.innerHTML = "Test a theme";
    document.documentElement.style.setProperty('--background-color', backgroundColor);
    document.documentElement.style.setProperty('--secondary-color', secondaryColor);
    document.documentElement.style.setProperty('--accent-color', accentColor);
}

function changeColor(inputElement) {
    // Get the selected color from the input element
    const color = inputElement.value;

    // Get the parent div (pill) of the clicked color input
    const pillSection = inputElement.closest('.pill-section');

    // Change the background color of the pill section
    pillSection.style.backgroundColor = color;
}
