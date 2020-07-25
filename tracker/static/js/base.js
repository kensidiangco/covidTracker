const g = document.getElementById('global');
const c = document.getElementById('countries');

function activeGlobal(){
	g.classList.add('navbar-brand');
	sessionStorage.setItem('clicked', true);
}
function activeCountries(){
	g.classList.remove('navbar-brand');
	c.classList.add('navbar-brand');
	sessionStorage.removeItem('clicked');
}

window.onload = function(){
	var data = sessionStorage.getItem('clicked');
	if (data == 'true'){
		activeGlobal();
	}
	else {
		activeCountries();
	}
}