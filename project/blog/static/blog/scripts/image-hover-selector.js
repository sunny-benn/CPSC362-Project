
// Show the image in the tray that the user has hovered over 
var srcToCopy = '';
srcToCopy = $('.tray img').first().attr('src');
$('.selected #selected').attr('src', srcToCopy);
$('.selected #selected').css('visibility', 'visible');

// Select the images in the tray
$('.tray img').hover(

// When the user is hovering, add the source of the image to another div which hold an image.
function () {
	srcToCopy = $(this).attr('src');
	$('.selected #selected').attr('src', srcToCopy);
	$('.selected #selected').css('visibility', 'visible');
},

// When the user is not hovering, remove the source of the image and hide the CSS.
function () {
	//$('.selected #selected').attr('src', '');
	//$('.selected #selected').css('visibility', 'hidden');
});