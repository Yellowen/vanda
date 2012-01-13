
function filter(){
    types = document.getElementsByID('typesGroup');
    cats = document.getElementsByID('catsGroup');

    for (i=0; i<types.length; i++){
	if (types[i].checked==true)
	    selected_types += 
    }

    for (i=0; i<cats.length; i++){
	if (cats[i].checked==true)
	    alert("Checkbox at index "+i+" is checked!")
    }
}