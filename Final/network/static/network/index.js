document.addEventListener('DOMContentLoaded', function() {

    // By default, load all messages 
    load_mailbox('all');

    document.addEventListener('click', event => {

        // Find what was clicked on
        const element = event.target;
    
        // Check if the user clicked on the edit button and do your magic
        if (element.className === 'edit-post') {
            element.style.display = 'none'
            element.parentElement.querySelector('.posted').style.display = 'none';
            element.parentElement.querySelector('.like-post').style.display = 'none';
            element.parentElement.querySelector('.edit-form').style.display = 'block';
        }
    });

     // Use buttons to access Compose and send new message
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#compose-form').addEventListener('submit', send_email);

    
});

function compose_email() {

    // Show compose view and hide other views and compose button
    document.querySelector('#messages-view').style.display = 'none';
    document.querySelector('#read-message-view').style.display = 'none';
    document.querySelector('#compose').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-body').value = '';
  }
  
  function send_email(event) {
    event.preventDefault();
    
      // Fetch emails and post to send
      fetch('/emails' , {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        body: document.querySelector('#compose-body').value
        })
      })
      .then(response => load_mailbox('all'));
  }
  
  function load_email(id) {
  
    // Show read-email-view and hide others
    document.querySelector('#messages-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#read-message-view').style.display = 'block';
  
    fetch('/emails/' + id)
      .then(response => response.json())
      .then(email => {
      console.log(email);
      // Render read-message-view
      var readone = document.querySelector('#read-message-view');
      readone.innerHTML = `
      <div class="message-info">
        <div class="pseudo-label">
            <b>ID: </b>
            <u>${email.id}</u>
          </div>
          <div class="flex-wrapper from-to">
            <div class="pseudo-label">
                <b>From: </b>
                <u>${email.sender}</u>
            </div>
            <div class="pseudo-label">
                <b>To: </b>
                <u>${email.recipients}</u>
            </div>
            <div class="pseudo-label">
                <b>Date: </b>
                <u>${email.timestamp}</u>
            </div>
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
          
  
          //add preface to message body - why doesn't this render in html?
          var body = `
          On ${email.timestamp}, ${email.sender} wrote: ${email.body}
        `;
          document.querySelector('#compose-body').value = body;
        });
        //add reply button to message
        readone.appendChild(replyButton);
  
    });
  }
  
  function load_mailbox(mailbox) {
    
    // Show the mailbox and hide other views
    document.querySelector('#messages-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#read-message-view').style.display = 'none';
  
   
    fetch('/emails/' + mailbox)
      .then(response => response.json())
      .then(emails => {
        console.log(emails)
        // create html for individual emails and populate with email summary content
        var listing = document.querySelector('#messages-view');
        
        listing.innerHTML = `
        
        <table>
          <tr class="message headers">
            <th class="sender"> From </th>
            <th class="recipient"> To </th>
            <th class="timestamp"> Date </th>
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
              <td class="sender"> ${email.sender} </td>
              <td class="recipient"> ${email.recipients} </td>
              <td class="timestamp"> ${email.timestamp}</td>
            `;
          tr.addEventListener('click', () => load_email(email['id']));
          document.querySelector('tbody').append(tr);
          });
        })
    }