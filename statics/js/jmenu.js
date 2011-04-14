$(function() {
    $('.accordian .entry:odd:gt(0)').hide();
    $('.accordian .entry:first').animate( {
	paddingLeft:"30px"
    });
    var gheight = parseInt($("#ldrawer").css("height"));
    $('.accordian .entry:even').each(function(){
	gheight = gheight - parseInt($(this).css("height"));
    });
    gheight = gheight - 10;
    $('.accordian .entry:odd').css("height", gheight.toString() + "px");
    $('.accordian .entry:odd').addClass('dimension');
    $('.accordian .entry:even:even').addClass('even');
    $('.accordian .entry:even:odd').addClass('odd');
    $('.accordian .entry:even').css('cursor', 'pointer');
    $('.accordian .entry:even').click( function() {
	var cur = $(this).next();
	var old = $('.accordian .entry:odd:visible');
	if ( cur.is(':visible') )
	    return false;
	old.slideToggle(500);
	cur.stop().slideToggle(500);
	$(this).stop().animate( {
	    paddingLeft:"30px"
	});
	old.prev().stop().animate( {
	    paddingLeft:"10px"
	});});});