var total = 0;

$('#getHouse').click(function () {
	// $('#alert-price').remove();
	renderTaskTwo("Property Management");
	// renderTotal(10);
	total+= 10;
	//updateTotal(10);
});


$('#getBill').click(function () {
	renderTaskTwo("Property Management");
	total+= 10;
});

$('#getProcurement').click(function () {
	renderTaskTwo("Property Management");
	total+= 10;
});


$('#getTranslators').click(function () {
	renderTaskTwo("Property Management");
	total+= 10;
});

$('#corporatePackages').click(function () {
	renderTaskTwo("Property Management");
	total+= 10;
});

$('#getBooking').click(function () {
	renderTaskTwo("Property Management");
	total+= 10;
});

$('#getClearance').click(function () {
	renderTaskTwo("Property Management");
	total+= 10;
});

$('#getShopping').click(function () {
	renderTaskTwo("Property Management");
	total+= 10;
});

$('#getProperty').click(function () {
	renderTaskTwo("Property Management");
	total+= 10;
});


$('#other').click(function () {
	task_cat = $('#text-input').val();
	renderTaskTwo("Property Management");
	total+= 10;
});


function updateTotal (total) {

	html = '<div class="list-group tickets top-space">' +
        '<li href="#" class="list-group-item">Total<span class="badge badge-success">$ ' + total + '</span></li>' +
    '</div>'

	$('#alert-price').append(html);
}


function renderTask (package) {

    console.log(package);

    $('#order-table').append('<tr>' +
      '<td style="width:30%;">'+ package +'</td>' +
      '<td> $10 </td>' +
      '<td class="text-right"> $10 </td>' +
      '<td class="text-center"> <a class="label' + 
      'label-danger" href="#"><i class="fa fa-times"></i></a></td>' +
    '</tr>');
}

function renderTaskTwo (package) {

    console.log(package);

    $('#order-table2').append('<tr>' +
      '<td style="width:30%;">'+ package +'</td>' +
      '<td> $10 </td>' +
      '<td class="text-right"> $10 </td>' +
      '<td class="text-center"> <a class="label' + 
      'label-danger" href="#"><i class="fa fa-times"></i></a></td>' +
    '</tr>');
}


function renderTotal (total) {

	html = '<div class="list-group tickets top-space">' +
        '<li href="#" class="list-group-item">Total<span class="badge badge-success">$ ' + total + '</span></li>' +
    '</div>'

	$('#alert-price').append(html);
}


function renderAlert() {
	$('#alert-div').append(
		'<div class="alert alert-success alert-white rounded top-space">' +
	        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
	        ' <div class="icon"><i class="fa fa-check"></i></div>' +
	        '<strong>Total </strong> $' + total +
		'</div>'
	);
}