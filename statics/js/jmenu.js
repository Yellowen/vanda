$(function() {
    $('.accordian entry')
    $('.accordian li:odd:gt(0)').hide();
    $('.accordian li:first').animate( {
	paddingLeft:"30px"
    });
    var gheight = parseInt($("#ldrawer").css("height"));
    $('.accordian li:even').each(function(){
	gheight = gheight - parseInt($(this).css("height"));
    });
    gheight = gheight - 10;
    $('.accordian li:odd').css("height", gheight.toString() + "px");
    $('.accordian li:odd').addClass('dimension');
    $('.accordian li:even:even').addClass('even');
    $('.accordian li:even:odd').addClass('odd');
    $('.accordian li:even').css('cursor', 'pointer');
    $('.accordian li:even').click( function() {
	var cur = $(this).next();
	var old = $('.accordian li:odd:visible');
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