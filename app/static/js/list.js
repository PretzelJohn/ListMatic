const titleText = document.getElementById("titleText");
const contentContainer = document.getElementById("contentContainer");
const time = document.getElementById("saveTime");

const saveBtn = document.getElementById("saveBtn");
const addBtn = document.getElementById("addBtn");
saveBtn.addEventListener('click', save);
addBtn.addEventListener('click', addRow);

const focusable = document.querySelectorAll(".focusable");
focusable.forEach((e) => {
    e.addEventListener('keydown', (event) => {
        if(event.keyCode === 13) {
            const next = e.parentNode.parentNode.nextSibling.nextSibling;
            if(next == null) {
                addRow();
            } else {
                const nextInput = next.firstChild.nextSibling.firstChild.nextSibling.nextSibling.nextSibling;
                if(nextInput != null) nextInput.focus();
            }
        }
    });
});

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
    cellContainer.appendChild(input);


    //Add trash button
    const trash = document.createElement("button");
    trash.setAttribute("class", "btn btn-danger btn-delete m-0");

    const trashIcon = document.createElement("img");
    trashIcon.setAttribute("style", "scale: 1.5");
    trashIcon.setAttribute("src", "/static/img/trash.svg");
    trash.appendChild(trashIcon);
    cellContainer.appendChild(trash);
    container.appendChild(cellContainer);
    contentContainer.appendChild(container);

    trash.onclick = () => {
        contentContainer.removeChild(container);
    }

    input.focus();
}