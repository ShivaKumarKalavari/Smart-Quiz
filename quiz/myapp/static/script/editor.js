require.config({ paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.1/min/vs" } });

const lang = {
    63: "javascript",
    35: "python",
    62: "java",
    54: "cpp",
    50: "c"
};

const lang_code = {
    63: "// Write your code here",
    35: "# Write your code here",
    62: "import java.util.*;\npublic class Main{\n    public static void main(String args[]){\n        // Write your code here\n    }\n}",
    54: "#include <bits/stdc++.h>\nusing namespace std;\nint main(){\n    // Write your code here\n    return 0;\n}",
    50: "#include <stdio.h>\nint main(){\n    // Write your code here\n    return 0;\n}"
};

let editor; // Declare editor globally
let value = 63; // Default to JavaScript

// Initialize Monaco Editor
function create_editor() {
    editor = monaco.editor.create(document.getElementById("editor-container"), {
        value: lang_code[value],
        language: lang[value],
        theme: "vs-dark"
    });
}

// Update editor configuration on language change
document.getElementById("language-select").onchange = function () {
    value = this.value;
    editor.setValue(lang_code[value]); // Update editor content
    monaco.editor.setModelLanguage(editor.getModel(), lang[value]); // Update editor language
};

// Show/hide the custom input textarea when checkbox is toggled
const customInputCheckbox = document.getElementById("custom-input-checkbox");
const customInputTextarea = document.getElementById("custom-input");

customInputCheckbox.addEventListener("change", () => {
    customInputTextarea.style.display = customInputCheckbox.checked ? "block" : "none";
});

// Run code function
function run() {
    const button = document.getElementById("run-code");
    // Change the color
    button.style.backgroundColor = "#afe8b1";
    // Revert to the original color after 1 second (1000ms)
    setTimeout(() => {
        button.style.backgroundColor = "#4CAF50";
    }, 1000);

    const source_code = editor.getValue();
    const language_id = document.getElementById("language-select").value;
    const stdin = customInputCheckbox.checked ? customInputTextarea.value : "";

    fetch("/execute/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ source_code, language_id, stdin }),
    })
        .then((response) => response.json())
        .then((data) => {
            const output = data.stdout || data.stderr || "No output";
            document.getElementById("output").innerText = output;
        })
        .catch((error) => console.error("Error:", error));
}

document.getElementById("run-code").addEventListener("click", run);

require(["vs/editor/editor.main"], create_editor);
