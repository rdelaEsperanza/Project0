document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(event) {
  event.preventDefault();
  
	// Fetch emails and post to send
	fetch('/emails' , {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
      })
    })
	.then(response => load_mailbox('sent'));
}

function load_email(id) {

  // Show read-email-view and hide others
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-email-view').style.display = 'block';

  fetch('/emails/' + id)
	.then(response => response.json())
	.then(email => {
    // can't seem to get the read values right... looks like the value defaults to true even though model states false
    // email.read === true;
    console.log(email);
    // Render read-email-view
    var readone = document.querySelector('#read-email-view');
    readone.innerHTML = `
    <div class="email-info">
      <div class="pseudo-label">
          <b>ID: </b>
          <u>${email.id}</u>
        </div>
        <div class="pseudo-label">
          <b>From: </b>
          <u>${email.sender}</u>
        </div>
        <div class="pseudo-label">
          <b>To: </b>
          <u>${email.recipients}</u>
        </div>
        <div class="pseudo-label">
          <b>Subject: </b>
          <u>${email.subject}</u>
        </div>
        <div class="pseudo-label">
          <b>Timestamp: </b>
          <u>${email.timestamp}</u>
        </div>
        <div class="pseudo-label">
          <b>Message: </b>
          <u>${email.body}</u>
        </div>
      </div>
    `;

    //allow user to reply
    var replyButton = document.createElement('button');
    replyButton.classList.add('tertiary');
    replyButton.innerHTML=`<i class="fa fa-reply"></i> Send Reply`;
    replyButton.addEventListener('click', () => {

        //call compose_email and populate
        compose_email();
        document.querySelector('#compose-recipients').value = email.sender;
        var subject = email.subject;
        //this was a bear! add re: to original reply
        console.log(subject.split(" ", 1)[0]);
        if (subject.split(" ", 1)[0] != "Re:") {
          subject = "Re: " + subject;
        }
        document.querySelector('#compose-subject').value = subject;

        //add preface to message body - why doesn't this render in html?
        var body = `
        On ${email.timestamp}, ${email.sender} wrote: ${email.body}
      `;
        document.querySelector('#compose-body').value = body;
      });
      //add reply button to message
      readone.appendChild(replyButton);

      //allow user to archive email and return to inbox
      var archiveButton = document.createElement('button');
      archiveButton.classList.add('tertiary');
      archiveButton.innerHTML = !email.archived ? `<i class="fa fa-archive"></i> Archive` : `<i class=" fa fa-box-open"></i> Unarchive`;
      archiveButton.addEventListener('click', () => {
          fetch('/emails/' + email.id, {
            method: 'PUT',
            body: JSON.stringify({ archived: true })
          })
            .then(response => load_mailbox('inbox'));
        });
      readone.appendChild(archiveButton);
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-email-view').style.display = 'none';

  
  // document.querySelector('#emails-view').innerHTML = `<h2>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h2>`;

  // Fetch emails, show the mailbox name and create table to hold email listing 

  fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {
      console.log(emails)
      // create html for individual emails and populate with email summary content
      var listing = document.querySelector('#emails-view');
      listing.innerHTML = `
      <h2>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h2>
      <table>
        <tr class="email headers">
          <th class="email-id"> Email ID </th>
          <th class="sender"> Sender </th>
          <th class="subject"> Subject </th>
          <th class="timestamp"> Timestamp </th>
        </tr>
      </table>
      `;
      emails.forEach(email => {
        var tr = document.createElement('tr');
        tr.classList.add('email');
        if (email.read != false) {
          tr.classList.add('read');
        }
        tr.innerHTML = 
          `
            <td class="email-id"> ${email.id} </td>
            <td class="sender"> ${email.sender} </td>
            <td class="subject"> ${email.subject}</td>
            <td class="timestamp"> ${email.timestamp}</td>
          `;
        tr.addEventListener('click', () => load_email(email['id']));
        document.querySelector('tbody').append(tr);
        });
      })
  }