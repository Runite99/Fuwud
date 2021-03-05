var input = document.querySelector('[name="mail"]');
var error = document.getElementById('submit_btn');

function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

input.addEventListener('keydown', function(){
    // Whatever you want
    console.log(validateEmail(this.value))
    if(validateEmail(this.value) == 1) {
        // You can control style of your invalid input with .invalid
        error.disabled = false; // Display your custom error
    } else {
        error.disabled = true;
    }
});