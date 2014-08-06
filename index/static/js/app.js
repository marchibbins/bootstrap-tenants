// Stop links in collapsed rows from closing.
$('.js-nested-link').on('click', function(e){
	e.stopPropagation();
});