function show() {
	var form = document.getElementById("comment");
	var insert = document.getElementById("insert-form");
	var base = document.getElementById("comment-form");
	insert.style.visibility = 'hidden';
	form.style.visibility = 'visible';
	base.style.height = '270px';
}