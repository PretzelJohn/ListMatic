const titleText = document.getElementById("titleText");
const time = document.getElementById("saveTime");
const contentContainer = document.getElementById("contentContainer");
const inviteContentContainer = document.getElementById("inviteContentContainer");

const saveBtn = document.getElementById("saveBtn");
const addBtn = document.getElementById("addBtn");
const addUserBtn = document.getElementById("addUserBtn");
saveBtn.addEventListener('click', save);
addBtn.addEventListener('click', addRow);
addUserBtn.addEventListener('click', addUser);

const focusable = document.querySelectorAll(".focusable");
focusable.forEach((e) => {
    e.addEventListener('keydown', next);
});

function next() {
    if(event.keyCode === 13) {
        const next = event.target.parentNode.parentNode.nextSibling;
        if(next == null || next.nextSibling == null) {
            addRow();
        } else {
            const nextInput = next.nextSibling.firstChild.nextSibling.firstChild.nextSibling.nextSibling.nextSibling;
            if(nextInput != null) nextInput.focus();
        }
    }
}

//Saves the list
function save() {
    let arr = [];
    for(let i = 0; i < contentContainer.children.length; i++) {
        const child = contentContainer.children[i].children[0].children[1];
        if(child.hasAttribute("onclick")) continue;
        arr.push(child.value);
    }

    const data = {title: titleText.value, content: arr}

    const tokens = window.location.href.split('/');
    const url = "/"+tokens[tokens.length-1]+"/update";
    console.log(url);
    if(tokens.length > 0) {
        console.log(tokens[tokens.length - 1]);
        fetch(url, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(res => {
            if(res.ok) {
                console.log("Saved! response: ", res);
                const date = new Date(Date.now()).toLocaleTimeString();
                time.innerText = "Last saved at " + date;
            }
        });
    }
}

//Adds a new row to the list
function addRow() {
    const container = document.createElement("tr");
    container.setAttribute("draggable", "true");
    container.setAttribute("ondragstart", "dragstart()");
    container.setAttribute("ondragover", "dragmove()");
    container.setAttribute("ondragend", "dragend()");

    const cellContainer = document.createElement("td");
    cellContainer.setAttribute("class", "hstack p-1");


    //Add grip icon
    const grip = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    grip.setAttribute("width", "24");
    grip.setAttribute("height", "24");
    grip.setAttribute("fill", "#333");
    grip.setAttribute("class", "bi bi-grip-vertical");
    grip.setAttribute("viewBox", "0 0 16 16");
    grip.innerHTML = '<path d="M7 2a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM7 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM7 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm-3 3a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm-3 3a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>'
    cellContainer.appendChild(grip);


    //Add text input
    const input = document.createElement("input");
    input.setAttribute("class", "focusable form-text w-100 flex-grow-1 m-0 me-1");
    input.setAttribute("type", "text");
    input.setAttribute("placeholder", "...");
    input.setAttribute("value", "");
    input.addEventListener('keydown', next);
    cellContainer.appendChild(input);


    //Add trash button
    const trash = document.createElement("button");
    trash.setAttribute("class", "btn btn-danger btn-delete m-0");
    trash.onclick = () => {
        contentContainer.removeChild(container);
    }

    const trashIcon = document.createElement("img");
    trashIcon.setAttribute("style", "scale: 1.5");
    trashIcon.setAttribute("src", "/static/img/trash.svg");
    trash.appendChild(trashIcon);
    cellContainer.appendChild(trash);
    container.appendChild(cellContainer);
    contentContainer.appendChild(container);

    input.focus();
}

//Adds a user to the invite modal
function addUser() {
    const container = document.createElement("tr");

    const cellContainer = document.createElement("td");
    cellContainer.setAttribute("class", "hstack gap-2 w-100");


    //Add profile picture
    const img = document.createElement("img");
    img.setAttribute("width", "32");
    img.setAttribute("height", "32");
    img.setAttribute("src", "https://listmatic.s3.us-east-2.amazonaws.com/default_profile.jpg");
    cellContainer.appendChild(img);


    //Add username text box
    const textContainer = document.createElement("div");
    textContainer.setAttribute("class", "flex-grow-1 text-start");

    const input = document.createElement("input");
    input.setAttribute("name",  "username");
    input.setAttribute("class", "form-text w-100 flex-grow-1 m-0 me-1");
    input.setAttribute("type", "text");
    input.setAttribute("placeholder", "username");
    input.setAttribute("value", "");
    input.setAttribute("autocomplete", "off");
    textContainer.appendChild(input);
    cellContainer.appendChild(textContainer);


    //Add select dropdown
    const select = document.createElement("select");
    select.setAttribute("name", "role");
    select.setAttribute("id", "roles");

    const optionEditor = document.createElement("option");
    optionEditor.setAttribute("value", "editor");
    optionEditor.innerHTML = "Editor";
    select.appendChild(optionEditor);

    const optionViewer = document.createElement("option");
    optionViewer.setAttribute("value", "viewer");
    optionViewer.setAttribute("selected", "selected")
    optionViewer.innerHTML = "Viewer";
    select.appendChild(optionViewer);
    cellContainer.appendChild(select);


    //Add delete button
    const deleteBtn = document.createElement("button");
    deleteBtn.setAttribute("class", "btn-close");
    deleteBtn.onclick = () => {
        inviteContentContainer.removeChild(container);
    }
    cellContainer.appendChild(deleteBtn);
    container.appendChild(cellContainer);
    inviteContentContainer.appendChild(container);

    input.focus();
}