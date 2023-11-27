const hostForm = document.getElementById("hostForm");
const joinForm = document.getElementById("joinForm");

// Even listner added to hostButton to determine whether it should be enabled or disabled.
hostForm.addEventListener('keyup', function() {
    var hostCode = document.getElementById('hostCode');
    var hostButton = document.getElementById('hostButton');
    if (hostCode.value == '') {
        hostButton.setAttribute("disabled", null);
    } else {
        hostButton.removeAttribute("disabled");
    }  
  });

  // Even listner added to joinButton to determine whether it should be enabled or disabled.
  joinForm.addEventListener('keyup', function() {
    var joinCode = document.getElementById('joinCode');
    var joinButton = document.getElementById('joinButton');
    if (joinCode.value == '') {
        joinButton.setAttribute("disabled", null);
    } else {
        joinButton.removeAttribute("disabled");
    }  
  });