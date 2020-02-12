function show(id){
  console.log("usando esto");
  if (document.getElementById){ 
  var el = document.getElementById(id); 
  el.style.display = (el.style.display == 'none') ? 'block' : 'none';
  }
}
let texto = "<a href='#' class='success link' onclick='show(`contenido`)'>Preciona Click Aqui</a>";
const BLACKLISTED_KEY_CODES = [38];
const COMMANDS = {
  mas: texto,
  reglas: 'Estas serian las reglas a tener en cuenta dentro del team............',
  help:
    'Comandos de ayuda: <span class="code">about</span>, <span class="code">experience</span>, <span class="code">skills</span>, <span class="code">contact</span>, <span class="code">reglas</span>,<span class="code">Reto</span>',
  about:
    "Hola 👋<br>Somos el Team Whoami. Un equipo de hackers que se esta renobando todo el tiempo, con el fin de ayudar y tener una comunidad fuerte de hacktivistas..",
  skills:
    '<span class="code">Habilidades que hay dentro de los que conforman el team:</span> Python, HTML, CSS, JavaScript, shell, Php, SQL inyeccion, etc.. <br><span class="code">Tecnologias que usamos:</span> Git, SQL, Postgresql, Mongo etc..<br><span class="code">Frameworks:</span> React.js, Vue.js, Django, Angular',

  reto: "<a href='./Reto.wap' class='success link'>Reto.wab <--- es un ejemplo aun no esta pero seria el reto de ingreso al team para tener tu clave de acceso</a>",
  experience: "hackeos a bancos correos y pishing facebook google y las novias",
  contact:
    "para contactar a alguien deja tu mensaje aqui, por seguridad no brindamos informacion personal a ninguno de nuestros integrantes, la premisa es no confies en el queso att:El raton<br><a href='#' class='success link'>Facebook</a> ,<a href='https://www.instagram.com/jatin.codes/' class='success link'>Instagram</a>, <a href='https://www.twitter.com/jatinn_r/' class='success link'>Twitter</a>"
};
let userInput, terminalOutput;

const app = () => {
  userInput = document.getElementById("userInput");
  terminalOutput = document.getElementById("terminalOutput");
  document.getElementById("dummyKeyboard").focus();
  console.log("Application loaded");
};

const execute = function executeCommand(input) {
  let output;
  input = input.toLowerCase();
  if (input.length === 0) {
    return;
  }
  output = `<div class="terminal-line"><span class="success">➜</span> <span class="directory">~</span> ${input}</div>`;
  if (!COMMANDS.hasOwnProperty(input)) {
    output += `<div class="terminal-line">no such command: ${input}</div>`;
    console.log("Oops! no such command");
  } else {
    output += COMMANDS[input];
  }

  terminalOutput.innerHTML = `${
    terminalOutput.innerHTML
  }<div class="terminal-line">${output}</div>`;
  terminalOutput.scrollTop = terminalOutput.scrollHeight;
};

const key = function keyEvent(e) {
  const input = userInput.innerHTML;

  if (BLACKLISTED_KEY_CODES.includes(e.keyCode)) {
    return;
  }

  if (e.key === "Enter") {
    execute(input);
    userInput.innerHTML = "";
    return;
  }

  userInput.innerHTML = input + e.key;
};

const backspace = function backSpaceKeyEvent(e) {
  if (e.keyCode !== 8 && e.keyCode !== 46) {
    return;
  }
  userInput.innerHTML = userInput.innerHTML.slice(
    0,
    userInput.innerHTML.length - 1
  );
};



document.addEventListener("keydown", backspace);
document.addEventListener("keypress", key);
document.addEventListener("DOMContentLoaded", app);