$(document).ready(function() {
	var objs = $('.file-upload');
	if (objs) {
		objs.each(function (index) { 
			var a = $(this).find('a');
			var src = a.html();
			if (index == 0) {
				a.html("<img src='/media/" + src + "' height='64'>");
			}
			else {
				a.html("<img src='/media/" + src + "' height='32'>");
			}
		});
	}	
});