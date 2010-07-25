// htmleditor.js
$(document).ready(function() {
  $("#id_content").wymeditor({ 
    updateSelector: "input:submit",
    updateEvent: "click"
  });
});