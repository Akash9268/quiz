// creating an array and passing the number, questions, options, and answers

// creating an array and passing the number, questions, options, and answers
console.log("hello")
const url = window.location.href
const quizBox = document.getElementById('quiz_box')
const ScoreBox = document.getElementById('score-box')
const ResultBox = document.getElementById('result-box')



$.ajax({
    type:'GET',
    url: `${url}data`,
    success:function(response) {
      // body...
      const data = response.data
      data.forEach(el=>{
        for (const [question,answers] of Object.entries(el)){
            quizBox.innerHTML +=  `
              <hr>
              <div class="mb-2">
                <b>${question}</b>
              </div>
            `
            answers.forEach(answer=>{
                quizBox.innerHTML +=  `
                  <div>
                    <input type = "radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                    <label for "${question}">${answer}</label>
                  </div>

                `
            })
        }
      })
      
    },
    error:function(error){
      console.log(error)
    }
});


const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () =>{
  const elements = [...document.getElementsByClassName('ans')]
  const data = {}
  data['csrfmiddlewaretoken'] = csrf[0].value
  elements.forEach(el=>{
    if(el.checked)
    {
      data[el.name] = el.value
    }
    else
    {
      if(!data[el.name])
      {
        data[el.name] = null
      }
    }
  })

$.ajax({
    type:'POST',
    url: `${url}save/`,
    data : data,
    success:function(response) {
      const results = response.results
      console.log(results)
      quizForm.classList.add('not-visible')


      ScoreBox.innerHTML = `${response.passed ? 'Congratulations!!!  ' : 'Oops.. Better luck next time'}Your result is ${response.score.toFixed(2)}%`
      results.forEach(res=>{
          const resDiv = document.createElement("div")
          for(const [question,resp] of Object.entries(res)){
            resDiv.innerHTML +=  question
            const cls = ['container','p-3','text-light','h6']
            resDiv.classList.add(...cls)

            if(resp == 'not_answered')
            {
              resDiv.innerHTML += '-not answered'
              resDiv .classList.add('bg-danger')
            }

            else
            {
              const answer = resp['answered']
              const correct = resp['correct_answer']
              console.log(answer)
              console.log(correct)


              if(answer == correct)
              {
                resDiv.classList.add('bg-success')
                resDiv.innerHTML += `answered : ${answer}`
              }

              else
              {
                resDiv.classList.add('bg-danger')
                resDiv.innerHTML += `| correct answer : ${correct}`
                resDiv.innerHTML += `| answered : ${answer}`
              }
            }
          }

          // const body = document.getElementsByTagName('BODY')[0]
          ResultBox.append(resDiv)

      })
    },
    error:function(error) {
      // body...
      console.log(error)
    }


})

}

quizForm.addEventListener('submit',e=>{
  e.preventDefault()

  sendData()
})