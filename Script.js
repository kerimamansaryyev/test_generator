
const render = () =>{
    data.map( question =>(
        new Questions(question,data)
    ))
}

class Questions{
    static Number_of_questions = 0
    static Right_answers = []
    static Checked_answers = []
    static content = ''
    static data = null
    constructor(data,array){
        this.id = `Question${Questions.Number_of_questions}`;
        this.ID = Questions.Number_of_questions;
        this.description = data.descr;
        this.right = data.right;
        this.answers = data.others;
        const body = document.getElementById('body');
        Questions.content += this.body();
        body.innerHTML = Questions.content;
        if(Questions.Number_of_questions == 0){
            for(let item of array){
                Questions.Right_answers.push(item.right);
                Questions.Checked_answers.push(null);
            }
        }
        Questions.Number_of_questions++;
    }


    header = () =>(
        `<header>
            ${Questions.Number_of_questions+1}. ${this.description}
        </header>`
    )
    static check = () =>{
        let total = 0;
        for(let i=0;i<Questions.Right_answers.length;i++){
            if(Questions.Right_answers[i] == Questions.Checked_answers[i]){
                total++;
            }
        }
        return total;
    }


    static click = (value,ans_id,ques_id,num_of_answers) =>{
        Questions.Checked_answers[ques_id] = value;
        document.getElementById(`Sheet${ques_id}${ans_id}`).style.color = (Questions.Checked_answers[ques_id] == Questions.Right_answers[ques_id])?'#29ffc4':'#fd3c3c';
        document.getElementById(`Question${ques_id}`).innerHTML = (Questions.Checked_answers[ques_id] == Questions.Right_answers[ques_id])?'<span class="ans" style="color:#29ffc4">Right!</span>':'<span class="ans" style="color:#fd3c3c">Wrong!</span>';
        for(let i=0;i<num_of_answers;i++){
            if(i != ans_id){
                document.getElementById(`Sheet${ques_id}${i}`).style.color = 'white';
            }
        }
        const progress = document.getElementById('prog');
        progress.value = (Questions.check()/Questions.Right_answers.length)*100;
    }



    body = () =>(
        `<section class="main">
            ${this.header()}
            <section class="answersheet">
            <div id="${this.id}"></div>
                ${this.AnswerSheet()}
            </section>
        </section>
        `
    )




    AnswerSheet = () =>{
        let Content = '';
        const index_of_right = Math.round(Math.random() * (this.answers.length));
        const sorted_answers = [];
        for(let i=0;i<(this.answers.length+1);i++)
            sorted_answers.push(( i == index_of_right)? this.right: null);
        for(let i=0, ans = 0;i<(this.answers.length+1);i++){
            if( sorted_answers[i] === null ){
                sorted_answers[i] = this.answers[ans];
                ans++;
            }
            Content += `<div class="block"  id='Sheet${Questions.Number_of_questions}${i}' style="display:block">
                            <input type="radio"
                            onclick = "Questions.click(\`${String(sorted_answers[i])}\`,${i},${this.ID},${this.answers.length+1})"
                            name='Sheet${Questions.Number_of_questions}' 
                            value='${sorted_answers[i]}'>${sorted_answers[i]}
                        </div>`;
        }
        return Content;
    }
}
