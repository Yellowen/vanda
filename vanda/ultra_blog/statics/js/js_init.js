function addpanel () {
    var area2 = new nicEditor({fullPanel : true}).panelInstance('id_content');
}
bkLib.onDomLoaded(function() { addpanel(); });
