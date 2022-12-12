const titleText = document.getElementById("titleText");
const contentContainer = document.getElementById("contentContainer");
const time = document.getElementById("saveTime");

const saveBtn = document.getElementById("saveBtn");
const addBtn = document.getElementById("addBtn");
saveBtn.addEventListener('click', save);
addBtn.addEventListener('click', addRow);

//Saves the list
function save() {
    let arr = [];
    for(let i = 0; i < contentContainer.children.length; i++) {
        const child = contentContainer.children[i].children[0].children[0];
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
    container.setAttribute("class", "d-flex flex-row");

    const inputContainer = document.createElement("td");
    inputContainer.setAttribute("class", "flex-grow-1");

    const input = document.createElement("input");
    input.setAttribute("class", "form-text w-100");
    input.setAttribute("type", "text");
    input.setAttribute("placeholder", "...");
    inputContainer.appendChild(input);
    container.appendChild(inputContainer);

    const trashContainer = document.createElement("td");
    const trash = document.createElement("button");
    trash.setAttribute("class", "btn btn-danger btn-delete");

    const trashIcon = document.createElement("img");
    trashIcon.style.scale = "1.5";
    trashIcon.src = "/static/img/trash.svg";
    trash.appendChild(trashIcon);
    trashContainer.appendChild(trash);
    container.appendChild(trashContainer);
    contentContainer.appendChild(container);

    trash.onclick = () => {
        container.parentElement.removeChild(container);
    }
}