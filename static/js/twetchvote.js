
let mb_token = localStorage.getItem('mb_token');


const config = {
    clientIdentifier: '0a0d0fc8ab67212359a7e721bf1ce023',
    permission: mb_token,
    suggestedAmount: {
        amount: '3',
        currency: 'USD'
      },
      minimumAmount: {
        amount: '0.25',
        currency: 'USD'
      },
    onNewPermissionGranted: (token) => {
        localStorage.setItem('mb_token', token);
    }}

var imb;

function closeVoteDialog(){document.getElementById("vote-dialog").setAttribute("class", "modal");}

function vote(txId, voteType, recipientId) {
    console.log(txId);
    console.log(voteType);
    document.getElementById("vote-dialog-footer").innerHTML = "";
    document.getElementById("vote-dialog-text").innerText = "Sending payment...";
    document.getElementById("vote-dialog").setAttribute( 'class', 'modal is-active' );
    document.getElementById("loading-circle").setAttribute('class', 'loader')
    imb.swipe({
        buttonId: voteType,
        buttonData: txId,
        outputs: [{
          to: 'bigriz@moneybutton.com',
          amount: '0.02',
          currency: 'USD',
       },{
          to: 'ins1d30ut@moneybutton.com',
          amount: '0.02',
          currency: 'USD',
       },{
          to: recipientId.concat('@moneybutton.com'),
          amount: '0.02',
          currency: 'USD',
       }]
    }).then(
        ({ payment }) => {
        console.log(payment);
        let score = parseInt(document.getElementById("score-".concat(txId)).innerText);
        if (voteType === "upvote"){document.getElementById("score-".concat(txId)).innerText = score + 1};
        if (voteType === "downvote"){document.getElementById("score-".concat(txId)).innerText = score - 1};
        document.getElementById("loading-circle").setAttribute('class', 'loader is-hidden');
        document.getElementById("vote-dialog-text").innerText = "Your ".concat(voteType.concat(" was successful!"));
        document.getElementById("vote-dialog-footer").innerHTML = "<button class='button' onclick='closeVoteDialog();'>Ok</button>";
        },
    error => console.log(error)
    )
}

function firstTime() {
    if (mb_token === null) {
        document.getElementById("welcome-dialog").setAttribute( 'class', 'modal is-active' );
    }
}

document.addEventListener("DOMContentLoaded", function(e) {
    timeago.render(document.querySelectorAll('.render-datetime'));

    var contents = document.getElementsByClassName("post-content");
    for (var i = 0; i < contents.length; i++){
        let content = contents[i].innerText;
        content = Autolinker.link(content, {sanitizeHtml: true});
        contents[i].innerHTML = content;
        }

    firstTime();

    imb = new moneyButton.IMB(config);

});

//function showPopup(text, confirm, cancel, onClick){
//    let dialog = document.getElementById('dlg');
//    dialogPolyfill.registerDialog(dialog);
//    dialog.innerHTML = `<form method="dialog"><p>${text}</p>
//    <menu class="dialog-menu">
//        ${cancel === true ? "<button class='nes-btn cancel'>Cancel</button>" : ""}
//        <button class="nes-btn confirm" onclick="${onClick}">${confirm}</button>
//    </menu></form>`;
//    dialog.showModal();
//}