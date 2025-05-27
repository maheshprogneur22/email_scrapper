document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const fileInput = document.querySelector("input[type='file']");
    const submitButton = document.querySelector("button[type='submit']");

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            const label = document.createElement("p");
            label.textContent = `Selected File: ${fileName}`;
            label.style.color = "#333";
            label.style.marginTop = "10px";
            fileInput.parentNode.appendChild(label);
        }
    });

    form.addEventListener("submit", function () {
        submitButton.disabled = true;
        submitButton.textContent = "Extracting Emails...";
        submitButton.style.backgroundColor = "#888";
    });
});
