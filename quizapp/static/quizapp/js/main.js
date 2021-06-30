console.log('hello')

let modalBtns = document.getElementsByClassName('ris')//made an array now

const modalbody = document.getElementById('modal-body-confirm')

var i;
for(i = 0;i<modalBtns.length;i++)
{	
	let t = modalBtns[i];
	t.addEventListener('click',function(){
		let pk = t.getAttribute('data-pk')
		let name = t.getAttribute('data-quiz')
		let Number_of_ques = t.getAttribute('data-questions')
		let difficulty = t.getAttribute('data-difficulty')
		let Score = t.getAttribute('data-pass')
		let time = t.getAttribute('data-time')
		console.log(name)

		modalbody.innerHTML = `
			<div class= "h5 mb-3">Are you sure you want to begin "<b>${name}</b>" ?</div>
			<div class="text-muted">
				<ul>
					<li>difficulty: <b>${difficulty}</b></li>
					<li>Number of questions: <b>${Number_of_ques}</b></li>
					<li>score to pass: <b>${Score}</b></li>
					<li>time: <b>${time}</b> mins</li>
				</ul>
			</div>
		`
	
	})

}

