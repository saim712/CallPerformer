console.log('bismILLAH');
const wrapper=document.querySelector('.wrapper');
const loginlink=document.querySelector('.login-link');
const registerlink=document.querySelector('.register-link');
const btnPopup=document.querySelector('.btnlogin-popup');
const iconclose=document.querySelector('.icon-close');

registerlink.addEventListener('click',()=>{
    wrapper.classList.add('active');
});
loginlink.addEventListener('click',()=>{
    wrapper.classList.remove('active');
});
btnPopup.addEventListener('click',()=>{
    wrapper.classList.add('active-popup');
});
iconclose.addEventListener('click',()=>{
    wrapper.classList.remove('active-popup');
});



let saved_name = "example@example.com"; 
let passd = "123"; 

function validate() {
    let password = document.getElementById('password').value;
    let email = document.getElementById('email').value;

    if (saved_name.toLowerCase() !== email.toLowerCase() || passd !== password) {
        alert('Your credentials are incorrect');
        return false;
    }
    
    return true;
}
