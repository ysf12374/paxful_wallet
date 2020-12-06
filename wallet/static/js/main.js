const identity = document.getElementById('idc')

const documnt = document.getElementById('docc')

const busness = document.getElementById('accc')


identity.addEventListener("click",displayidc)
documnt.addEventListener("click",displaydocc)
busness.addEventListener("click",acccc)

function displayidc() {
	document.getElementById('identitychecks').style.display='block';
	document.getElementById('documentcheck').style.display='none';
	document.getElementById('business').style.display='none';
	// body...
}

function displaydocc() {
	document.getElementById('identitychecks').style.display='none';
	document.getElementById('documentcheck').style.display='block';
	document.getElementById('business').style.display='none';
	// body...
}

function acccc() {
    document.getElementById('identitychecks').style.display='none';
    document.getElementById('documentcheck').style.display='none';
    document.getElementById('business').style.display='block';
    // body...
  }



setTimeout(function(){
	$('#message').faadeOut('slow');
},3000);