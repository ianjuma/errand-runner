$(function () {

	//chained func + DOM selection
	$('<ul></ul>')
		.append('<li><a>jQuery.com</a></li><li><a>jQuery Documentation</a></li>')
		.find('a:first')
		.attr('href', 'http://www.jquery.com')
		.end()
		.appendTo('body');


	// Traversing the DOM -parent(), parents(), closest()
	console.log($('#start').parent().attr('id')); //0
	console.log($('#start').parent().parent().attr('id')); // 1
	console.log($('#start').parent()[0].id); // 0


	// manipulate the DOM
	$('<div><a></a></div>')
		.find('a')
		.text('jQuery')
		.attr('href', 'http://www.jquery.com')
		.end().appendTo('body'); // end used to close the find method



	$('#one').text('I am One'); // set text in element one
	$('#two').text('I am two');

	// Loop through $ object .foreach element log the ID attr
	$('article').each(function() {
		console.log($(this).attr('id'));
	});

	var listItems = $('li');
	console.log(listItems[0]);

	var headerItems = $('head');
	console.log(headerItems);
	console.log(headerItems[0]);


	var listItems = jQuery("li");
	var model = $('#best-model');

	var list_Unordered = $('ul li');
	var byclass = $('.model');


	// create jquery object from DOM element
	var someEl = $('.model');
	console.log(someEl);

	$(someEl, '.model-people');

	if ($('.model').length) {
		console.log("some");
	}

	// selecting specific element
	var listItems = $('li');
	var rawListItem = listItems[0]; //listitems.get(0)
	var html = rawListItem.innerHTML; // inner html content

	console.log(html); // logs list item 1 at index 0
	console.log(rawListItem);



	// creating new elements
	$('<p class="data"> Hey, Man! </p>');

	$( '<p>', {
  		html: 'Hello!',
  		'class': 'greet'
	});

	//$('.model').html('Hey I hate TDCC'); - sets entire html doc

	$('li').each(function(index, elem) {
		$(elem).prepend('<strong>' + (index+1) + ' ');
	});


	// chaining JS
	$('#my-button')
		.click(function() {
			console.log("I was clicked!");
		});

});