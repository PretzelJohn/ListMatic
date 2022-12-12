/* Drag and drop */
var row;
var children;

function dragstart() {
  row = event.target;
}

function dragover() {
  let e = event;
  e.preventDefault();

  if(e.target.parentNode.nodeName === "TR" && row.nodeName == "TR") {
    children = Array.from(e.target.parentNode.parentNode.children);


    if(children.indexOf(e.target.parentNode) > children.indexOf(row)) {
      e.target.parentNode.after(row);
    } else {
      e.target.parentNode.before(row);
    }

    row.style.background = "#7FC4FD";
  }
}

function dragdrop() {
  row.style.background = "none";
}
